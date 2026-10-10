# Construction of waste-to-resource knowledge graph for industrial symbiosis identification using large language models

- **Citation (IEEE):** L. Zhao, Y. Sun, J. Ren, et al., "Construction of waste-to-resource knowledge graph for industrial symbiosis identification using large language models," *Nature Communications*, vol. 17, art. 26, 2026, doi: 10.1038/s41467-025-66599-7.
- **Domain:** Industrial sustainability / circular economy; LLM-based information extraction and knowledge-graph construction.
- **Relevance to FYP (1-5):** 3 — not fault diagnosis, but a well-evaluated LLM pipeline (chunk retrieval, schema-constrained extraction, LoRA fine-tuning, embedding-based entity fusion, Neo4j KG) directly reusable for turning TRUMPF documentation into a structured knowledge base.

## Problem
Waste-to-resource (W2R) databases (e.g., MAESTRI, ISDATA) used for industrial symbiosis are manually built, small, noisy and unstandardised. The authors automate construction of a W2R knowledge graph (W2RKG) from research literature using LLMs.

## Data & modalities
Text only: 4499 Scopus papers (abstracts) plus full texts of 77 review papers via Elsevier API, with DOIs kept as provenance. 150 manually annotated abstracts (100 for fine-tuning, 50 for evaluation).

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Four parts: (1) data preparation; (2) Retrieving Module — full texts split into chunks and an LLM classifies each chunk as relevant/irrelevant (mitigating long-context and positional bias); (3) Extraction Module — framed as Event Argument Extraction with three arguments (waste, transformed resource, transforming process); compared GPT-4o, GPT-4o-mini and Llama-3.1-8B-Instruct (4-bit, LoRA r=8, alpha=8), zero- vs few-shot (k=2), JSON-style vs code-style output; benchmarked against LangChain and LlamaIndex extractors; (4) Fusion Module — gte-large-en-v1.5 embeddings, Hierarchical Agglomerative Clustering (complete linkage, threshold 0.2), then GPT-4o-mini standardises entity names per cluster; result written to Neo4j with process and DOI as edge properties.

## Results (key numbers and metrics)
Highest precision 93.53% (LlamaIndex + GPT-4o few-shot); proposed GPT-4o JSON few-shot 91.94%; highest recall 88.20% (GPT-4o-mini code-style zero-shot), chosen because recall is prioritised. Few-shot and fine-tuning raised precision but lowered recall. Error analysis: 23% true mispredictions, 46% ambiguity. Final KG: 3518 wastes, 4471 resources, 33,679 relationships (from intermediate 7488/8343/43,199). Covers 58% of MAESTRI relationships; human evaluation: waste/resource aligned 90%/87%, valid 95.56%/83.91% (Cohen's kappa 0.41-0.54). Taranto case study: 24/45 benchmark IS links (53%), 81% at company level.

## Limitations
Only academic sources; no material attributes/quantities; one-to-one waste-resource schema misses concurrent dependencies; extracted knowledge needs verification; GPT API cost vs local hardware burden for Llama.

## Transferable ideas for the FYP pipeline
- **Text/RAG (data ingestion):** Chunk TRUMPF manuals and use an LLM relevance filter before extraction to cut noise.
- **Text/KG:** Cast extraction as event/argument extraction with a fixed schema, e.g., (defect, probable cause, corrective parameter, material/thickness), stored in Neo4j with source page as provenance for evidence-based answers.
- **Data ingestion:** Embedding + HAC + LLM canonicalisation to unify synonyms ("dross", "burr", "slag") and alarm-code names across database and manuals.
- **LLM reasoning:** Compare zero/few-shot vs LoRA-tuned open model; note precision-recall trade-off and pick recall-favouring settings for candidate cause generation followed by verification.
- **Evaluation:** Use micro-P/R/F1 + Jaccard on an annotated set, plus multi-rater alignment/validity scoring with Cohen's kappa for expert review of diagnoses.
