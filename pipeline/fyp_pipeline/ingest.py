"""Stage 1 - data ingestion for the three modalities.

* Machine database  -> pandas DataFrame, checked against schema.MACHINE_COLUMNS
* Cut-part images   -> normalised tensors (with contrast enhancement)
* Technical documents -> text chunks for retrieval

Design notes from the literature:
  * serialise table rows into fixed, label-free text before giving them to an LLM
    (Wang et al., "Auditable progressive multimodal bearing fault diagnosis with
    LLM screening", Measurement, 2026)
  * contrast enhancement helps on shiny metal surfaces (Chen et al., "Faster
    R-CNN-based surface defect detection for sheet metal inspection", IJAMT, 2026;
    Sundaravadivel et al., Discover AI, 2026)
  * keep the source of every chunk so reports can cite it (Ru et al., npj
    Heritage Science, 2026)
"""

from __future__ import annotations

import glob
import os
import re
import sqlite3
from dataclasses import dataclass

import numpy as np
import pandas as pd
from PIL import Image, ImageOps

from .schema import MACHINE_COLUMNS, NUMERIC_COLUMNS


# ---------------------------------------------------------------- tables
def load_machine_table(path: str, sql_table: str | None = None) -> pd.DataFrame:
    """Load a CSV, Excel or SQLite export of the machine database."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(path)
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
    elif ext in (".db", ".sqlite", ".sqlite3"):
        with sqlite3.connect(path) as con:
            df = pd.read_sql_query(f"SELECT * FROM {sql_table or 'jobs'}", con)
    else:
        raise ValueError(f"Unsupported table format: {ext}")
    return df


def validate_machine_table(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable problems (empty list = table is fine)."""
    problems = []
    missing = [c for c in MACHINE_COLUMNS if c not in df.columns]
    if missing:
        problems.append(f"missing columns: {missing}")
    for c in NUMERIC_COLUMNS:
        if c in df.columns:
            bad = pd.to_numeric(df[c], errors="coerce").isna().sum()
            if bad:
                problems.append(f"{c}: {bad} empty or non-numeric values")
    if "job_id" in df.columns and df["job_id"].duplicated().any():
        problems.append("duplicate job_id values")
    return problems


def serialise_row(row: pd.Series) -> str:
    """Turn one machine record into compact 'key = value' text for an LLM prompt.

    Labels (defect, measured quality) are deliberately left out to avoid leakage.
    """
    parts = []
    for c in MACHINE_COLUMNS:
        if c in row.index:
            v = row[c]
            if isinstance(v, float):
                v = round(v, 2)
            parts.append(f"{c} = {v}")
    return "; ".join(parts)


# ---------------------------------------------------------------- images
def load_image(path: str, size: int = 64) -> np.ndarray:
    """Load an image as float32 array in [0, 1], grey-scale, auto-contrasted."""
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=1)  # simple stand-in for CLAHE
    img = img.resize((size, size))
    return np.asarray(img, dtype=np.float32) / 255.0


# ---------------------------------------------------------------- documents
@dataclass
class Chunk:
    source: str      # file name
    section: str     # heading the text sits under
    text: str

    @property
    def cite(self) -> str:
        return f"[DOC::{self.source}#{self.section}]"


def load_documents(folder: str, max_words: int = 180) -> list[Chunk]:
    """Read .md/.txt (and .pdf if pypdf is installed) and split by heading."""
    chunks: list[Chunk] = []
    for path in sorted(glob.glob(os.path.join(folder, "**", "*"), recursive=True)):
        ext = os.path.splitext(path)[1].lower()
        if ext in (".md", ".txt"):
            text = open(path, encoding="utf-8", errors="ignore").read()
        elif ext == ".pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                print(f"skip {path}: pip install pypdf to read PDFs")
                continue
            text = "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
        else:
            continue
        section, buf = "start", []
        for line in text.splitlines():
            m = re.match(r"^#+\s+(.*)", line)
            if m:
                if buf:
                    chunks.extend(_split(os.path.basename(path), section, " ".join(buf), max_words))
                section, buf = m.group(1).strip(), []
            elif line.strip():
                buf.append(line.strip())
        if buf:
            chunks.extend(_split(os.path.basename(path), section, " ".join(buf), max_words))
    return chunks


def _split(source: str, section: str, text: str, max_words: int) -> list[Chunk]:
    words = text.split()
    return [Chunk(source, section, " ".join(words[i:i + max_words])) for i in range(0, len(words), max_words)]
