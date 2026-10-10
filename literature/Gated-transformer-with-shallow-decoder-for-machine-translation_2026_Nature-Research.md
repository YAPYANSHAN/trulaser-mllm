# Gated transformer with shallow decoder for machine translation

- **Citation (IEEE):** F. Li, F. Yin, S. Deng, et al., "Gated transformer with shallow decoder for machine translation," *Scientific Reports*, vol. 16, art. 19069, 2026, doi: 10.1038/s41598-026-49583-z.
- **Domain:** NLP / neural machine translation; efficient Transformer architecture.
- **Relevance to FYP (1-5):** 1 — unrelated task; only the general lesson about deep-encoder/shallow-decoder efficiency trade-offs for latency-constrained deployment is loosely transferable.

## Problem
LLMs translate well but are too costly for latency-critical or resource-constrained deployment, and linear-attention Transformer variants only help on very long texts, not short sentences typical of MT. The authors seek a simple, efficient Transformer for short-text translation.

## Data & modalities
Text only: WMT14 English-German and WMT14 English-French (36M sentence pairs); additional cross-domain (TED talks) and low-resource (10% of WMT en-fr) tests. Metric: BLEU, per-sentence latency, speedup; NVIDIA Tesla V100S, beam size 4.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Gated Transformer with Shallow Decoder (GTSD): an Attention-FFN fusion block (AFF) using a gating mechanism (GLU-inspired) to combine attention and feed-forward network; replaces multi-head with single-head attention and optimises the resulting redundant cross-attention; deep encoder + shallow decoder (configurations 15-6, 21-3, 24-1). Compared with baseline Transformer, AAN, SAN, ACN, LightFormer, LightTransformer and zero-shot NLLB (3.3B). No RAG, no LLM fine-tuning.

## Results (key numbers and metrics)
WMT14 en-de: baseline 27.31 BLEU (4.88 ms, 65M); GTSD21-3 27.64 BLEU, 4.03 ms, 1.21x speedup, 70M; GTSD24-1 25.79 BLEU, 1.59x; NLLB 29.11 BLEU but 0.05x speed. WMT14 en-fr: baseline 37.96; GTSD21-3 39.04 BLEU, 1.34x speedup; GTSD15-6 38.99; NLLB 40.97 at 0.05x. Ablation: removing gating lowers BLEU. A single-layer decoder degrades quality by ~1-1.5 BLEU.

## Limitations
Weaker on long-form and cross-domain data (TED talks); strong dependence on data scale (large drop when trained on 10% data); evaluated only on two language pairs.

## Transferable ideas for the FYP pipeline
- **Deployment:** Report a quality-vs-latency table (like Table 2) comparing a small local model against a large LLM, to justify which model runs on the shop-floor edge device versus cloud.
- **Fusion (minor):** Gated combination of sub-module outputs is a cheap way to improve small task-specific models (e.g., a lightweight alarm-text classifier used as a pre-filter before the multimodal LLM).
- **Evaluation:** Include low-data and cross-domain tests (e.g., new material or sheet thickness) to show robustness rather than only in-distribution scores.
