"""Stage 2a - specialist model for the machine-database table.

Two models:
  * DefectClassifier: predicts the defect class from process parameters.
    Gradient-boosted trees are the recommended first choice for small tabular
    datasets (Nguyen et al., "Toward trustworthy and explainable AI-driven
    industrial fault diagnosis: a data-to-deployment review", Results Eng., 2026).
  * QualitySurrogate: predicts measured quality (dross height, roughness) and is
    used by the optimiser, after Bhoir & Verma (ANN/GPR surrogate + NSGA-II,
    Discover Mech. Eng., 2026) and Rao & Vaneesha (digital-twin SCADA loop for a
    TRUMPF laser, Adv. Eng. Informatics, 2026).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder

from .schema import CATEGORICAL_COLUMNS, NUMERIC_COLUMNS

FEATURES = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS


def _preprocessor():
    return ColumnTransformer(
        [
            ("num", "passthrough", NUMERIC_COLUMNS),
            ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), CATEGORICAL_COLUMNS),
        ]
    )


class DefectClassifier:
    def __init__(self, seed: int = 0):
        cat_mask = [False] * len(NUMERIC_COLUMNS) + [True] * len(CATEGORICAL_COLUMNS)
        self.model = Pipeline(
            [
                ("prep", _preprocessor()),
                ("gbt", HistGradientBoostingClassifier(max_iter=300, learning_rate=0.06,
                                                       categorical_features=cat_mask, random_state=seed)),
            ]
        )
        self.classes_: list[str] = []
        self.reference_: pd.Series | None = None

    def fit(self, df: pd.DataFrame, y: pd.Series):
        self.model.fit(df[FEATURES], y)
        self.classes_ = list(self.model.classes_)
        # typical values, used for the per-job explanation below
        self.reference_ = pd.concat([df[NUMERIC_COLUMNS].median(), df[CATEGORICAL_COLUMNS].mode().iloc[0]])
        return self

    def predict_proba(self, df: pd.DataFrame) -> np.ndarray:
        return self.model.predict_proba(df[FEATURES])

    def explain(self, row: pd.DataFrame, top_k: int = 4) -> list[dict]:
        """Occlusion attribution: how much does the predicted class probability drop
        when one feature is replaced by its typical value? Bigger drop = more evidence."""
        p = self.predict_proba(row)[0]
        k = int(np.argmax(p))
        out = []
        for c in FEATURES:
            alt = row.copy()
            alt[c] = self.reference_[c]
            drop = p[k] - self.predict_proba(alt)[0][k]
            out.append({"feature": c, "value": row.iloc[0][c], "typical": self.reference_[c], "importance": float(drop)})
        out.sort(key=lambda d: -d["importance"])
        return out[:top_k]


class QualitySurrogate:
    """One regressor per quality target, e.g. dross_height_mm, roughness_ra_um."""

    def __init__(self, targets=("dross_height_mm", "roughness_ra_um"), seed: int = 0):
        self.targets = list(targets)
        cat_mask = [False] * len(NUMERIC_COLUMNS) + [True] * len(CATEGORICAL_COLUMNS)
        self.models = {
            t: Pipeline([("prep", _preprocessor()),
                         ("gbr", HistGradientBoostingRegressor(max_iter=300, categorical_features=cat_mask,
                                                               random_state=seed))])
            for t in self.targets
        }

    def fit(self, df: pd.DataFrame):
        for t, m in self.models.items():
            m.fit(df[FEATURES], df[t])
        return self

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame({t: m.predict(df[FEATURES]) for t, m in self.models.items()}, index=df.index)
