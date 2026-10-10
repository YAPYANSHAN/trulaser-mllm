# Enhancing the capabilities of large language models for API calls through knowledge graphs

- **Citation (IEEE):** Y. Yang, X. Xiao, P. Yin, et al., "Enhancing the capabilities of large language models for API calls through knowledge graphs," *Sci. Rep.*, vol. 16, art. 16938, 2026, doi: 10.1038/s41598-026-47696-z.
- **Domain:** NLP / LLM agents — knowledge-graph-augmented tool use (API calls) in meteorology
- **Relevance to FYP (1-5):** 4 — different domain, but a directly reusable recipe: build a domain KG from operation manuals with an LLM, then let a ReAct agent use the KG to choose and parameterise data-query tools. It also compares KG against vector RAG. This maps onto the FYP's manual + machine-database querying.

## Problem
LLMs calling APIs in knowledge-intensive domains fail on specialised terminology and long or complex queries, and they hallucinate API names. Vector RAG gives shallow semantic links, incomplete coverage and weak multi-source integration. Fine-tuning is costly and must be repeated as APIs change.

## Data & modalities
Text corpus: meteorological operation manuals (not disclosed) covering severe weather, mechanisms, forecasting indicators and cases. A virtual API set of 35 tool functions. 70 instruction–answer pairs, written by experts with reference to manuals and ranging from simple lookups to multi-element analyses.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **KG construction:** Qwen-Turbo chunks the manuals (50–300 Chinese characters per chunk). Few-shot prompting (13 annotated examples) extracts 5-tuples (head, head type, relation, tail, tail type) as JSON against an entity/relation schema covering phenomena, physical quantities, equipment and formulas, with relations such as influences and causes. Leiden community detection clusters entities and prunes noisy edges. Stored in Neo4j with a BGE-M3 vector index (via Ollama), using multi-hop retrieval (up to 3 hops).
- **ReAct expert agent:** Qwen-Turbo (8k context, max 10 iterations) following Thought → Action (API selection) → Action Input (parameters) → Observation → Final Answer, with KG knowledge supporting reasoning.
- **Baselines:** chat2data (no knowledge) and RAG2data (vector DB instead of the KG). No fine-tuning.

## Results (key numbers and metrics)
| System | Name-recognition failure | Hallucination-recognition failure | API-call accuracy |
|---|---|---|---|
| KG2data | 1.43% | 0% | 88.57% |
| RAG2data | 16% | 10% | 72.14% |
| chat2data | 7.14% | 8.57% | 71.43% |

## Limitations
Small benchmark (70 test cases, 35 tools), which the authors acknowledge limits statistical power. Virtual rather than production APIs. Manuals are undisclosed and Chinese-language. A single LLM backbone. KG quality depends on LLM extraction.

## Transferable ideas for the FYP pipeline
- **Text/RAG/KG:** build a TruLaser knowledge graph from the operating manual and troubleshooting tables. Example entities: defect (burr, dross, incomplete cut), cause (focus position, gas pressure, nozzle damage, lens contamination), parameter, component, remedy. Example relations: causes, indicates, adjusted_by. Use LLM extraction with few-shot schema examples and store in Neo4j.
- **Hybrid retrieval:** combine multi-hop graph traversal (defect → cause → parameter) with vector search over manual chunks.
- **Tool use / tabular:** expose machine-database queries (SQL over job tables, alarm logs) as tools for a ReAct agent. The KG helps map operator language to the correct table and column names. This cuts hallucinated field names.
- **Evaluation:** use the three metrics directly: entity/name-recognition failure, hallucination rate and tool-call accuracy, with ablations without knowledge and with vector RAG.
