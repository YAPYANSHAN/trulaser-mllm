"""Stage 7 - evaluation.

Metrics chosen from the reviewed papers:
  * accuracy and macro-F1 (class imbalance aware), confusion matrix
  * expected calibration error (ECE) - is the confidence honest?
  * coverage / selective accuracy for the "unknown" option (Shi et al., 2026)
  * modality ablation: table only vs image only vs fused (Yang et al., 2026;
    Wu et al., digital twin substation fusion, Nat. Commun., 2026)
  * report checks: schema validity, evidence faithfulness, allowed actions
    (Shi et al. EFR/MRC; Zhang et al. hallucination rate, 2026)
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

from .schema import UNKNOWN


def ece(probs: np.ndarray, y_idx: np.ndarray, bins: int = 10) -> float:
    conf, pred = probs.max(1), probs.argmax(1)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any():
            e += m.mean() * abs((pred[m] == y_idx[m]).mean() - conf[m].mean())
    return float(e)


def classification_metrics(probs: np.ndarray, y_true: list[str], classes: list[str]) -> dict:
    y_idx = np.array([classes.index(t) for t in y_true])
    pred = probs.argmax(1)
    return {
        "accuracy": round(accuracy_score(y_idx, pred), 4),
        "macro_f1": round(f1_score(y_idx, pred, average="macro"), 4),
        "ece": round(ece(probs, y_idx), 4),
    }


def selective_metrics(decisions: list[dict], y_true: list[str]) -> dict:
    answered = [(d["label"], t) for d, t in zip(decisions, y_true) if d["label"] != UNKNOWN]
    cov = len(answered) / len(y_true)
    acc = np.mean([p == t for p, t in answered]) if answered else float("nan")
    wrong_unknown = np.mean([d["best_guess"] != t for d, t in zip(decisions, y_true) if d["label"] == UNKNOWN]) \
        if cov < 1 else float("nan")
    return {"coverage": round(cov, 4), "selective_accuracy": round(float(acc), 4),
            "share_of_abstentions_that_were_wrong_guesses": round(float(wrong_unknown), 4)}


def confusion(y_true, y_pred, classes) -> str:
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    w = max(len(c) for c in classes)
    lines = [" " * (w + 2) + " ".join(c[:6].rjust(6) for c in classes)]
    for c, row in zip(classes, cm):
        lines.append(c.rjust(w) + "  " + " ".join(str(v).rjust(6) for v in row))
    return "\n".join(lines)


def report_checks(results: list[dict]) -> dict:
    """results: outputs of reasoner.reason()."""
    n = len(results)
    valid = sum(1 for r in results if r["report"] is not None and not r["problems"])
    cited = total = 0
    for r in results:
        for c in (r["report"] or {}).get("root_causes", []):
            total += 1
            cited += bool(c.get("evidence_ids"))
    return {
        "reports": n,
        "schema_and_rule_valid_rate": round(valid / max(1, n), 4),
        "root_causes_with_evidence_rate": round(cited / max(1, total), 4),
        "mean_attempts": round(float(np.mean([r["attempts"] for r in results])), 2),
    }
