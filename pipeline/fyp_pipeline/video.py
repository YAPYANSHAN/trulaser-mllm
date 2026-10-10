"""Stage 2c - process-video model (PyTorch) and video evidence.

A photo shows the finished edge. A video of the cutting zone (coaxial process
camera, or a camera watching the spark jet under the sheet) shows HOW the cut
went: whether the glow was stable, oscillated, drifted or threw sparks upward.
The methods here follow the video papers in the review:

  * Cut the recording into fixed-length clips at a fixed frame rate, predict per
    clip, then combine the clips (Liu W. et al., 2026, ADOS-M1: 30 s clips at
    8 FPS, clip predictions aggregated per subject).
  * Track and measure the bright region over time and turn the motion into
    numbers (Costamagna et al., 2026, open-source motion tracking in ultrasound
    video); coaxial process-camera features predict dross and plasma states in
    fusion laser cutting (Guerra et al., 2026); camera frames combined with
    process parameters (Asadi et al., 2026, DED melt-pool monitoring).
  * Compare the current clip with a reference "normal" state and describe the
    deviation (Ding et al., 2026: stress as a deviation from each person's
    resting baseline, fed to the LLM as "discrepancy tokens").
  * The trained video model decides; the LLM never classifies raw video, because
    zero-shot video MLLMs were unreliable and very sensitive to framing and
    lighting (Patel et al., 2026: 25-54 % accuracy, ~0 % on low-light videos).
  * The frame CNN + GRU itself is a standard sequence design chosen for this
    demo, not taken from one paper.

Real videos: any format OpenCV can read (.mp4, .avi). Synthetic demo videos are
written as .mp4 so you can watch them.
"""

from __future__ import annotations

import os

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

CLIP_FRAMES = 16      # frames per clip given to the model
FRAME_SIZE = 32       # frames are resized to FRAME_SIZE x FRAME_SIZE grey-scale
WINDOW = 4            # frames per window for the temporal statistics


# ---------------------------------------------------------------- loading
def load_video(path: str, n_frames: int = 2 * CLIP_FRAMES, size: int = FRAME_SIZE) -> np.ndarray:
    """Read a video and return n_frames evenly spaced grey-scale frames,
    shape (n_frames, size, size), float32 in [0, 1].

    Evenly spaced sampling gives a fixed frame rate regardless of the camera's
    own rate (Liu W. et al. used 8 FPS). For long jobs, cut the video
    into one file per job or per contour first.
    """
    if path.endswith(".npy"):
        frames = np.load(path)
    else:
        import cv2
        cap = cv2.VideoCapture(path)
        frames = []
        while True:
            ok, f = cap.read()
            if not ok:
                break
            frames.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) if f.ndim == 3 else f)
        cap.release()
        if not frames:
            raise ValueError(f"could not read any frames from {path}")
        frames = np.stack(frames)
    idx = np.linspace(0, len(frames) - 1, n_frames).round().astype(int)
    frames = frames[idx].astype(np.float32)
    if frames.shape[1:] != (size, size):
        import cv2
        frames = np.stack([cv2.resize(f, (size, size), interpolation=cv2.INTER_AREA) for f in frames])
    if frames.max() > 1.5:
        frames /= 255.0
    return frames


def to_clips(frames: np.ndarray, clip_frames: int = CLIP_FRAMES) -> np.ndarray:
    """(T, H, W) -> (n_clips, clip_frames, H, W), non-overlapping."""
    n = len(frames) // clip_frames
    return frames[: n * clip_frames].reshape(n, clip_frames, *frames.shape[1:])


# ---------------------------------------------------------------- explainable temporal statistics
SIGNALS = ["brightness", "glow_area", "glow_x", "glow_y"]


def frame_signals(frames: np.ndarray) -> np.ndarray:
    """Per-frame signals, shape (T, 4): mean brightness, share of bright pixels,
    and the bright region's centre (x, y as a fraction of the frame)."""
    T, H, W = frames.shape
    out = np.zeros((T, 4), np.float32)
    yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
    for t, f in enumerate(frames):
        thr = f.mean() + 1.5 * f.std()
        m = f > thr
        out[t, 0] = f.mean()
        out[t, 1] = m.mean()
        if m.any():
            out[t, 2], out[t, 3] = xx[m].mean(), yy[m].mean()
        else:
            out[t, 2] = out[t, 3] = 0.5
    return out


def temporal_features(frames: np.ndarray, window: int = WINDOW) -> dict:
    """Window statistics turned into named numbers:
      <signal>_mean     average level
      <signal>_jitter   average std inside short windows (fast fluctuation)
      <signal>_trend    change from the first to the last window (slow drift)
    """
    s = frame_signals(frames)
    n = len(s) // window
    w = s[: n * window].reshape(n, window, -1)
    w_mean, w_std = w.mean(1), w.std(1)
    feats = {}
    for i, name in enumerate(SIGNALS):
        feats[f"{name}_mean"] = float(s[:, i].mean())
        feats[f"{name}_jitter"] = float(w_std[:, i].mean())
        feats[f"{name}_trend"] = float(w_mean[-1, i] - w_mean[0, i])
    return feats


class VideoEvidence:
    """Reference comparison (after Ding et al., 2026): learn what 'ok' cuts look like
    and describe only the signals that are outside the normal range."""

    def fit(self, videos: list[np.ndarray], labels: list[str]):
        ok = [temporal_features(v) for v, l in zip(videos, labels) if l == "ok"]
        keys = ok[0].keys()
        self.ref = {k: (float(np.median([f[k] for f in ok])),
                        float(np.subtract(*np.percentile([f[k] for f in ok], [90, 10]))) + 1e-6) for k in keys}
        return self

    def describe(self, frames: np.ndarray, z_limit: float = 1.5) -> list[dict]:
        feats = temporal_features(frames)
        out = []
        for k, v in feats.items():
            med, spread = self.ref[k]
            z = (v - med) / spread
            if abs(z) > z_limit:
                out.append({"signal": k, "value": round(v, 3), "normal": round(med, 3),
                            "level": "high" if z > 0 else "low", "z": round(z, 1)})
        return sorted(out, key=lambda d: -abs(d["z"]))[:4]


# ---------------------------------------------------------------- learned model
class CNNGRU(nn.Module):
    """Shared 2D CNN on every frame, then a GRU over time (a light alternative
    to a 3D CNN; swap in a pretrained frame encoder for real videos)."""

    def __init__(self, n_classes: int, hidden: int = 64):
        super().__init__()
        self.frame_enc = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.AdaptiveAvgPool2d(2),
            nn.Flatten(),
        )
        self.gru = nn.GRU(32 * 4, hidden, batch_first=True)
        self.head = nn.Sequential(nn.Dropout(0.2), nn.Linear(hidden, n_classes))

    def forward(self, x):                       # x: (B, T, H, W)
        B, T, H, W = x.shape
        f = self.frame_enc(x.reshape(B * T, 1, H, W)).reshape(B, T, -1)
        _, h = self.gru(f)
        return self.head(h[-1])


class DefectVideoModel:
    def __init__(self, classes: list[str], device: str | None = None, seed: int = 0):
        torch.manual_seed(seed)
        self.classes = list(classes)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.net = CNNGRU(len(classes)).to(self.device)

    def fit(self, videos: list[np.ndarray], labels: list[str], epochs: int = 8, batch_size: int = 32, lr: float = 2e-3):
        # every clip of a video gets the video's label
        clips, ys = [], []
        for v, l in zip(videos, labels):
            c = to_clips(v)
            clips.append(c)
            ys += [self.classes.index(l)] * len(c)
        x = torch.tensor(np.concatenate(clips), dtype=torch.float32)
        y = torch.tensor(ys)
        opt = torch.optim.AdamW(self.net.parameters(), lr=lr, weight_decay=1e-4)
        self.net.train()
        for ep in range(epochs):
            perm = torch.randperm(len(x))
            total = 0.0
            for i in range(0, len(x), batch_size):
                idx = perm[i:i + batch_size]
                xb = x[idx].to(self.device)
                if np.random.rand() < 0.5:      # augmentation: mirror left-right
                    xb = torch.flip(xb, dims=[3])
                loss = F.cross_entropy(self.net(xb), y[idx].to(self.device))
                opt.zero_grad()
                loss.backward()
                opt.step()
                total += loss.item() * len(idx)
            print(f"  video epoch {ep + 1}/{epochs}  loss {total / len(x):.3f}")
        return self

    @torch.no_grad()
    def predict_proba(self, videos: list[np.ndarray]) -> np.ndarray:
        """Average the clip probabilities of each video (Liu W. et al., 2026)."""
        self.net.eval()
        out = []
        for v in videos:
            x = torch.tensor(to_clips(v), dtype=torch.float32, device=self.device)
            out.append(F.softmax(self.net(x), dim=1).mean(0).cpu().numpy())
        return np.stack(out)

    @torch.no_grad()
    def clip_labels(self, frames: np.ndarray) -> list[str]:
        """Label of each clip, so the report can say when in the job it went wrong."""
        self.net.eval()
        x = torch.tensor(to_clips(frames), dtype=torch.float32, device=self.device)
        return [self.classes[i] for i in self.net(x).argmax(1).cpu().numpy()]

    def save(self, path: str):
        torch.save({"classes": self.classes, "state": self.net.state_dict()}, path)


# ---------------------------------------------------------------- synthetic demo videos
def render_process_video(defect: str, n_frames: int = 2 * CLIP_FRAMES, size: int = FRAME_SIZE,
                         seed: int = 0) -> np.ndarray:
    """A grey-scale 'process camera' video of the glowing cutting front.
    Each defect has a typical behaviour over time; a single frame is often
    ambiguous, which is why a temporal model is needed. PLACEHOLDER for real
    TruLaser process videos."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size].astype(float)
    sev = rng.uniform(0.15, 1.0)
    cx, cy, r, amp = size / 2, size / 2, size / 7, 170.0
    phase, period = rng.uniform(0, 6), rng.uniform(3, 6)
    sparks = []                       # [x, y, vy]
    frames = []
    for t in range(n_frames):
        f = 30 + rng.normal(0, 10, (size, size))
        x0, y0, rad, a = cx + rng.normal(0, 0.6), cy + rng.normal(0, 0.6), r, amp
        if defect == "rough_striations":
            a *= 1 + 0.45 * sev * np.sin(2 * np.pi * t / period + phase)
        elif defect == "burn_overheating":
            rad *= 1 + 0.9 * sev * t / n_frames
        elif defect == "bevel_deviation":
            x0 += sev * 0.35 * size * (t / n_frames - 0.5)
        if defect in ("dross", "incomplete_cut") and rng.random() < 0.5 * sev + 0.1:
            vy = 2.0 if defect == "dross" else -2.0
            sparks.append([x0 + rng.normal(0, 2), y0, vy * rng.uniform(0.7, 1.3)])
        f += a * np.exp(-((xx - x0) ** 2 + (yy - y0) ** 2) / (2 * rad ** 2))
        for s in sparks:
            s[1] += s[2]
            f += 120 * np.exp(-((xx - s[0]) ** 2 + (yy - s[1]) ** 2) / 2.0)
        sparks = [s for s in sparks if 0 <= s[1] < size]
        frames.append(f)
    v = np.stack(frames) * rng.uniform(0.75, 1.25)
    return np.clip(v, 0, 255).astype(np.uint8)


def write_video(frames: np.ndarray, path: str, fps: int = 8):
    """Save (T, H, W) uint8 frames as .mp4 (or .npy if OpenCV is missing)."""
    try:
        import cv2
    except ImportError:
        np.save(os.path.splitext(path)[0] + ".npy", frames)
        return os.path.splitext(path)[0] + ".npy"
    h, w = frames.shape[1:]
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h), isColor=False)
    for f in frames:
        out.write(f)
    out.release()
    return path
