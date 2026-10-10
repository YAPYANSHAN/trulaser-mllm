"""Make a small, made-up TruLaser history to practise the event-centric
multimodal knowledge graph (MMKG) in Neo4j. Nothing here is real TRUMPF data.

Story built into the data (so the graph has something to find):
  * the nozzle wears out over time -> rough cuts and dross become more common,
    and each nozzle change resets this;
  * one afternoon the gas supply weakens -> E_GAS alarms, then dross;
  * the protective glass gets dirty -> incomplete cuts until it is cleaned;
  * a head collision knocks the bevel axis out -> bevel deviations until it is
    recalibrated.
Photos and videos are copied from the pipeline's synthetic demo set, picked to
match each job's defect.
"""

import json
import os
import shutil
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.join(HERE, "..", "pipeline", "demo_data")
KG = os.path.join(HERE, "..", "pipeline", "knowledge_base", "laser_kg.json")
rng = np.random.default_rng(7)

# ------------------------------------------------------------- timeline
events, jobs = [], []
t = datetime(2026, 9, 1, 8, 0)
nozzle_jobs = lens_jobs = 0
gas_problem = glass_dirty = axis_off = False
eid = 0


def add_event(kind, when, **kw):
    global eid
    eid += 1
    events.append({"event_id": f"EV{eid:04d}", "type": kind, "timestamp": when.isoformat(timespec="minutes"), **kw})
    return events[-1]["event_id"]


for day in range(15):                                      # 15 working days, one machine
    t = datetime(2026, 9, 1, 8, 0) + timedelta(days=day + 2 * (day // 5))
    for n in range(16):                                    # 16 jobs a day
        # scripted incidents
        if day == 4 and n == 6:
            gas_problem = True
        if day == 5 and n == 0:
            gas_problem = False
            add_event("Maintenance", t, action="gas supply regulator repaired", component="gas supply")
        if day == 8 and n == 0:
            glass_dirty = True
        if day == 9 and n == 4:
            glass_dirty = False
            lens_jobs = 0
            add_event("Maintenance", t, action="protective glass cleaned", component="protective glass")
        if day == 11 and n == 6:
            axis_off = True
            add_event("Alarm", t, code="E_AXIS", text="cutting head collision detected")
        if day == 13 and n == 3:
            axis_off = False
            add_event("Maintenance", t, action="bevel axis recalibrated", component="bevel axis")
        if nozzle_jobs >= 70 and n == 0:
            nozzle_jobs = 0
            add_event("Maintenance", t, action="nozzle replaced", component="nozzle")

        material = rng.choice(["mild_steel", "stainless", "aluminium"])
        thickness = float(rng.choice([3, 5, 8, 10, 12]))
        bevel = float(rng.choice([0, 0, 0, 30, 45]))
        pressure_nominal = 0.8 if material == "mild_steel" else 15.0
        pressure = pressure_nominal * (0.55 if gas_problem else rng.normal(1, 0.05))
        job_id = f"J{len(jobs) + 1:04d}"
        if gas_problem and rng.random() < 0.6:
            add_event("Alarm", t, code="E_GAS", text="assist gas pressure below set value", job_id=job_id)

        # which defect does this job get?
        risk = {
            "dross": 0.04 + 0.004 * nozzle_jobs + (0.6 if gas_problem else 0),
            "rough_striations": 0.03 + 0.004 * nozzle_jobs,
            "incomplete_cut": 0.02 + (0.5 if glass_dirty else 0),
            "bevel_deviation": (0.8 if (axis_off and bevel > 0) else 0.02 if bevel > 0 else 0),
            "burn_overheating": 0.02,
        }
        defect = "ok"
        for d, p in sorted(risk.items(), key=lambda kv: -kv[1]):
            if rng.random() < min(p, 0.9):
                defect = d
                break
        jobs.append({
            "job_id": job_id, "start": t.isoformat(timespec="minutes"), "material": material,
            "thickness_mm": thickness, "laser_power_w": round(min(6000, 1500 + 300 * thickness) * rng.normal(1, 0.04)),
            "cutting_speed_mm_min": round(9000 * 2 / (thickness + 1) * rng.normal(1, 0.06)),
            "gas_pressure_bar": round(pressure, 2), "bevel_angle_deg": bevel,
            "nozzle_jobs_since_change": nozzle_jobs, "glass_jobs_since_clean": lens_jobs,
            "defect": defect,
        })
        add_event("Job", t, job_id=job_id)
        t += timedelta(minutes=int(rng.integers(18, 32)))
        add_event("Inspection", t, job_id=job_id, result=defect)
        nozzle_jobs += 1
        lens_jobs += 1

# ------------------------------------------------------------- photos and videos
demo = pd.read_csv(os.path.join(DEMO, "jobs.csv"))
os.makedirs(os.path.join(HERE, "media", "photos"), exist_ok=True)
os.makedirs(os.path.join(HERE, "media", "videos"), exist_ok=True)
pool = {d: list(g.job_id) for d, g in demo.groupby("defect")}
photos, videos = [], []
for j in jobs:
    src = pool[j["defect"]].pop(int(rng.integers(len(pool[j["defect"]]))))
    p_dst = os.path.join("media", "photos", f"{j['job_id']}.png")
    v_dst = os.path.join("media", "videos", f"{j['job_id']}.mp4")
    shutil.copy(os.path.join(DEMO, "images", f"{src}.png"), os.path.join(HERE, p_dst))
    shutil.copy(os.path.join(DEMO, "videos", f"{src}.mp4"), os.path.join(HERE, v_dst))
    # stand-in embedding: the photo shrunk to 8x8 grey values (replace with the
    # image model's last-layer features in the real pipeline)
    img = np.asarray(Image.open(os.path.join(HERE, p_dst)).convert("L").resize((8, 8)), dtype=float) / 255
    emb = (img.flatten() - img.mean()) / (img.std() + 1e-6)
    # stand-in model output: correct 85 % of the time
    label = j["defect"] if rng.random() < 0.85 else rng.choice(list(risk) + ["ok"])
    photos.append({"photo_id": f"P{j['job_id']}", "job_id": j["job_id"], "file": p_dst,
                   "model_label": label, "confidence": round(float(rng.uniform(0.55, 0.99)), 2),
                   "embedding": ";".join(f"{x:.3f}" for x in emb)})
    videos.append({"video_id": f"V{j['job_id']}", "job_id": j["job_id"], "file": v_dst,
                   "model_label": j["defect"] if rng.random() < 0.8 else "ok",
                   "unusual_signal": {"bevel_deviation": "glow drifts sideways", "dross": "sparks fall below the cut",
                                      "incomplete_cut": "sparks fly upward", "rough_striations": "glow brightness oscillates",
                                      "burn_overheating": "glow grows over time"}.get(j["defect"], "none")})

# ------------------------------------------------------------- knowledge layer (from the placeholder manual)
triples = json.load(open(KG))["triples"]
manual = {
    "dross": "Troubleshooting guide (placeholder), section 'Dross on the bottom edge'",
    "rough_striations": "Troubleshooting guide (placeholder), section 'Rough cut face / deep striations'",
    "incomplete_cut": "Troubleshooting guide (placeholder), section 'Incomplete cut / loss of cut'",
    "burn_overheating": "Troubleshooting guide (placeholder), section 'Burn-out / overheating'",
    "bevel_deviation": "Troubleshooting guide (placeholder), section 'Bevel angle deviation'",
}
knowledge = [{"subject": s, "relation": r.upper(), "object": o,
              "source": manual.get(s, manual.get(next((a for a, rr, b in triples if b == s and rr == "caused_by"), ""), ""))}
             for s, r, o in triples if r in ("caused_by", "remedied_by")]
for k in knowledge:
    k["relation"] = {"CAUSED_BY": "CAUSED_BY", "REMEDIED_BY": "FIXED_BY"}[k["relation"]]
alarm_links = [{"code": "E_GAS", "cause": "low_gas_pressure"}, {"code": "E_AXIS", "cause": "bevel_axis_drift"},
               {"code": "E_TEMP", "cause": "power_too_high"}]
component_links = [{"component": "nozzle", "cause": "worn_nozzle"},
                   {"component": "protective glass", "cause": "dirty_protective_glass"},
                   {"component": "gas supply", "cause": "low_gas_pressure"},
                   {"component": "bevel axis", "cause": "bevel_axis_drift"}]

# ------------------------------------------------------------- write CSVs
out = os.path.join(HERE, "csv")
os.makedirs(out, exist_ok=True)
ev = pd.DataFrame(events).sort_values(["timestamp", "event_id"])
ev.to_csv(os.path.join(out, "events.csv"), index=False)
pd.DataFrame(jobs).to_csv(os.path.join(out, "jobs.csv"), index=False)
pd.DataFrame(photos).to_csv(os.path.join(out, "photos.csv"), index=False)
pd.DataFrame(videos).to_csv(os.path.join(out, "videos.csv"), index=False)
pd.DataFrame(knowledge).to_csv(os.path.join(out, "knowledge.csv"), index=False)
pd.DataFrame(alarm_links).to_csv(os.path.join(out, "alarm_causes.csv"), index=False)
pd.DataFrame(component_links).to_csv(os.path.join(out, "component_causes.csv"), index=False)
print(f"{len(jobs)} jobs, {len(ev)} events, {len(knowledge)} knowledge facts")
print(pd.DataFrame(jobs).defect.value_counts().to_string())
print(ev.type.value_counts().to_string())
