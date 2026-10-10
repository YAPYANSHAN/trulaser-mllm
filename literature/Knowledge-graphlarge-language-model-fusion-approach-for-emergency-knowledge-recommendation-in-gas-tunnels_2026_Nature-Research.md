# Knowledge graph-large language model fusion approach for emergency knowledge recommendation in gas tunnels

- **Citation (IEEE):** N. Xu, X. Chen, J. Luo, et al., "Knowledge graph-large language model fusion approach for emergency knowledge recommendation in gas tunnels," *Scientific Reports*, vol. 16, art. 11438, 2026, doi: 10.1038/s41598-026-39204-0.
- **Domain:** Engineering safety / KG-augmented LLM decision support
- **Relevance to FYP (1-5):** 4 - a small, locally deployed KG-RAG system over manuals and case records for an engineering domain, evaluated with both NLP metrics and expert ratings; closely matches the documentation/RAG branch of the FYP.

## Problem
In gas-tunnel emergencies, relevant knowledge is fragmented across unstructured reports, manuals and case records; standalone LLMs hallucinate and fine-tuning is costly and opaque.

## Data & modalities
Text: heterogeneous emergency documents (plans, manuals, accident case records). KG built from them: 435 nodes and 1,568 relationship edges from 1,568 extracted triples. Test set: 50 QA pairs across scenario types (e.g., gas outburst, fire, ventilation failure, trapped workers, sensor failure, cascading multi-hazard events) with reference answers from actual case decisions.

## Method
(1) KG construction: prompt-optimised LLM extracts entity-relation triplets from document fragments. (2) Inference: entities/relations embedded as vectors; query keywords extracted by the LLM; semantic cosine-similarity vector search retrieves the most relevant subgraph; candidates are re-ranked; the subgraph augments the prompt. Base LLM Qwen-14B served locally via Ollama on consumer-grade CPU/GPU; temperature 0.05, top_p 0.8. No fine-tuning. Framework also run with ChatGLM-6B and Llama2-7B as alternative base models; compared against native Qwen-14B and GPT-4o.

## Results
Proposed (Qwen-14B + KG): BLEU 0.47, ROUGE-1 0.63, ROUGE-2 0.51, ROUGE-L 0.52, cosine similarity (CS, 384-d sentence embeddings) 0.83; weighted expert score 4.665/5 (accuracy 4.75, completeness 4.6, coherence 4.8, speed 4.15). Native Qwen-14B: CS 0.10, weighted 2.49. GPT-4o (no KG): CS 0.29, weighted 4.45. With KG, ChatGLM-6B reached CS 0.79 and Llama2-7B 0.80, showing the gain comes mainly from retrieval. Retrieval adds latency (lower speed score).

## Limitations
Bespoke, small dataset (50 test QAs) underrepresenting rare high-consequence events; no ablation of which LLM is best as knowledge extractor; real-time performance and user-centred interpretability need work; text only (multimodal data planned); data available only on request; small evaluator panel (10 users).

## Transferable ideas for the FYP pipeline
- **Text/RAG:** build a compact KG from TRUMPF TruLaser manuals, troubleshooting tables and maintenance logs via LLM triple extraction, then retrieve and re-rank subgraphs per fault query.
- **Deployment:** a local 7-14B open model (Ollama) plus KG can rival or beat GPT-4o on domain QA - attractive for on-premise factory data; use low temperature for deterministic recommendations.
- **Evaluation:** combine BLEU/ROUGE/embedding-cosine against expert reference answers with weighted Likert criteria (accuracy, completeness, coherence, speed) by practitioners and researchers; include "native LLM" and "GPT-4o without retrieval" baselines.
- **LLM reasoning:** structure outputs along required dimensions (hazard, safety, equipment, communication) - analogous to fault, cause, parameter adjustment, safety note.
