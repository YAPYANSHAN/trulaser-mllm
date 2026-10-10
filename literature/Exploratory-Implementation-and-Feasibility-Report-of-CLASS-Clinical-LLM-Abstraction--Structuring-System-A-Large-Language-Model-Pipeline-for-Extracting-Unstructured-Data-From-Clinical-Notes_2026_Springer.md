# Exploratory Implementation and Feasibility Report of CLASS (Clinical LLM Abstraction & Structuring System), A Large Language Model Pipeline for Extracting Unstructured Data From Clinical Notes

- **Citation (IEEE):** F. H. Kuo, J. L. Fierstein, F. Gonzales, et al., "Exploratory Implementation and Feasibility Report of CLASS (Clinical LLM Abstraction & Structuring System), A Large Language Model Pipeline for Extracting Unstructured Data From Clinical Notes," *J. Med. Syst.*, vol. 50, art. 133, 2026, doi: 10.1007/s10916-026-02462-6.
- **Domain:** Clinical NLP / LLM-based information extraction pipeline
- **Relevance to FYP (1-5):** 3 — medical text, but a practical, well-engineered template for turning unstructured text into schema-validated structured data with evidence, confidence and a review dashboard. This applies directly to ingesting maintenance logs, operator notes and service reports in the FYP.

## Problem
Non-coded procedure information in long operative notes requires slow, variable manual chart abstraction. The study tests whether a constrained LLM pipeline can extract it reliably and help grow the concept lists.

## Data & modalities
2,402 paediatric oesophageal/airway surgery (EATS) operative notes covering about 6 years at one centre, pulled from the Epic data warehouse. Text only. A surgeon-curated master list of 198 procedures.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Modular Python 3.11 pipeline:
  - An expert-curated concept list and the expert's description of how they would search manually (used to retrieve the notes).
  - A task-specific prompt suite with explicit decision rules, semantic rather than literal matching, an instruction to express uncertainty, and flags for variants or novel concepts.
  - One note per stateless query, with encoding normalisation and chunking to fit the context window.
- **LLM:** GPT-5 (October 2025) via a secure institutional integration, temperature 0.1.
- **Output:** a CSV schema. The parser validates concept IDs and confidence values and logs errors without halting. Each extraction keeps the concept, supporting evidence, reasoning, confidence and metadata (model ID, time, API errors), linked back to the source note.
- Results are exported to a Power BI dashboard for expert review. No fine-tuning.

## Results (key numbers and metrics)
- All 2,402 notes were processed in ~35 h on standard hardware.
- On the 20 longest notes (mean 23,037 characters; 3,960 note–procedure pairs; 3.8% prevalence), checked by surgeon adjudication:
  - 99.97% concordance, F1 0.9967.
  - Sensitivity 0.9933, precision 1.0000.
  - No false positives. One missed procedure.
- Of 28 proposed new variants, 18 (64.3%) were judged clinically useful. The surgeon found 12 procedures that CLASS missed.

## Limitations
Single centre, single service, single adjudicator. Small evaluation subset (20 notes, selected for length). Only procedure names were evaluated. Results are tied to GPT-5 and this prompt design. Model drift requires re-validation. Privacy, governance and cost need attention for wider use.

## Transferable ideas for the FYP pipeline
- **Data ingestion / text:** use the same pattern to extract structured fields from free-text maintenance logs, alarm descriptions, operator shift notes and service tickets for the TruLaser. Use an expert-curated concept list (fault codes, components, defect types) and flag novel concepts for review.
- **LLM reasoning:** require evidence spans, reasoning and confidence for each extracted item. Validate against a schema and allowed IDs. Use temperature ~0.1 with stateless per-document calls.
- **Deployment:** link outputs back to source records for auditability. A dashboard lets engineers drill down from aggregate fault statistics to individual evidence.
- **Evaluation:** keep a small, expert-adjudicated regression test set and re-run it before each batch to detect model drift. Report sensitivity and precision under imbalance.
