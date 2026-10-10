# CTI-Thinker: An LLM-Driven System for CTI Knowledge Graph Construction and Attack Reasoning

- **Citation (IEEE):** X. Yang, R. Zhong, Y. Chen, et al., "CTI-Thinker: an LLM-driven system for CTI knowledge graph construction and attack reasoning," *Cybersecurity*, vol. 9, art. 106, 2026, doi: 10.1186/s42400-025-00505-y.
- **Domain:** Cybersecurity / cyber threat intelligence (CTI) / knowledge graphs + GraphRAG
- **Relevance to FYP (1-5):** 3 - different domain, but the full recipe (LLM entity/relation extraction with LoRA, entity alignment, KG + GraphRAG reasoning against a standard taxonomy) maps well onto building a fault knowledge graph from TRUMPF documentation and fault logs.

## Problem
CTI data are unstructured, fragmented, manually annotated and weakly mapped to attack techniques. Classical extraction (BiLSTM-CRF, BERT) generalises poorly across paragraphs, to emerging threats and to low-resource samples, limiting attribution and intent inference.

## Data & modalities
Text: APT analysis reports from security vendors (e.g. FireEye, QiAnXin, 360, Kaspersky), open-source threat/vulnerability alerts, technical blogs; crawled, cleaned, segmented to sentences. Schema: 12 entity types (based on STIX 2.1, e.g. Attacker, Technique, Vulnerability, Malware Family, ATT&CK) and 11 relation types (e.g. Alias_of, Use, Target_at, Exploit). External MITRE ATT&CK knowledge base.

## Method
(1) LLM-assisted annotation (LLaMA3-8B, DeepSeek, ChatGPT) with few-shot prompt templates producing standardised JSON triples. (2) Extraction via in-context learning plus a LoRA-fine-tuned LLaMA3-8B. (3) Two-stage knowledge alignment: LLM-based coarse semantic grouping, then fine-grained entity alignment with embedding cosine similarity above a validation-tuned threshold (e.g. merging "APT32" and "OceanLotus"). (4) CTI knowledge graph construction. (5) GraphRAG reasoning engine combining the KG with ATT&CK resources for tactic/technique inference and question answering; answers scored with a reasoning-based rubric.

## Results
Entity recognition F1 0.8385 and relation extraction F1 0.7689, surpassing deep-learning baselines, ATTCKG+, LLM-TIKG, ChatGPT-4o, DeepSeek-R1 and LoRA-tuned LLaMA3-8B/Qwen/Mistral-7B baselines. Alignment: average +5.50% (entity) and +5.81% (triplet) over baselines. In a QA example, a native LLM hallucinated (score 0.20), plain LLM-RAG scored 0.50 and CTI-Thinker 0.95.

## Limitations
Semantic drift and redundant triples in complex/ambiguous reports, causing incorrect aggregation or omissions; unstable multi-turn reasoning (causal tracing); interpretability of reasoning paths needs work; text-only - no logs or malware artefacts yet (multimodal extension is future work).

## Transferable ideas for the FYP pipeline
- **Text/RAG + KG:** define a fault schema (Machine component, Alarm code, Symptom, Defect type, Material, Process parameter, Cause, Remedy) and use an LLM (ICL or LoRA) to extract JSON triples from TruLaser manuals, alarm lists and service reports.
- **Data ingestion:** entity alignment by LLM grouping + embedding similarity to merge synonyms (e.g. "dross", "slag", "burr at bottom edge"; parameter aliases across software versions).
- **LLM reasoning:** GraphRAG over the fault KG plus the official TRUMPF taxonomy as the analogue of ATT&CK, enabling symptom -> cause -> remedy chain reasoning with traceable paths.
- **Evaluation:** compare native LLM vs vanilla RAG vs KG-RAG on the same diagnostic questions with a scored rubric.
