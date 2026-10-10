# Mutual information-based retrieval-augmented generation for domain question answering

- **Citation (IEEE):** H. Lu, D. Zheng, and L. Yang, "Mutual information-based retrieval-augmented generation for domain question answering," *Knowledge and Information Systems*, vol. 68, art. 49, 2026, doi: 10.1007/s10115-025-02624-x.
- **Domain:** NLP — knowledge-graph-based RAG for domain-specific question answering (medical, biological, industrial)
- **Relevance to FYP (1-5):** 3 — text-only, but KG-RAG with jargon/abbreviation handling and noise-pruned subgraph retrieval is directly applicable to grounding diagnosis in TRUMPF manuals and fault-code documentation.

## Problem
Retrieve-first RAG pulls in noisy or unnecessary context, causing irrelevant information, wrong associations and hallucinations, especially for multi-hop questions and texts full of abbreviations/jargon. Existing KG-RAG fixes subgraph size/hop count rather than adapting to what the generator actually needs.

## Data & modalities
Text only. Multi-hop Chinese medical QA: CMCQA and Chinese-medical-dialogue-data (CMD), with jargon/abbreviations added manually; one-hop biological (BDQA) and industrial domain QA (IDQA) sets.

## Method
- **KG construction:** LLM extracts [entity, relation, entity] triples from unstructured text with domain-specific relation lists in the prompt; a **search engine** is called to resolve unknown abbreviations/jargon; stored in **Neo4j**.
- **Generate-then-retrieve:** LLM extracts keywords, matches graph entities, and retrieves subgraphs scored by **mutual information** between question and candidate facts (probability model Qwen2-1.5B), with hop parameter n.
- **Subgraph pruning** to drop redundant branches; **LangChain** fuses KG, LLM and web knowledge; final answers converted back into triples to **update the KG**.
- Inference LLM gpt-4o-mini; embeddings text-embedding-3-small. Baselines: GPT-4/4o/4o-mini (no retrieval), traditional RAG, MindMap, Graph-RAG, PG-RAG.

## Results
- CMCQA F1: MI-RAG (n=3) 0.6570 vs Graph-RAG 0.6320, PG-RAG 0.6312, traditional RAG 0.6176, GPT-4o 0.6035. CMD F1: 0.5849 (best among methods).
- n=3 chosen as the best cost-performance trade-off (n=4 marginal gains at higher compute).
- On one-hop BDQA/IDQA (manual 0/0.5/1 scoring), all RAG methods far exceed plain GPTs, but differences between RAG variants are small.
- Ablations: removing search-engine jargon resolution, subgraph pruning or knowledge aggregation each lowers accuracy; no pruning increases token usage.

## Limitations
Highly sensitive to prompt-template design per domain (entity/relation extraction quality depends on it); requires domain expertise to craft prompts; gains are modest in absolute terms; evaluation mostly on Chinese medical data.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** build a Neo4j KG from TruLaser manuals and maintenance logs with a fixed relation schema (e.g. *fault → caused_by → parameter*, *defect → remedied_by → adjustment*, *alarm_code → indicates → component*).
- **Jargon handling:** maintain an abbreviation glossary (e.g. TRUMPF-specific terms, nozzle/gas codes) resolved during triple extraction — the analogue of the search-engine step.
- **Retrieval:** prune retrieved subgraphs to only facts relevant to the observed symptoms to reduce hallucination and token cost; tune hop depth.
- **Continuous learning:** write confirmed diagnoses back into the KG as new triples.
- **Evaluation:** compare no-RAG vs vector-RAG vs KG-RAG with precision/recall/F1 on a held-out fault-QA set.
