"""Turn raw numbers into qualitative evidence ("gas pressure is LOW for this
material and thickness") that the knowledge graph and the LLM can use.

The reference is the typical value for the same material and thickness in the
historical data, i.e. an empirical cutting table. Swap in the real TRUMPF
cutting-table values when you have them.
"""

from __future__ import annotations

import pandas as pd

RELATIVE = ["laser_power_w", "cutting_speed_mm_min", "gas_pressure_bar"]   # compare as ratio
ABSOLUTE = {"focus_position_mm": 0.8, "nozzle_standoff_mm": 0.25}          # compare as difference
WEAR = ["nozzle_hours", "lens_hours"]                                      # high if above 85th percentile


class EvidenceProfiler:
    def __init__(self, ratio_band: float = 0.15):
        self.ratio_band = ratio_band

    def fit(self, df: pd.DataFrame):
        cols = RELATIVE + list(ABSOLUTE)
        self.table_ = df.groupby(["material", "thickness_mm"])[cols].median()
        self.global_ = df[cols].median()
        self.wear_limits_ = df[WEAR].quantile(0.85)
        return self

    def reference(self, row: pd.Series) -> pd.Series:
        key = (row["material"], row["thickness_mm"])
        return self.table_.loc[key] if key in self.table_.index else self.global_

    def profile(self, row: pd.Series) -> dict:
        """Return {"gas_pressure_bar": "low", ...} plus the numbers behind it."""
        ref = self.reference(row)
        levels, details = {}, {}
        for c in RELATIVE:
            r = row[c] / ref[c]
            levels[c] = "high" if r > 1 + self.ratio_band else "low" if r < 1 - self.ratio_band else "normal"
            details[c] = f"{row[c]:.1f} vs typical {ref[c]:.1f} ({(r - 1) * 100:+.0f}%)"
        for c, band in ABSOLUTE.items():
            d = row[c] - ref[c]
            levels[c] = "high" if d > band else "low" if d < -band else "normal"
            details[c] = f"{row[c]:.2f} vs typical {ref[c]:.2f} ({d:+.2f})"
        for c in WEAR:
            levels[c] = "high" if row[c] > self.wear_limits_[c] else "normal"
            details[c] = f"{row[c]:.0f} h (limit used: {self.wear_limits_[c]:.0f} h)"
        levels["bevel_angle_deg"] = "high" if row["bevel_angle_deg"] >= 30 else "normal"
        details["bevel_angle_deg"] = f"{row['bevel_angle_deg']:.0f} deg"
        levels["alarm_code"] = str(row["alarm_code"])
        details["alarm_code"] = str(row["alarm_code"])
        return {"levels": levels, "details": details}
