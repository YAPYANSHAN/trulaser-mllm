# A study on question answering in the ceramics domain using large language models with retrieved triples and generated textual knowledge prompts

- **Citation (IEEE):** Q. Zhang, F. He, K. Hu, et al., "A study on question answering in the ceramics domain using large language models with retrieved triples and generated textual knowledge prompts," *Scientific Reports*, vol. 16, art. 21281, 2026, doi: 10.1038/s41598-026-52265-5.
- **Domain:** Domain-specific QA / KG-based RAG (ceramics, Chinese)
- **Relevance to FYP (1-5):** 4 - shows that feeding retrieved KG facts as structured triples (not prose) sharply reduces hallucination, especially for small open LLMs, which directly informs how the FYP should present machine/document evidence to the LLM.

## Problem
LLMs hallucinate in fragmented specialist domains. It is unclear whether retrieved knowledge should be given to the LLM as structured triples or as natural-language text.

## Data & modalities
Text: ceramic knowledge graph built from encyclopedias, online articles and cultural resources; Chinese ceramic QA benchmark plus the ZJQA dataset for confirmation.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Domain KG construction from heterogeneous sources.
- Retrieval: BERT-based hop prediction and path reasoning to retrieve relevant subgraphs (entity matching with cosine similarity threshold 0.7).
- Prompting: subgraph supplied either as structured triples or converted to textual descriptions.
- LLMs: GPT-3.5, GPT-4, ChatGLM2-6B, LLaMA-2-7B; additional baseline: fine-tuned LLaMA-based RAG without prompt engineering.

## Results (key numbers and metrics)
- Structured triples give the highest accuracy for all models; best ChatGLM2-6B 97.24% (97.07% on ZJQA).
- GPT-4: 95.08% with structured prompts vs 22.1% with no knowledge.
- Triples-to-text conversion lowers accuracy, largest drop LLaMA-2-7B (90.94% to 79.28%, 11.66 pp), smallest ChatGLM2-6B (2.51 pp); larger models handle text better.
- Knowledge-base retrieval accuracy 81.1%; fine-tuned RAG without prompts only 26.97% (distribution mismatch).

## Limitations
Small, single-domain Chinese dataset; text-only (no images); generalisation to other languages/domains unverified; retrieval accuracy (81.1%) bounds end-to-end performance.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** serialise retrieved evidence as compact triples/rows, e.g., (Job_123, gas_pressure, 12 bar), (Dross, caused_by, low_gas_pressure), rather than paraphrased paragraphs, particularly if using a 6-8B local model.
- **LLM reasoning:** prompt design matters more than naive fine-tuning; a well-structured evidence prompt can outperform a fine-tuned model without prompting.
- **Evaluation:** ablate no-knowledge vs text-knowledge vs triple-knowledge prompts and measure hallucination/accuracy; report retrieval accuracy separately from answer accuracy.
- **Fusion:** extend to multimodal RAG (images + KG), which the authors list as future work and the FYP can address.
