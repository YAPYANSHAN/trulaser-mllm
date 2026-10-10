"""Stage 5 - LLM reasoning: turn all evidence into an evidence-based diagnosis report.

Design rules, each taken from the reviewed papers:
  * Four reasoning steps: describe image -> locate defect -> identify defect ->
    match to manual/rules (Yang et al., RAG + multimodal fusion for power
    equipment, 2026).
  * The LLM explains the fused decision but may not change it; maintenance
    actions come from a whitelist, and only conservative ones when "unknown"
    (Shi et al., 2026).
  * Every claim cites an evidence id (E1, E2 ...) or document chunk, so a report
    can be audited (Ru et al., 2026; Zhang et al., LLM-KGSO, 2026).
  * Output is a fixed JSON schema and is validated (Zhang et al., vineyard
    monitoring with DeepSeek-VL2, Measurement, 2026; Abdelkader, 2026).
"""

from __future__ import annotations

import json

import pandas as pd

from .ingest import serialise_row
from .schema import ALLOWED_ACTIONS, CONSERVATIVE_ACTIONS, DEFECT_CLASSES, UNKNOWN

SYSTEM_PROMPT = """You are a laser-cutting diagnosis assistant for a TRUMPF TruLaser 3000 Bevel Cut machine.
You receive an EVIDENCE packet: a fused decision from trained models, machine-table evidence,
image-model findings, process-video findings (if a video exists),
knowledge-graph cause paths and manual excerpts, each with an id.

Reason in four steps:
 1. Describe what the image evidence (and video evidence, if any) shows.
 2. Say where on the part the defect is.
 3. State the diagnosis. It MUST equal decision.label (you explain it, you do not change it).
 4. Match the evidence to causes and remedies from the knowledge graph and manual.

Rules:
 - Use ONLY the evidence provided. Every root cause and action must list the evidence ids that support it.
 - Recommend actions only from allowed_actions. Copy parameter_changes from the optimiser; never invent numbers.
 - If decision.label is "unknown", say why and recommend only the allowed conservative actions.
 - If the table, image or video evidence disagree, say so in "uncertainty".

Reply with JSON only, using exactly these keys:
{"image_description": str, "defect_location": str, "diagnosis": str,
 "root_causes": [{"cause": str, "evidence_ids": [str], "confidence": "high|medium|low"}],
 "recommended_actions": [{"action": str, "detail": str, "evidence_ids": [str]}],
 "parameter_changes": object, "explanation": str, "uncertainty": str}"""


def build_evidence_packet(row: pd.Series, decision: dict, profile: dict, tab_expl: list[dict],
                          image_region: str, kg_paths: list[dict], doc_hits, optimiser_out: dict | None,
                          video_ev: dict | None = None) -> dict:
    says = "; ".join(f"{k[:-5]} model says {v}" for k, v in decision.items() if k.endswith("_says"))
    evidence = [{"id": "E_DEC", "type": "decision",
                 "text": f"fused decision {decision['label']} (best guess {decision['best_guess']}, "
                         f"confidence {decision['confidence']:.2f}; {says})"}]
    n = 1
    for c, lvl in profile["levels"].items():
        if lvl not in ("normal", "none"):
            evidence.append({"id": f"E{n}", "type": "machine_table", "signature": f"{c}={lvl}",
                             "text": f"{c} is {lvl.upper()}: {profile['details'][c]}"})
            n += 1
    for t in tab_expl:
        if t["importance"] > 0.01:
            evidence.append({"id": f"E{n}", "type": "table_model_attribution",
                             "text": f"{t['feature']} = {t['value']} pushed the table model towards its answer "
                                     f"(probability drop {t['importance']:.2f} if set to typical {t['typical']})"})
            n += 1
    evidence.append({"id": f"E{n}", "type": "image_model", "text": f"image model attention on the {image_region}"})
    n += 1
    if video_ev:
        # deviation from normal cuts, not raw frames (after Ding et al., 2026)
        clips = video_ev["clip_labels"]
        evidence.append({"id": "V1", "type": "video_model",
                         "text": f"video model label per clip, in time order: {', '.join(clips)}"})
        for j, sig in enumerate(video_ev["unusual_signals"]):
            evidence.append({"id": f"V{j + 2}", "type": "video_signal",
                             "text": f"process video {sig['signal'].replace('_', ' ')} is {sig['level'].upper()} "
                                     f"({sig['value']} vs {sig['normal']} on normal cuts)"})
    for i, (score, ch) in enumerate(doc_hits):
        evidence.append({"id": f"D{i + 1}", "type": "manual", "text": f"{ch.cite} {ch.text}"})
    allowed = CONSERVATIVE_ACTIONS if decision["label"] == UNKNOWN else ALLOWED_ACTIONS
    return {
        "job": serialise_row(row),
        "decision": decision,
        "image_region": image_region,
        "evidence": evidence,
        "knowledge_graph_paths": kg_paths,
        "optimiser": optimiser_out or {},
        "allowed_actions": allowed,
    }


def build_user_prompt(packet: dict) -> str:
    return "EVIDENCE_JSON:\n" + json.dumps(packet, indent=1, default=str) + "\nEND_EVIDENCE\nWrite the JSON report."


def validate_report(report_text: str, packet: dict) -> tuple[dict | None, list[str]]:
    """Parse and check the LLM output. Returns (report, list of problems)."""
    problems = []
    try:
        rep = json.loads(report_text[report_text.find("{"): report_text.rfind("}") + 1])
    except Exception as e:  # noqa: BLE001
        return None, [f"not valid JSON: {e}"]
    for k in ["diagnosis", "root_causes", "recommended_actions", "explanation"]:
        if k not in rep:
            problems.append(f"missing key {k}")
    if rep.get("diagnosis") != packet["decision"]["label"]:
        problems.append(f"diagnosis changed from {packet['decision']['label']} to {rep.get('diagnosis')}")
    if rep.get("diagnosis") not in DEFECT_CLASSES + [UNKNOWN]:
        problems.append("diagnosis not a known class")
    ids = {e["id"] for e in packet["evidence"]}
    for item in rep.get("root_causes", []) + rep.get("recommended_actions", []):
        bad = [i for i in item.get("evidence_ids", []) if i not in ids]
        if bad:
            problems.append(f"cites evidence that does not exist: {bad}")
    for a in rep.get("recommended_actions", []):
        if a.get("action") not in packet["allowed_actions"]:
            problems.append(f"action not allowed: {a.get('action')}")
    return rep, problems


def reason(llm, packet: dict, image_paths=None, retries: int = 1) -> dict:
    user = build_user_prompt(packet)
    for attempt in range(retries + 1):
        text = llm.generate(SYSTEM_PROMPT, user, image_paths)
        rep, problems = validate_report(text, packet)
        if rep is not None and not problems:
            return {"report": rep, "problems": [], "model": llm.name, "attempts": attempt + 1}
        user = build_user_prompt(packet) + "\nYour previous answer had these problems, fix them: " + "; ".join(problems)
    return {"report": rep, "problems": problems, "model": llm.name, "attempts": retries + 1}
