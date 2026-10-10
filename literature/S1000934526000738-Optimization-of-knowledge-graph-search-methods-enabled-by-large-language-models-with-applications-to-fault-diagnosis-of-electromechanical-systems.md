# Optimization of knowledge graph search methods enabled by large language models with applications to fault diagnosis of electromechanical systems

- **Citation (IEEE):** H. Zhang, W. Wang, S. Shao, et al., "Optimization of knowledge graph search methods enabled by large language models with applications to fault diagnosis of electromechanical systems," *Chinese Journal of Mechanical Engineering*, vol. 39, Art. no. 100284, 2026, doi: n/a.
- **Domain:** Industrial fault diagnosis (electromechanical systems) / LLM + knowledge graph retrieval (GraphRAG)
- **Relevance to FYP (1-5):** 5 - an end-to-end LLM + KG diagnosis system. It includes VLM parsing of fault flowcharts, LoRA-tuned triple extraction, adaptive multi-hop KG search, traceable reasoning paths and hallucination metrics, all directly reusable for TruLaser documentation.

## Problem
Fault KGs for electromechanical systems are searched by keyword matching or query languages, which causes semantic ambiguity and inefficient retrieval. General LLMs lack domain adaptation and give low-credibility answers.

## Data & modalities
- **Sources:** fault reports, phenomenon/cause/troubleshooting texts (engines, motors) and fault-handling flowcharts (images).
- **FTT-DS:** an instruction dataset for triple extraction.
- **PEES-FD:** a fault-diagnosis QA dataset.
- KG stored in Neo4j with five entity types: equipment, component, phenomenon, cause, troubleshooting.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
1. **KG construction:**
   - Text is split into single-relation sentences; prompt templates and few-shot examples drive a fine-tuned LLM to extract triples.
   - VLMs (Qwen-VL, GLM-4V) detect boxes, diamonds and arrows in flowcharts, OCR the text, and rebuild "box-arrow-box" logic into descriptive text.
   - Experts manually verify all triples.
2. **Fine-tuning:** LoRA on a domain QA dataset. Updating about 0.5-1% of parameters worked best; more than 1% risked degradation.
3. **Entity extraction:** the LLM simulates the user query and generates a hypothetical answer document (HyDE-like) to extract more relevant entities, followed by entity alignment.
4. **Query-complexity metric:** an LLM scores the number of entities, relation hierarchy and constraints, then dynamically sets the hop count k and search scope s.
5. **Answering:** reasoning paths are scored for relevance, and the LLM answers from the best path while also outputting the subgraph and path for traceability.
6. **Base models compared:** Qwen2.5 (1.5B-32B), ChatGLM3-6B, GLM-4 and DeepSeek-R1. DeepSeek-R1 was best at extraction; Qwen2.5-14B and GLM-4 were used as bases.

## Results (key numbers and metrics)
- **Triple extraction:** F1 above 0.698 for multi-entity queries (within 5% of single-entity queries); entity alignment accuracy above 85%.
- **Adaptive retrieval:** cuts response time by 72.6% on low-complexity queries (M3eScore above 0.73).
- **High-complexity queries:** APLS 0.850 and answer similarity 0.839, vs. 0.681 for TOG and 0.639 for GraphRAG.
- **Reasoning-path integrity:** above 92%.
- **Hallucination test (100 samples):**

  | Method | Hallucination rate | KG match degree | Confidence pass rate |
  |---|---|---|---|
  | GraphRAG | 27.8% | 0.61 | 51.9% |
  | TOG | 12.4% | 0.77 | 67.5% |
  | LLM-KGSO | 3.9% in table (3.7% in text) | 0.93-0.94 | 93.2% |

- Beats GraphRAG and TOG on both accuracy and time, with GLM-4 or Qwen2.5 as the base model.

## Limitations
- Relies on manual expert verification of the KG.
- Queries outside the dataset fall back to the LLM's internal knowledge, which is random and unreliable; this case is not evaluated.
- Text-similarity metrics dominate the evaluation.
- Fine-tuning above 1% of parameters degrades performance.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** use Qwen-VL or GLM-4V to parse TRUMPF manual flowcharts and troubleshooting tables into text, then into triples (equipment, component, phenomenon, cause, remedy). Keep a human verification step.
- **Text/RAG:** HyDE-style query expansion plus complexity-adaptive k-hop retrieval over a laser-cutting KG.
- **LLM reasoning:** return the answer together with the KG path and subgraph as evidence, which is required for "evidence-based diagnosis".
- **Fine-tuning:** small LoRA (0.5-1% of parameters) on a domain QA set.
- **Evaluation:** adopt the hallucination rate (HR), KG match degree (KGMD) and confidence pass rate (CS), and compare against GraphRAG and ToG baselines.
