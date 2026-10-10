# A comprehensive survey on deep learning approaches for image captioning: a systematic review

- **Citation (IEEE):** M. A. Al-Malla, O. Hamdoun, and N. Ghneim, "A comprehensive survey on deep learning approaches for image captioning: a systematic review," *Journal of Big Data*, vol. 13, art. 48, 2026, doi: 10.1186/s40537-026-01377-w.
- **Domain:** Computer vision + NLP / image captioning (systematic review)
- **Relevance to FYP (1-5):** 2 - general captioning survey; useful background on VLP models, captioning metrics and hallucination, but no industrial or diagnostic focus.

## Problem
Provide an updated, structured synthesis of whole-image captioning methods published 2018 to August 2025, compare them, and identify open challenges.

## Data & modalities
Image + text. Reviews 174 peer-reviewed studies. Benchmarks discussed: MS COCO (Karpathy split), Flickr30K, Conceptual Captions, Visual Genome. Metrics: BLEU, METEOR, ROUGE-L, CIDEr, SPICE, CHAIR, CLIPScore, BERTScore.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Systematic review with a nine-category taxonomy: attention-based (23 studies), graph-based (22), attention+graph (19), CNN-based (7), transformer-based (28), transformer+graph (3), vision-language pretraining (24; e.g., OSCAR, OFA, BLIP-2, ClipCap, Flamingo, PaLI), unsupervised/RL (14; e.g., self-critical sequence training), and other specialised techniques including controllable and multi-style captioning (34). Covers encoder choices (CNN grids, bottom-up region features, ViT), scene graphs for relationships, and the growing role of LLMs/MLLMs.

## Results (key numbers and metrics)
- Transformer-based and VLP methods consistently achieve the highest CIDEr and SPICE; top architectures often exceed CIDEr 130 on the COCO Karpathy test split.
- Graph-based and attention-augmented models improve substantially over CNN-RNN baselines in complex scenes.
- Persistent challenge: visual-semantic (object) hallucination; n-gram metrics favour syntactic similarity over semantic correctness.

## Limitations
Survey only (no new experiments); focuses on whole-image captioning (excludes dense captioning); comparisons rely on reported numbers mostly on MS COCO, a general-domain benchmark.

## Transferable ideas for the FYP pipeline
- **Vision / text:** treat defect description as a domain captioning task; VLP models (BLIP-2-style Q-Former, ClipCap-style prefix mapping) offer lightweight ways to connect a frozen image encoder to an LLM.
- **Fusion:** scene-graph ideas map to representing relationships between defect regions and part features (edge, corner, pierce point) before LLM reasoning.
- **Evaluation:** go beyond BLEU/ROUGE; include CHAIR-style hallucination checks (does the report mention defects not present?), CLIPScore/BERTScore for semantic alignment, and expert review.
- **LLM reasoning:** controllable captioning ideas support templated outputs (defect type, location, severity, probable cause) for consistent diagnostic reports.
