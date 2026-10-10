"""Synthetic TruLaser-like data so the whole pipeline runs before real data arrives.

Nothing here is real TRUMPF data. The rules are simplified laser-cutting physics,
used only to test the code:
  * dross grows when gas pressure is too low or speed too high
    (Guerra et al., "Hierarchical vision-driven automatic control of quality and
    speed in fusion laser cutting", Opt. Laser Technol., 2026)
  * too little power or too much speed gives loss of cut (same source)
  * too slow with high power overheats the kerf; worn nozzles and dirty
    protective glass degrade the cut face
Replace generate_jobs()/render_edge_image() with your real export and photos.
"""

from __future__ import annotations

import os
import numpy as np
import pandas as pd
from PIL import Image

from .schema import DEFECT_CLASSES

MATERIALS = {
    # material: (assist gas, nominal pressure bar, speed constant)
    "mild_steel": ("O2", 0.8, 9000.0),
    "stainless": ("N2", 16.0, 11000.0),
    "aluminium": ("N2", 14.0, 12000.0),
}


def nominal_recipe(material: str, thickness: float) -> dict:
    """A made-up 'cutting table' giving the ideal parameters for a job."""
    gas, pressure, k = MATERIALS[material]
    power = min(6000.0, 1500.0 + 300.0 * thickness)
    speed = k * 2.0 / (thickness + 1.0)
    focus = -0.4 * thickness if gas == "N2" else 0.1 * thickness
    return {
        "assist_gas": gas,
        "laser_power_w": power,
        "cutting_speed_mm_min": speed,
        "gas_pressure_bar": pressure,
        "focus_position_mm": float(np.clip(focus, -8, 4)),
        "nozzle_standoff_mm": 1.0,
    }


def _defect_scores(row: dict, nom: dict) -> dict:
    """Physics-inspired risk score for each defect class."""
    speed_ratio = row["cutting_speed_mm_min"] / nom["cutting_speed_mm_min"]
    power_ratio = row["laser_power_w"] / nom["laser_power_w"]
    press_ratio = row["gas_pressure_bar"] / nom["gas_pressure_bar"]
    focus_err = abs(row["focus_position_mm"] - nom["focus_position_mm"])
    standoff_err = abs(row["nozzle_standoff_mm"] - 1.0)
    return {
        "ok": 1.2,
        "dross": 4.0 * max(0, 1 - press_ratio) + 2.5 * max(0, speed_ratio - 1.1) + 0.4 * focus_err,
        "rough_striations": 0.004 * row["nozzle_hours"] + 0.6 * focus_err + 2.0 * max(0, 0.8 - speed_ratio),
        "incomplete_cut": 5.0 * max(0, speed_ratio / power_ratio - 1.35) + 0.01 * row["lens_hours"],
        "burn_overheating": 4.0 * max(0, 0.7 - speed_ratio) * power_ratio + (0.8 if row["alarm_code"] == "E_TEMP" else 0),
        "bevel_deviation": (0.08 * row["bevel_angle_deg"]) * (1 + 3 * standoff_err)
        + (1.5 if row["alarm_code"] == "E_AXIS" else 0),
    }


def generate_jobs(n: int = 1500, seed: int = 0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        material = rng.choice(list(MATERIALS))
        thickness = float(rng.choice([2, 3, 5, 8, 10, 12, 15, 20]))
        nom = nominal_recipe(material, thickness)
        row = {
            "job_id": f"J{i:05d}",
            "material": material,
            "thickness_mm": thickness,
            "assist_gas": nom["assist_gas"],
            "laser_power_w": nom["laser_power_w"] * rng.normal(1.0, 0.12),
            "cutting_speed_mm_min": nom["cutting_speed_mm_min"] * rng.lognormal(0, 0.25),
            "gas_pressure_bar": nom["gas_pressure_bar"] * rng.normal(1.0, 0.18),
            "focus_position_mm": nom["focus_position_mm"] + rng.normal(0, 0.8),
            "nozzle_standoff_mm": float(np.clip(rng.normal(1.0, 0.2), 0.5, 2.0)),
            "nozzle_diameter_mm": float(rng.choice([1.4, 1.7, 2.0, 2.3])),
            "nozzle_hours": float(rng.exponential(60)),
            "lens_hours": float(rng.exponential(40)),
            "bevel_angle_deg": float(rng.choice([0, 0, 0, 15, 30, 45])),
            "alarm_code": rng.choice(["none"] * 12 + ["E_TEMP", "E_AXIS", "E_GAS"]),
        }
        row["laser_power_w"] = float(np.clip(row["laser_power_w"], 1000, 6000))
        row["gas_pressure_bar"] = float(np.clip(row["gas_pressure_bar"], 0.3, 22))
        scores = _defect_scores(row, nom)
        logits = np.array([scores[c] for c in DEFECT_CLASSES]) * 3.0
        p = np.exp(logits - logits.max())
        p /= p.sum()
        row["defect"] = DEFECT_CLASSES[int(rng.choice(len(p), p=p))]
        # Measured quality numbers (what a technician would record after the cut).
        row["dross_height_mm"] = round(max(0.0, 0.05 + 0.3 * scores["dross"] + rng.normal(0, 0.03)), 3)
        row["roughness_ra_um"] = round(max(0.5, 2.0 + 0.4 * thickness + 3 * scores["rough_striations"] + rng.normal(0, 0.5)), 2)
        rows.append(row)
    return pd.DataFrame(rows)


def render_edge_image(defect: str, size: int = 64, seed: int = 0) -> Image.Image:
    """Draw a grey-scale 'photo' of a cut edge with a texture typical of the defect."""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size].astype(float)
    base = 150 + 8 * np.sin(x / 2.5 + rng.uniform(0, 6)) + rng.normal(0, 6, (size, size))
    img = base.copy()
    if defect == "dross":
        for _ in range(rng.integers(4, 9)):
            cx, r = rng.uniform(0, size), rng.uniform(2, 5)
            img -= 70 * np.exp(-((x - cx) ** 2 + (y - size + 3) ** 2) / (2 * r ** 2))
    elif defect == "rough_striations":
        img += 35 * np.sin(x / 1.3 + 0.15 * y + rng.uniform(0, 6)) * (y / size)
    elif defect == "incomplete_cut":
        # lower part of the edge is uncut (dark, smooth)
        img[int(size * rng.uniform(0.45, 0.6)):, :] = 60
    elif defect == "burn_overheating":
        img -= 55 * np.exp(-((x - size / 2) ** 2 + (y - size / 2) ** 2) / (2 * (size / 3.5) ** 2))
    elif defect == "bevel_deviation":
        img[x > (size / 2 + (y - size / 2) * rng.uniform(0.5, 0.9))] -= 50
    # real defects vary in severity, and photos vary in lighting: blend the defect
    # pattern with a clean edge so mild cases are genuinely hard to see
    severity = rng.uniform(0.08, 1.0)
    img = base + severity * (img - base)
    img = img * rng.uniform(0.8, 1.2) + rng.normal(0, 14, (size, size))
    img = np.clip(img, 0, 255).astype(np.uint8)
    return Image.fromarray(img, mode="L")


SYNTHETIC_MANUAL = """\
# Troubleshooting guide (PLACEHOLDER - replace with the real TRUMPF TruLaser 3000 documentation)

## Dross on the bottom edge
Symptom: droplets or a burr of re-solidified melt hanging under the cut.
Causes: gas pressure too low; cutting speed too high for the thickness; focus position too high; worn or damaged nozzle.
Remedy: increase gas pressure towards the cutting-table value; reduce cutting speed in steps of 5-10 %; lower the focus position; inspect the nozzle.

## Rough cut face / deep striations
Symptom: irregular drag lines, rough cut surface, roughness above tolerance.
Causes: cutting speed too low; focus position wrong; nozzle worn or off-centre; contaminated protective glass.
Remedy: adjust cutting speed towards the table value; check focus position; replace the nozzle after many operating hours; clean the protective glass.

## Incomplete cut / loss of cut
Symptom: the sheet is not cut through, sparks fly upward.
Causes: cutting speed too high relative to laser power; laser power too low; dirty protective glass reducing power at the workpiece.
Remedy: reduce cutting speed or increase laser power; clean or replace the protective glass.

## Burn-out / overheating
Symptom: wide kerf, burned corners, discoloured edges, temperature alarm E_TEMP.
Causes: cutting speed too low for the laser power; excessive heat input in corners.
Remedy: increase cutting speed or reduce laser power; check the cooling; review corner strategies.

## Bevel angle deviation
Symptom: bevel face angle or land outside tolerance, axis alarm E_AXIS.
Causes: bevel axis calibration drift; nozzle standoff incorrect; collision of the cutting head.
Remedy: recalibrate the bevel axis; set the nozzle standoff to the nominal value; re-measure the part.

## Alarm E_GAS
Meaning: assist-gas pressure fell below the set value during cutting.
Remedy: check the gas supply and regulator; re-run the job after the pressure is stable.
"""


def write_demo_dataset(out_dir: str, n_jobs: int = 1500, seed: int = 0, with_video: bool = True) -> str:
    """Create jobs.csv, images/<job_id>.png, videos/<job_id>.mp4 and knowledge_base/manual.md."""
    from .video import render_process_video, write_video
    os.makedirs(os.path.join(out_dir, "images"), exist_ok=True)
    df = generate_jobs(n_jobs, seed)
    df["image_path"] = [os.path.join(out_dir, "images", f"{j}.png") for j in df.job_id]
    for i, (path, defect) in enumerate(zip(df.image_path, df.defect)):
        render_edge_image(defect, seed=seed * 100000 + i).save(path)
    if with_video:
        os.makedirs(os.path.join(out_dir, "videos"), exist_ok=True)
        df["video_path"] = [
            write_video(render_process_video(d, seed=seed * 100000 + 50000 + i),
                        os.path.join(out_dir, "videos", f"{j}.mp4"))
            for i, (j, d) in enumerate(zip(df.job_id, df.defect))]
    csv_path = os.path.join(out_dir, "jobs.csv")
    df.to_csv(csv_path, index=False)
    kb_dir = os.path.join(out_dir, "knowledge_base")
    os.makedirs(kb_dir, exist_ok=True)
    with open(os.path.join(kb_dir, "manual_placeholder.md"), "w") as f:
        f.write(SYNTHETIC_MANUAL)
    return csv_path
