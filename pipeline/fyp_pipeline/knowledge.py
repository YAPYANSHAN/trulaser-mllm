"""Stage 3 - domain knowledge: a small knowledge graph + keyword retrieval (RAG).

Pattern taken from the KG/RAG papers in the review:
  * defect -> cause -> parameter -> remedy ontology and path retrieval
    (Li et al., GAT-RAG for wind-power maintenance, Chin. J. Mech. Eng., 2026;
    Zhang et al., LLM-KGSO for electromechanical fault diagnosis, Chin. J. Mech.
    Eng., 2026; Hou et al., KE-CausalLLM, Discover AI, 2026)
  * pass retrieved knowledge as compact triples, which small LLMs use best
    (Zhang et al., ceramics QA with retrieved triples, Sci. Rep., 2026)
  * hybrid keyword + vector retrieval (Yang et al., RAG and multimodal fusion for
    power equipment, J. Appl. Sci. Eng., 2026). Only BM25 is implemented here so
    nothing needs downloading; add sentence-transformers embeddings later.

The KG lives in knowledge_base/laser_kg.json so you can edit it by hand or fill
it from the TRUMPF manuals with an LLM triple-extraction step (see README).
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter

from .ingest import Chunk


class KnowledgeGraph:
    def __init__(self, path: str):
        data = json.load(open(path))
        self.triples: list[tuple[str, str, str]] = [tuple(t) for t in data["triples"]]
        self.source = data.get("source", path)

    def neighbours(self, head: str, relation: str) -> list[str]:
        return [t for h, r, t in self.triples if h == head and r == relation]

    def cause_paths(self, defect: str) -> list[dict]:
        """All defect -> cause -> (parameter, remedy) paths for a defect."""
        paths = []
        for cause in self.neighbours(defect, "caused_by"):
            paths.append({
                "defect": defect,
                "cause": cause,
                "parameters": self.neighbours(cause, "linked_to_parameter"),
                "remedies": self.neighbours(cause, "remedied_by"),
                "signature": self.neighbours(cause, "evidence_signature"),
            })
        return paths

    def rank_causes(self, defect: str, evidence: dict) -> list[dict]:
        """Score each cause by how well the measured evidence matches its signature.

        evidence: {"cutting_speed_mm_min": "high", "gas_pressure_bar": "low", ...}
        signature triples look like ("low_gas_pressure", "evidence_signature",
        "gas_pressure_bar=low").
        """
        ranked = []
        for p in self.cause_paths(defect):
            hits = [s for s in p["signature"] if evidence.get(s.split("=")[0]) == s.split("=")[1]]
            ranked.append({**p, "support": len(hits), "matched_evidence": hits})
        ranked.sort(key=lambda d: -d["support"])
        return ranked


class BM25:
    """Plain BM25 keyword retrieval over document chunks."""

    def __init__(self, chunks: list[Chunk], k1: float = 1.5, b: float = 0.75):
        self.chunks = chunks
        self.docs = [self._tok(c.section + " " + c.text) for c in chunks]
        self.avgdl = sum(map(len, self.docs)) / max(1, len(self.docs))
        df = Counter(w for d in self.docs for w in set(d))
        n = len(self.docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}
        self.tf = [Counter(d) for d in self.docs]
        self.k1, self.b = k1, b

    @staticmethod
    def _tok(text: str) -> list[str]:
        return re.findall(r"[a-z0-9_]+", text.lower().replace("_", " "))

    def search(self, query: str, k: int = 3) -> list[tuple[float, Chunk]]:
        q = self._tok(query)
        scores = []
        for i, tf in enumerate(self.tf):
            dl = len(self.docs[i])
            s = sum(self.idf.get(w, 0) * tf[w] * (self.k1 + 1) /
                    (tf[w] + self.k1 * (1 - self.b + self.b * dl / self.avgdl)) for w in q if w in tf)
            scores.append((s, self.chunks[i]))
        scores.sort(key=lambda t: -t[0])
        return [s for s in scores[:k] if s[0] > 0]
