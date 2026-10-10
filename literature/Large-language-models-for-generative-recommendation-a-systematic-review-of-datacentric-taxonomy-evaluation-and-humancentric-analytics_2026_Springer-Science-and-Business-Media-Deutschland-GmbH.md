# Large language models for generative recommendation: a systematic review of data-centric taxonomy, evaluation, and human-centric analytics

- **Citation (IEEE):** T. Saeed and B. Wang, "Large language models for generative recommendation: a systematic review of data-centric taxonomy, evaluation, and human-centric analytics," *International Journal of Data Science and Analytics*, vol. 22, art. 130, 2026, doi: 10.1007/s41060-026-01106-9.
- **Domain:** Recommender systems / NLP - systematic review
- **Relevance to FYP (1-5):** 1 - consumer recommender systems; only generic LLM-adaptation techniques (prompting, RAG, LoRA, RLHF) are loosely transferable.

## Problem
How LLMs transform recommender systems from static ranking into generative, explainable, conversational recommendation; which mechanisms, techniques, datasets and evaluation practices are used; and what challenges remain.

## Data & modalities
Review of over 110 peer-reviewed and preprint studies (2019-2025) via a PRISMA 2020 pipeline. Datasets discussed: Amazon, Goodreads, MovieLens, BookGPT, APIGen, DimeRec. Modalities: text, graphs, user-behaviour sequences, some multimodal content.

## Method
Systematic review with five research questions. Proposes a three-family taxonomy: Sequence-Driven Generative Systems (SDGS), Knowledge-Driven (KDGS, e.g., RAG/KG grounding) and Creativity-Driven (CDGS, multimodal/creative synthesis). Maps enabling techniques - prompting and in-context learning, retrieval-augmented generation, parameter-efficient fine-tuning (LoRA), reinforcement learning/RLHF - to empirical trends; compares with traditional and deep-learning recommenders and previous surveys.

## Results
Qualitative synthesis: LLM-based recommenders show relative improvements in personalisation, semantic grounding, diversity, dialogue ability and user trust over collaborative filtering and transformer baselines, at the cost of high computation/latency and fairness and sparsity-robustness issues. No pooled quantitative numbers.

## Limitations
Narrative synthesis without meta-analysis; heterogeneous metrics across studies; includes preprints; domain (e-commerce, media, jobs, news) far from manufacturing.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** the "knowledge-driven generation" family (RAG/KG grounding plus generated rationale) is the relevant pattern for recommending process-parameter changes with explanations.
- **Fine-tuning:** LoRA is presented as the standard low-cost way to adapt an LLM to a domain - applicable if a small laser-cutting instruction dataset is created.
- **Evaluation:** recommendation-style metrics (ranking of candidate fixes, e.g., hit@k of the correct remedy among suggestions) and human-centric measures (trust, perceived usefulness) could assess the optimisation advice.
- **Governance:** transparency and bias audits; hybrid retrieval-generation to balance grounding and fluency.
