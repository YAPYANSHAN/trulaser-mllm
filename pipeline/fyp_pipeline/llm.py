"""LLM back-ends.

* "offline": no model at all - builds the report from the evidence with rules.
  Lets you run and test the full pipeline anywhere.
* "ollama": a local open model through Ollama (http://localhost:11434), e.g.
  qwen2.5:7b-instruct for text or qwen2.5vl:7b / llava for text + image.
  Local models keep factory data on-premise; Xu et al. (KG + Qwen-14B, Sci. Rep.,
  2026) and Wu et al. (local DeepSeek-R1-distill, ESWA, 2026) show a local 7-14B
  model plus a knowledge base can match GPT-4o on domain questions.

To add a cloud model (Claude, GPT, Gemini), write another class with the same
`generate(system, user, image_paths)` method.
"""

from __future__ import annotations

import base64
import json

import requests


class OfflineLLM:
    name = "offline-rules"

    def generate(self, system: str, user: str, image_paths=None) -> str:
        packet = json.loads(user.split("EVIDENCE_JSON:", 1)[1].split("END_EVIDENCE", 1)[0])
        return json.dumps(rule_based_report(packet))


class OllamaLLM:
    def __init__(self, model: str = "qwen2.5vl:7b", host: str = "http://localhost:11434", temperature: float = 0.0):
        self.model, self.host, self.temperature = model, host, temperature
        self.name = f"ollama:{model}"

    def generate(self, system: str, user: str, image_paths=None) -> str:
        msg = {"role": "user", "content": user}
        if image_paths:
            msg["images"] = [base64.b64encode(open(p, "rb").read()).decode() for p in image_paths]
        r = requests.post(f"{self.host}/api/chat", timeout=600, json={
            "model": self.model,
            "messages": [{"role": "system", "content": system}, msg],
            "stream": False,
            "format": "json",
            "options": {"temperature": self.temperature},
        })
        r.raise_for_status()
        return r.json()["message"]["content"]


def get_llm(kind: str = "offline", **kw):
    if kind == "offline":
        return OfflineLLM()
    if kind == "ollama":
        return OllamaLLM(**kw)
    raise ValueError(kind)


def rule_based_report(packet: dict) -> dict:
    """Deterministic report used by the offline back-end (and as a baseline in the
    evaluation, so you can show what the LLM adds)."""
    decision = packet["decision"]
    label = decision["label"]
    causes = packet["knowledge_graph_paths"]
    ev_ids = {e["id"]: e for e in packet["evidence"]}
    root, actions = [], []
    if label == "unknown":
        actions = [{"action": a, "detail": "System is unsure; collect more evidence.", "evidence_ids": ["E_DEC"]}
                   for a in packet["allowed_actions"]]
        # still name the causes the evidence points to for the best guess, as low-confidence leads
        for c in causes:
            if c["support"] > 0:
                ids = [i for i, e in ev_ids.items() if e.get("signature") in c["matched_evidence"]]
                root.append({"cause": c["cause"], "evidence_ids": ids, "confidence": "low"})
    else:
        for c in causes:
            ids = [i for i, e in ev_ids.items() if e.get("signature") in c["matched_evidence"]]
            if c["support"] > 0:
                root.append({"cause": c["cause"], "evidence_ids": ids, "confidence": "high" if c["support"] > 1 else "medium"})
                for r in c["remedies"]:
                    actions.append({"action": r, "detail": f"Addresses {c['cause']}.", "evidence_ids": ids})
        if not root and causes:
            root.append({"cause": causes[0]["cause"], "evidence_ids": [], "confidence": "low"})
    return {
        "image_description": f"Image model reports {decision['image_says']} near the {packet['image_region']}."
        + "".join(f" {e['text'].capitalize()}." for e in packet["evidence"] if e["type"].startswith("video")),
        "defect_location": packet["image_region"],
        "diagnosis": label,
        "root_causes": root,
        "recommended_actions": actions,
        "parameter_changes": packet.get("optimiser", {}).get("changes", {}),
        "explanation": "Rule-based summary of the evidence (no language model used).",
        "uncertainty": decision.get("abstain_reason") or f"fused confidence {decision['confidence']:.2f}",
    }
