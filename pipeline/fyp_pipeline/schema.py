"""Shared definitions: machine-table columns, defect classes and allowed actions.

Edit this file first when you get the real TruLaser database export: rename the
columns in MACHINE_COLUMNS to match your table and adjust the defect list to the
categories your engineers actually record.
"""

# Columns expected in the machine-database table (one row per cutting job).
# type: "num" (number), "cat" (category / text label)
MACHINE_COLUMNS = {
    "job_id": "id",
    "material": "cat",            # e.g. mild_steel, stainless, aluminium
    "thickness_mm": "num",
    "assist_gas": "cat",          # O2 or N2
    "laser_power_w": "num",
    "cutting_speed_mm_min": "num",
    "gas_pressure_bar": "num",
    "focus_position_mm": "num",
    "nozzle_standoff_mm": "num",
    "nozzle_diameter_mm": "num",
    "nozzle_hours": "num",        # hours since the nozzle was changed
    "lens_hours": "num",          # hours since the protective glass was cleaned/changed
    "bevel_angle_deg": "num",     # 0 = straight cut, >0 = bevel cut
    "alarm_code": "cat",          # last machine alarm during the job ("none" if no alarm)
}

FEATURE_COLUMNS = [c for c, t in MACHINE_COLUMNS.items() if t in ("num", "cat")]
NUMERIC_COLUMNS = [c for c, t in MACHINE_COLUMNS.items() if t == "num"]
CATEGORICAL_COLUMNS = [c for c, t in MACHINE_COLUMNS.items() if t == "cat"]

# Parameters the optimiser (and the LLM) are allowed to recommend changing.
# Everything else (material, thickness, bevel angle) is fixed by the job.
ADJUSTABLE_PARAMETERS = {
    "laser_power_w": (1000, 6000),
    "cutting_speed_mm_min": (300, 12000),
    "gas_pressure_bar": (0.5, 20.0),
    "focus_position_mm": (-8.0, 4.0),
    "nozzle_standoff_mm": (0.5, 2.0),
}

# Cut-quality defect classes. "ok" means no defect.
DEFECT_CLASSES = [
    "ok",
    "dross",               # molten metal re-solidified on the bottom edge
    "rough_striations",    # deep / irregular drag lines on the cut face
    "incomplete_cut",      # loss of cut, the beam did not go through
    "burn_overheating",    # burn-out, overheating, wide kerf, discolouration
    "bevel_deviation",     # bevel angle or bevel face out of tolerance
]

# Maintenance / process actions the report may recommend (whitelist, after
# Shi et al., "Entropy-conflict-aware dual-model fusion with LLM reporting").
ALLOWED_ACTIONS = [
    "adjust_cutting_speed",
    "adjust_laser_power",
    "adjust_gas_pressure",
    "adjust_focus_position",
    "adjust_nozzle_standoff",
    "inspect_or_replace_nozzle",
    "clean_or_replace_protective_glass",
    "recalibrate_bevel_axis",
    "check_material_quality",
    "re_measure_part",
    "manual_review_by_engineer",
]

# When the system is unsure (label "unknown"), only these conservative actions
# are allowed.
CONSERVATIVE_ACTIONS = ["re_measure_part", "inspect_or_replace_nozzle", "manual_review_by_engineer"]

UNKNOWN = "unknown"
