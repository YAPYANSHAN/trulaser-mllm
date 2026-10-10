"""Stage 2b - specialist image model for cut-part photos (PyTorch).

Why a trained model and not only a VLM? Several papers in the review found that
zero-shot vision-language models are unreliable on subtle defects, e.g.
  * Kukuljan et al., "Illusion of competence", Sci. Rep., 2026 (GPT-4o near random
    zero-shot; a small head on foundation features did far better)
  * Haupt et al., zero-shot MLLMs vs a trained CNN, Sci. Rep., 2026
  * Abdelkader, "VLMs for automated quality control", Sci. Rep., 2026 (local VLMs
    averaged ~25 % on industrial parts)
So the trained model decides "what defect", and the LLM explains "why" with the
other evidence (small-model-centred design, Yan et al., Chin. J. Mech. Eng., 2026).

Two backbones:
  * "small_cnn": trains from scratch in seconds on CPU (used in the demo)
  * "resnet18":  ImageNet-pretrained torchvision model, better for real photos
"""

from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class SmallCNN(nn.Module):
    def __init__(self, n_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.AdaptiveAvgPool2d(4),
        )
        self.head = nn.Sequential(nn.Flatten(), nn.Dropout(0.2), nn.Linear(64 * 16, n_classes))

    def forward(self, x):
        return self.head(self.features(x))


def build_backbone(name: str, n_classes: int) -> nn.Module:
    if name == "small_cnn":
        return SmallCNN(n_classes)
    if name == "resnet18":
        import torchvision
        m = torchvision.models.resnet18(weights="IMAGENET1K_V1")
        m.conv1 = nn.Conv2d(1, 64, 7, 2, 3, bias=False)  # grey-scale input
        m.fc = nn.Linear(m.fc.in_features, n_classes)
        return m
    raise ValueError(name)


class DefectImageModel:
    def __init__(self, classes: list[str], backbone: str = "small_cnn", device: str | None = None, seed: int = 0):
        torch.manual_seed(seed)
        self.classes = list(classes)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.net = build_backbone(backbone, len(classes)).to(self.device)

    def fit(self, images: np.ndarray, labels: list[str], epochs: int = 8, batch_size: int = 64, lr: float = 2e-3):
        x = torch.tensor(images[:, None], dtype=torch.float32)
        y = torch.tensor([self.classes.index(l) for l in labels])
        opt = torch.optim.AdamW(self.net.parameters(), lr=lr, weight_decay=1e-4)
        self.net.train()
        for ep in range(epochs):
            perm = torch.randperm(len(x))
            total = 0.0
            for i in range(0, len(x), batch_size):
                idx = perm[i:i + batch_size]
                xb = x[idx].to(self.device)
                if np.random.rand() < 0.5:          # simple augmentation: horizontal flip
                    xb = torch.flip(xb, dims=[3])
                loss = F.cross_entropy(self.net(xb), y[idx].to(self.device))
                opt.zero_grad()
                loss.backward()
                opt.step()
                total += loss.item() * len(idx)
            print(f"  vision epoch {ep + 1}/{epochs}  loss {total / len(x):.3f}")
        return self

    @torch.no_grad()
    def predict_proba(self, images: np.ndarray) -> np.ndarray:
        self.net.eval()
        x = torch.tensor(images[:, None], dtype=torch.float32, device=self.device)
        return F.softmax(self.net(x), dim=1).cpu().numpy()

    def saliency_region(self, image: np.ndarray) -> str:
        """Which part of the photo drove the decision? Returned as plain words the
        LLM can quote (a lightweight stand-in for Grad-CAM)."""
        self.net.eval()
        x = torch.tensor(image[None, None], dtype=torch.float32, device=self.device, requires_grad=True)
        out = self.net(x)
        out[0, out.argmax()].backward()
        sal = x.grad.abs()[0, 0].cpu().numpy()
        h, w = sal.shape
        regions = {
            "top of the cut face": sal[: h // 3].mean(),
            "middle of the cut face": sal[h // 3: 2 * h // 3].mean(),
            "bottom edge": sal[2 * h // 3:].mean(),
        }
        side = "left side" if sal[:, : w // 2].mean() > sal[:, w // 2:].mean() * 1.3 else (
            "right side" if sal[:, w // 2:].mean() > sal[:, : w // 2].mean() * 1.3 else "across the width")
        return f"{max(regions, key=regions.get)}, {side}"

    def save(self, path: str):
        torch.save({"classes": self.classes, "state": self.net.state_dict()}, path)
