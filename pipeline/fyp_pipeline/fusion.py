"""Stage 4 - decision-level fusion of the table, image and (if present) video models.

Follows Shi, Gao & Liu, "Entropy-conflict-aware dual-model fusion with LLM
reporting for wind turbine fault diagnosis", Results in Engineering, 2026:
  1. weight each branch by its confidence (low entropy = more weight)
  2. measure how much the branches disagree (conflict)
  3. if confidence is too low or conflict too high, answer "unknown" and only
     allow conservative actions (re-measure, inspect, engineer review)
This abstain-when-unsure rule is also recommended by Fedynyshyn et al. (2026)
and the EBRB-LLM paper (Liu et al., 2026).
"""

from __future__ import annotations

import numpy as np

from .schema import UNKNOWN


def _entropy(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 1e-9, 1)
    return -(p * np.log(p)).sum(-1) / np.log(p.shape[-1])   # normalised to [0, 1]


def _temper(p: np.ndarray, t: float) -> np.ndarray:
    q = np.exp(np.log(np.clip(p, 1e-9, 1)) / t)
    return q / q.sum(-1, keepdims=True)


def _fit_temperature(p: np.ndarray, y_idx: np.ndarray) -> float:
    grid = np.exp(np.linspace(np.log(0.3), np.log(5), 40))
    nll = [-np.log(_temper(p, t)[np.arange(len(y_idx)), y_idx] + 1e-9).mean() for t in grid]
    return float(grid[int(np.argmin(nll))])


class ConflictAwareFusion:
    """Fuses any number of branches, e.g. {"table": p, "image": p, "video": p}.
    Each branch is an (n_samples, n_classes) probability array."""

    def __init__(self, classes: list[str], min_confidence: float = 0.5, max_conflict: float = 0.6):
        self.classes = list(classes)
        self.temps: dict[str, float] = {}   # temperature per branch, fitted in tune()
        self.min_confidence = min_confidence
        self.max_conflict = max_conflict

    def combine(self, branches: dict[str, np.ndarray]):
        """Returns fused probabilities, confidence weights (one column per branch)
        and conflict per sample. Conflict is the largest disagreement between
        any two branches."""
        ps = {k: _temper(p, self.temps.get(k, 1.0)) for k, p in branches.items()}
        w = np.stack([1 - _entropy(p) for p in ps.values()], 1)
        w = w / (w.sum(1, keepdims=True) + 1e-9)
        fused = sum(w[:, i:i + 1] * p for i, p in enumerate(ps.values()))
        names = list(ps)
        conflict = np.zeros(len(fused))
        for i in range(len(names)):
            for j in range(i + 1, len(names)):        # 0 = agree, 1 = fully disagree
                conflict = np.maximum(conflict, 1 - np.sqrt(ps[names[i]] * ps[names[j]]).sum(1))
        return fused, w, conflict

    def decide(self, branches: dict[str, np.ndarray]) -> list[dict]:
        fused, weights, conflict = self.combine(branches)
        out = []
        for i in range(len(fused)):
            k = int(fused[i].argmax())
            label = self.classes[k]
            reason = None
            if fused[i, k] < self.min_confidence:
                label, reason = UNKNOWN, f"low confidence ({fused[i, k]:.2f})"
            elif conflict[i] > self.max_conflict:
                label, reason = UNKNOWN, f"the {' / '.join(branches)} models disagree (conflict {conflict[i]:.2f})"
            d = {
                "label": label,
                "best_guess": self.classes[k],
                "confidence": float(fused[i, k]),
                "conflict": float(conflict[i]),
            }
            for j, (name, p) in enumerate(branches.items()):
                d[f"weight_{name}"] = float(weights[i, j])
                d[f"{name}_says"] = self.classes[int(p[i].argmax())]
            d["abstain_reason"] = reason
            d["probabilities"] = {c: round(float(v), 3) for c, v in zip(self.classes, fused[i])}
            out.append(d)
        return out

    def tune(self, branches: dict[str, np.ndarray], y_true, min_coverage: float = 0.85):
        """Pick thresholds on a validation set: best accuracy on accepted cases
        while still answering at least `min_coverage` of them."""
        # 1) calibrate each branch so its confidence is honest (temperature scaling)
        y_idx = np.array([self.classes.index(t) for t in y_true])
        self.temps = {k: _fit_temperature(p, y_idx) for k, p in branches.items()}
        # 2) choose abstention thresholds
        best = (-1, self.min_confidence, self.max_conflict)
        for mc in np.arange(0.3, 0.8, 0.05):
            for mx in np.arange(0.3, 1.01, 0.05):
                self.min_confidence, self.max_conflict = mc, mx
                d = self.decide(branches)
                acc_mask = np.array([x["label"] != UNKNOWN for x in d])
                if acc_mask.mean() < min_coverage:
                    continue
                acc = np.mean([x["label"] == t for x, t, m in zip(d, y_true, acc_mask) if m])
                if acc > best[0]:
                    best = (acc, mc, mx)
        _, self.min_confidence, self.max_conflict = best
        return self
