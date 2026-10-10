"""The whole pipeline in one class: train the specialist models, then diagnose a job.

    data (table + image + manuals)
      -> Stage 1 ingest & validate
      -> Stage 2 specialist models (table classifier, image CNN, video CNN-GRU if
         the table has a video_path column, quality surrogate)
      -> Stage 3 knowledge (evidence profile, knowledge-graph paths, manual retrieval)
      -> Stage 4 conflict-aware fusion with "unknown"
      -> Stage 6 parameter optimiser (tool)
      -> Stage 5 LLM report (validated JSON, cited evidence)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .evidence import EvidenceProfiler
from .fusion import ConflictAwareFusion
from .ingest import load_documents, load_image
from .knowledge import BM25, KnowledgeGraph
from .optimiser import ParameterOptimiser
from .reasoner import build_evidence_packet, reason
from .schema import DEFECT_CLASSES, UNKNOWN
from .tabular_model import DefectClassifier, QualitySurrogate
from .video import DefectVideoModel, VideoEvidence, load_video
from .vision_model import DefectImageModel


class FaultDiagnosisPipeline:
    def __init__(self, kg_path: str, docs_folder: str, llm, backbone: str = "small_cnn", seed: int = 0):
        self.classes = DEFECT_CLASSES
        self.tab = DefectClassifier(seed)
        self.sur = QualitySurrogate(seed=seed)
        self.img = DefectImageModel(self.classes, backbone, seed=seed)
        self.vid = None          # created in fit() only if the data has videos
        self.vid_evidence = VideoEvidence()
        self.profiler = EvidenceProfiler()
        self.fusion = ConflictAwareFusion(self.classes)
        self.kg = KnowledgeGraph(kg_path)
        self.bm25 = BM25(load_documents(docs_folder))
        self.llm = llm
        self.optimiser = None

    # ------------------------------------------------------------ training
    def fit(self, train: pd.DataFrame, val: pd.DataFrame, image_epochs: int = 8):
        print("Training table model ...")
        self.tab.fit(train, train["defect"])
        print("Training quality surrogate ...")
        self.sur.fit(train)
        print("Training image model ...")
        self.img.fit(self.images(train), list(train["defect"]), epochs=image_epochs)
        if self.has_video(train):
            print("Training video model ...")
            videos = self.videos(train)
            self.vid = DefectVideoModel(self.classes).fit(videos, list(train["defect"]), epochs=image_epochs)
            self.vid_evidence.fit(videos, list(train["defect"]))
        self.profiler.fit(train)
        print("Tuning fusion thresholds on validation data ...")
        self.fusion.tune(self.probas(val), list(val["defect"]))
        print(f"  min_confidence={self.fusion.min_confidence:.2f}  max_conflict={self.fusion.max_conflict:.2f}")
        self.optimiser = ParameterOptimiser(self.tab, self.sur)
        return self

    @staticmethod
    def images(df: pd.DataFrame) -> np.ndarray:
        return np.stack([load_image(p) for p in df["image_path"]])

    @staticmethod
    def has_video(df: pd.DataFrame) -> bool:
        return "video_path" in df.columns and df["video_path"].notna().all()

    @staticmethod
    def videos(df: pd.DataFrame) -> list[np.ndarray]:
        return [load_video(p) for p in df["video_path"]]

    def probas(self, df: pd.DataFrame) -> dict[str, np.ndarray]:
        """Class probabilities from every specialist model, in DEFECT_CLASSES order."""
        p_tab = self.tab.predict_proba(df)
        order = [list(self.tab.model.classes_).index(c) for c in self.classes]
        out = {"table": p_tab[:, order], "image": self.img.predict_proba(self.images(df))}
        if self.vid is not None and self.has_video(df):
            out["video"] = self.vid.predict_proba(self.videos(df))
        return out

    @staticmethod
    def kg_directions(kg_paths: list[dict], levels: dict) -> dict:
        """Knowledge-guided search space: for every cause supported by evidence,
        move its parameter back towards normal (low -> increase, high -> decrease)."""
        from .schema import ADJUSTABLE_PARAMETERS
        d = {}
        for p in kg_paths:
            for sig in p["matched_evidence"]:
                param, lvl = sig.split("=")
                if param in ADJUSTABLE_PARAMETERS and lvl in ("low", "high"):
                    d[param] = 1 if lvl == "low" else -1
        return d

    # ------------------------------------------------------------ inference
    def diagnose(self, job: pd.Series, use_image_in_llm: bool = False) -> dict:
        row = pd.DataFrame([job.to_dict()])
        decision = self.fusion.decide(self.probas(row))[0]
        profile = self.profiler.profile(job)
        region = self.img.saliency_region(load_image(job["image_path"]))
        label_for_kg = decision["label"] if decision["label"] != UNKNOWN else decision["best_guess"]
        kg_paths = self.kg.rank_causes(label_for_kg, profile["levels"])
        query = label_for_kg.replace("_", " ") + " " + " ".join(p["cause"].replace("_", " ") for p in kg_paths[:2])
        docs = self.bm25.search(query, k=2)
        opt = None
        if decision["label"] not in ("ok", UNKNOWN):
            opt = self.optimiser.recommend(row, self.kg_directions(kg_paths, profile["levels"]))
        video_ev = None
        if self.vid is not None and self.has_video(row):
            frames = load_video(job["video_path"])
            video_ev = {"clip_labels": self.vid.clip_labels(frames),
                        "unusual_signals": self.vid_evidence.describe(frames)}
        packet = build_evidence_packet(job, decision, profile, self.tab.explain(row), region, kg_paths, docs, opt,
                                       video_ev)
        out = reason(self.llm, packet, [job["image_path"]] if use_image_in_llm else None)
        out["packet"] = packet
        return out
