"""Stage 6 - process optimisation: suggest better parameters with the surrogate.

The LLM must not invent parameter values. Instead it calls this optimiser and
explains the result (tool-use pattern from Bhoir & Verma, surrogate ANN +
NSGA-II for sheet-metal blanking, 2026; and the closed loop of Rao & Vaneesha,
digital twin for TRUMPF laser machining, 2026). Guerra et al. (2026) show speed
is the main lever for dross/productivity in fusion cutting, so cycle time is kept
as a second objective.

This version uses random search inside the allowed envelope, which is easy to
read. For a proper multi-objective Pareto front, swap in NSGA-II from `pymoo`.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .schema import ADJUSTABLE_PARAMETERS


class ParameterOptimiser:
    def __init__(self, classifier, surrogate, max_change: float = 0.3, n_candidates: int = 1500, seed: int = 0):
        self.clf, self.sur = classifier, surrogate
        self.max_change = max_change
        self.n = n_candidates
        self.rng = np.random.default_rng(seed)

    def _score(self, cand: pd.DataFrame, base_speed: float) -> np.ndarray:
        p = self.clf.predict_proba(cand)
        p_ok = p[:, self.clf.classes_.index("ok")]
        q = self.sur.predict(cand)
        slow_penalty = np.clip(1 - cand["cutting_speed_mm_min"].values / base_speed, 0, None)
        # lower is better: defect risk + quality + small productivity penalty
        return (1 - p_ok) + 0.5 * q["dross_height_mm"].values + 0.02 * q["roughness_ra_um"].values + 0.3 * slow_penalty

    def recommend(self, row: pd.DataFrame, directions: dict | None = None) -> dict:
        """directions: {parameter: +1 (may only increase) or -1 (may only decrease)}.
        Comes from the knowledge graph (e.g. cause power_too_low -> laser_power_w +1),
        so the data-driven search cannot suggest physically wrong moves. Parameters
        not listed stay fixed. If directions is None every parameter may move."""
        base = row.iloc[0]
        cand = pd.concat([row] * self.n, ignore_index=True)
        for c, (lo, hi) in ADJUSTABLE_PARAMETERS.items():
            if directions is not None and c not in directions:
                continue
            if c == "focus_position_mm" or c == "nozzle_standoff_mm":
                step = self.rng.uniform(-1.5, 1.5, self.n) * (1 if c == "focus_position_mm" else 0.3)
            else:
                step = base[c] * self.rng.uniform(-self.max_change, self.max_change, self.n)
            if directions is not None:
                step = np.abs(step) * directions[c]
            cand[c] = np.clip(base[c] + step, lo, hi)
        cand.iloc[0] = row.iloc[0]                       # keep "no change" as a candidate
        scores = self._score(cand, base["cutting_speed_mm_min"])
        best = cand.iloc[int(scores.argmin())]
        before = self.sur.predict(row).iloc[0]
        after = self.sur.predict(best.to_frame().T.astype(row.dtypes.to_dict())).iloc[0]
        p_before = self.clf.predict_proba(row)[0][self.clf.classes_.index("ok")]
        p_after = self.clf.predict_proba(best.to_frame().T.astype(row.dtypes.to_dict()))[0][self.clf.classes_.index("ok")]
        changes = {}
        for c in ADJUSTABLE_PARAMETERS:
            if abs(best[c] - base[c]) > 1e-6 and abs(best[c] - base[c]) / (abs(base[c]) + 1e-6) > 0.02:
                changes[c] = {"from": round(float(base[c]), 2), "to": round(float(best[c]), 2)}
        return {
            "changes": changes,
            "predicted_before": {"p_ok": round(float(p_before), 3), **{k: round(float(v), 3) for k, v in before.items()}},
            "predicted_after": {"p_ok": round(float(p_after), 3), **{k: round(float(v), 3) for k, v in after.items()}},
            "searched_parameters": sorted(directions) if directions is not None else "all",
            "note": "Model predictions only. Validate with a test cut before using in production.",
        }
