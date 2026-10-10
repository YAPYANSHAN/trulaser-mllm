# A survey of transformer and LLM-based architectures, workflows, and systems in drug discovery

- **Citation (IEEE):** S. Tsimenidis, E. Vrochidou, and G. A. Papakostas, "A survey of transformer and LLM-based architectures, workflows, and systems in drug discovery," *Journal of Computer-Aided Molecular Design*, vol. 40, art. 205, 2026, doi: 10.1007/s10822-026-00911-5.
- **Domain:** Drug discovery / transformers and LLMs (survey)
- **Relevance to FYP (1-5):** 2 - pharmaceutical domain; useful only for generic architectural patterns (transformer encoders for multimodal fusion, LLM agents with tools, RAG to cut hallucination).

## Problem
Survey how transformers and LLMs are used across drug-discovery tasks (target identification, molecule design, drug-target interaction, potency, synthesis planning, side effects) and which architectures, workflows and systems integrate them.

## Data & modalities
Molecular sequences (SMILES), protein sequences/structures, graphs, biomedical text, tabular assay and clinical data, images, time series; public chemical/biological databases.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Narrative review organised by:
- Transformer architectures: encoder-only (BERT-type representation), decoder-only (generative GPT-type), encoder-decoder (seq2seq, e.g., reaction prediction, BART/T5), plus hybrids with GNN/GCN/MLP and state-space models.
- Roles: predictive (classification/regression), generative (de novo design guided by RL and multi-objective optimisation), representation (embeddings for downstream models).
- LLM categories: chemical language models; LLMs combining molecular data and text or operating in text mode; LLM-based agentic systems with tools, database integration and chain-of-thought monitoring.
- Multimodal fusion via hierarchical feature extraction and concatenation (e.g., transformer + GCN + MLP for drug synergy).
- Notes evolution to multimodal LLMs (GPT-4, GPT-4o) and reasoning models (OpenAI-o1, DeepSeek-R1).

## Results (key numbers and metrics)
No new experiments; qualitative synthesis concluding transformers are highly flexible and applicable at every stage of drug development.

## Limitations
High computational cost of large models (hindering local deployment); hallucination; complex multimodal data pipelines; black-box behaviour requiring external validation; difficulty updating knowledge (fine-tuning expensive).

## Transferable ideas for the FYP pipeline
- **Fusion:** the review's multimodal pattern (separate encoders per modality, hierarchical feature extraction, concatenation to an MLP head) is a baseline for fusing tabular machine parameters, image embeddings and text embeddings before or alongside LLM reasoning.
- **Data ingestion:** prune modalities/features that do not add predictive power to keep pipelines simple; automate and standardise preprocessing.
- **LLM reasoning:** agentic design where the LLM calls tools (SQL query, defect classifier, document retriever) and logs its chain of thought for auditing.
- **Deployment:** prefer parameter-efficient fine-tuning and smaller models for local deployment; use RAG rather than repeated fine-tuning to keep machine documentation up to date.
