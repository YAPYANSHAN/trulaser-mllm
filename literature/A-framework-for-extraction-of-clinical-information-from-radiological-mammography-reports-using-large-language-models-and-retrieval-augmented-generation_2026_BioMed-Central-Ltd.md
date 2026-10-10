# A framework for extraction of clinical information from radiological mammography reports using large language models and retrieval augmented generation

- **Citation (IEEE):** E. Godoy, J. De Ferrari, S. Lazo, et al., "A framework for extraction of clinical information from radiological mammography reports using large language models and retrieval augmented generation," *BMC Medical Informatics and Decision Making*, vol. 26, art. 345, 2026, doi: 10.1186/s12911-026-03633-8.
- **Domain:** Clinical NLP / information extraction with LLM + RAG
- **Relevance to FYP (1-5):** 4 - few-shot RAG for turning free-text reports into structured schemas transfers directly to structuring operator fault logs and maintenance notes for the laser-cutting pipeline.

## Problem
Free-text mammography reports (Spanish, BI-RADS-style) are heterogeneous and lack standard terminology; supervised NER/RE needs costly annotation and separate models. Can few-shot LLMs with retrieved examples replace fine-tuning?

## Data & modalities
Text only: Spanish mammography reports annotated (doccano, double annotation, consensus with senior radiologist) for entities (findings, characteristics, density, laterality, region/quadrant, present/absent findings) and relations (describe, locate). Fine-tuned BETO trained on 317 reports.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Vector database of annotated training reports embedded with all-MiniLM-L6-v2; annotations stored as metadata.
- For a new report, similar annotated reports are retrieved as in-context demonstrations (1-3 shot) for joint NER + RE.
- LLMs: GPT-4.1-mini, GPT-4o-mini (API); local open-weight LLaMA 2 and LLaMA 3.2 (quantised).
- Outputs mapped to a standardised BI-RADS report schema.
- Baselines: fine-tuned BETO and Clinical RoBERTa. Robustness test with injected annotation noise (clean / light / heavy) into training labels or retrieved exemplars.

## Results (key numbers and metrics)
- NER: GPT-based few-shot 0.89-0.94 F1 vs BETO 0.97; per-class GPT-4.1-mini 85.6-98.2% vs BETO 97.2-99.7%.
- RE: LLMs up to 0.78 F1 vs BETO 0.99.
- Local LLaMA models mostly below 0.50 F1 (e.g., LLaMA 3.2 RE 15.5-18.4%).
- Cost fractions of a cent per report; latency within seconds.
- BETO more robust to label noise for NER; GPT RAG comparatively more resilient for constrained RE.

## Limitations
Needs an initial annotated subset to populate the RAG store; RE is sensitive to boundaries and cross-sentence context; local models too weak; single language/site; cloud API privacy concerns.

## Transferable ideas for the FYP pipeline
- **Text/RAG / data ingestion:** store a few dozen annotated fault-log entries (symptom, defect type, location, parameter, action) in a vector DB with MiniLM embeddings; retrieve nearest examples as few-shot demonstrations to extract structured fields from new free-text operator notes.
- **LLM reasoning:** output into a fixed JSON schema (analogous to BI-RADS) so downstream fusion with machine tables is deterministic.
- **Deployment:** staged "cold start" strategy: start with RAG few-shot, switch to a fine-tuned small encoder once enough labels accumulate; small local models may be insufficient for precise extraction.
- **Evaluation:** strict per-field F1 and noise-injection robustness tests on the retrieval store.
