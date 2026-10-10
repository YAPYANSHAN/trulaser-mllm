"""Run the full pipeline.

Examples
  python run_pipeline.py                         # synthetic demo, no LLM needed
  python run_pipeline.py --llm ollama --model qwen2.5:7b-instruct
  python run_pipeline.py --data my_export.csv --docs knowledge_base   # real data
      (the CSV needs the columns in fyp_pipeline/schema.py plus defect,
       dross_height_mm, roughness_ra_um and image_path)
"""

from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np
import pandas as pd

from fyp_pipeline.evaluate import classification_metrics, confusion, report_checks, selective_metrics
from fyp_pipeline.ingest import load_machine_table, validate_machine_table
from fyp_pipeline.llm import get_llm
from fyp_pipeline.pipeline import FaultDiagnosisPipeline
from fyp_pipeline.synthetic import write_demo_dataset

HERE = os.path.dirname(os.path.abspath(__file__))


def split(df: pd.DataFrame, how: str, seed: int = 0):
    """random: 70/15/15. leave_material_out: test on a material never seen in training
    (domain-shift test recommended by Nguyen et al., 2026)."""
    rng = np.random.default_rng(seed)
    if how == "leave_material_out":
        test_mat = sorted(df.material.unique())[-1]
        test = df[df.material == test_mat]
        rest = df[df.material != test_mat].sample(frac=1, random_state=seed)
        n_val = int(0.15 * len(rest))
        return rest.iloc[n_val:], rest.iloc[:n_val], test
    idx = rng.permutation(len(df))
    a, b = int(0.7 * len(df)), int(0.85 * len(df))
    return df.iloc[idx[:a]], df.iloc[idx[a:b]], df.iloc[idx[b:]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="machine table (csv/xlsx/sqlite). Omit for synthetic demo data.")
    ap.add_argument("--docs", default=None, help="folder with manuals (.md/.txt/.pdf)")
    ap.add_argument("--kg", default=os.path.join(HERE, "knowledge_base", "laser_kg.json"))
    ap.add_argument("--llm", default="offline", choices=["offline", "ollama"])
    ap.add_argument("--model", default="qwen2.5vl:7b")
    ap.add_argument("--image-to-llm", action="store_true", help="also send the photo to a vision LLM")
    ap.add_argument("--split", default="random", choices=["random", "leave_material_out"])
    ap.add_argument("--n-jobs", type=int, default=1500)
    ap.add_argument("--n-reports", type=int, default=5)
    ap.add_argument("--epochs", type=int, default=8)
    ap.add_argument("--no-video", action="store_true", help="ignore the video_path column (table + image only)")
    ap.add_argument("--out", default=os.path.join(HERE, "outputs"))
    args = ap.parse_args()

    os.makedirs(os.path.join(args.out, "reports"), exist_ok=True)
    if args.data is None:
        print("No --data given: generating synthetic demo data ...")
        demo = os.path.join(HERE, "demo_data")
        args.data = write_demo_dataset(demo, args.n_jobs)
        args.docs = args.docs or os.path.join(demo, "knowledge_base")
    df = load_machine_table(args.data)
    if args.no_video and "video_path" in df.columns:
        df = df.drop(columns="video_path")
    problems = validate_machine_table(df)
    if problems:
        print("Data problems found:\n  " + "\n  ".join(problems))
    train, val, test = split(df, args.split)
    print(f"train {len(train)}  val {len(val)}  test {len(test)}")

    llm = get_llm(args.llm, **({"model": args.model} if args.llm == "ollama" else {}))
    pipe = FaultDiagnosisPipeline(args.kg, args.docs, llm).fit(train, val, image_epochs=args.epochs)

    # ---------------- evaluation with modality ablation
    probs = pipe.probas(test)
    y = list(test["defect"])
    rows = {f"{k} model only": classification_metrics(p, y, pipe.classes) for k, p in probs.items()}
    if "video" in probs:
        two = {k: probs[k] for k in ("table", "image")}
        rows["table + image, conflict-aware fusion"] = classification_metrics(pipe.fusion.combine(two)[0], y, pipe.classes)
    rows["simple average fusion (all)"] = classification_metrics(sum(probs.values()) / len(probs), y, pipe.classes)
    fused, _, _ = pipe.fusion.combine(probs)
    rows["conflict-aware fusion (all)"] = classification_metrics(fused, y, pipe.classes)
    decisions = pipe.fusion.decide(probs)
    sel = selective_metrics(decisions, y)

    # ---------------- reports for a few test jobs
    results = []
    sample = test[test.defect != "ok"].head(args.n_reports)
    for _, job in sample.iterrows():
        t0 = time.time()
        r = pipe.diagnose(job, use_image_in_llm=args.image_to_llm)
        r["seconds"] = round(time.time() - t0, 2)
        r["true_defect"] = job["defect"]
        results.append(r)
        with open(os.path.join(args.out, "reports", f"{job['job_id']}.json"), "w") as f:
            json.dump(r, f, indent=1, default=str)
    checks = report_checks(results)

    md = ["# Evaluation results", "",
          f"Data: `{os.path.basename(args.data)}`, split: {args.split}, test jobs: {len(test)}, LLM: {llm.name}", "",
          "## Defect classification (modality ablation)", "",
          "| Model | Accuracy | Macro-F1 | ECE (lower is better) |", "|---|---|---|---|"]
    md += [f"| {k} | {v['accuracy']:.3f} | {v['macro_f1']:.3f} | {v['ece']:.3f} |" for k, v in rows.items()]
    md += ["", "## Abstention (answer 'unknown' when unsure)", "",
           f"Thresholds: min confidence {pipe.fusion.min_confidence:.2f}, max conflict {pipe.fusion.max_conflict:.2f}", "",
           f"- Coverage (share answered): {sel['coverage']:.3f}",
           f"- Accuracy on answered jobs: {sel['selective_accuracy']:.3f}",
           f"- Share of 'unknown' cases where the best guess would have been wrong: "
           f"{sel['share_of_abstentions_that_were_wrong_guesses']}", "",
           "## Confusion matrix (fused, rows = true)", "", "```",
           confusion(y, [pipe.classes[i] for i in fused.argmax(1)], pipe.classes), "```", "",
           "## Diagnosis reports", "", f"- {checks}", ""]
    for r in results:
        rep = r["report"] or {}
        md += [f"### {r['packet']['job'].split(';')[0]}  (true: {r['true_defect']}, diagnosis: {rep.get('diagnosis')}, {r['seconds']} s)",
               "", "Root causes: " + ", ".join(f"{c['cause']} {c['evidence_ids']}" for c in rep.get("root_causes", [])),
               "", "Actions: " + ", ".join(a["action"] for a in rep.get("recommended_actions", [])),
               "", f"Parameter changes: {rep.get('parameter_changes')}", "",
               f"Problems: {r['problems'] or 'none'}", ""]
    with open(os.path.join(args.out, "evaluation.md"), "w") as f:
        f.write("\n".join(md))
    print("\n".join(md[:20]))
    print(f"\nFull results: {os.path.join(args.out, 'evaluation.md')}")


if __name__ == "__main__":
    main()
