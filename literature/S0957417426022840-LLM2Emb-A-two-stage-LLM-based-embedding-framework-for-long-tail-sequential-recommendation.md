# LLM2Emb: A two-stage LLM-based embedding framework for long-tail sequential recommendation

- **Citation (IEEE):** Z. Zhang, X. Yang, W. Luo, et al., "LLM2Emb: A two-stage LLM-based embedding framework for long-tail sequential recommendation," *Expert Systems With Applications*, vol. 331, Art. no. 133375, 2026, doi: 10.1016/j.eswa.2026.133375.
- **Domain:** Recommender systems / representation learning with LLM embeddings
- **Relevance to FYP (1-5):** 1 - e-commerce recommendation; only the idea of fusing sparse-ID and LLM-text embeddings with a gate transfers loosely.

## Problem
Sequential recommenders learn item ID embeddings from interaction logs, so rarely-seen (long-tail) items get poorly trained embeddings. LLM text embeddings capture semantics but ignore collaborative-filtering (CF) signals, and existing methods do not balance the two representation types across head vs. tail items.

## Data & modalities
Three real-world datasets (Amazon Baby, Amazon Movies, Yelp) with user-item interaction sequences plus textual item attributes/descriptions. Text + interaction IDs only; no images or sensor data.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Stage 1, Attribute-level Collaborative Contrastive Tuning (ACCT): an LLM (LLaMA2-7B; Qwen2 variants also tested) is LoRA-fine-tuned with contrastive learning over co-occurring item pairs, injecting collaboratively retrieved item information into the item embeddings.
- Stage 2, adapter framework: a cross-attention user-preference module re-weights attribute-level LLM embeddings with user representations, aligning the semantic and behavioural spaces.
- A popularity-gated network with popularity-aware regularisation adaptively fuses ID and LLM embeddings, so tail items lean on LLM semantics.
- Plugged into sequential backbones (SASRec, BERT4Rec, etc.; four backbones in total).

## Results (key numbers and metrics)
Consistently beats LLM-based and ID-only baselines on NDCG@k and HR@k, with the largest gains on long-tail items. On the low-quality Amazon Baby dataset the NDCG@k and HR@k improvements exceed 10%.

## Limitations
- No noise detection or attribute validation, so erroneous descriptions can propagate.
- ACCT has non-trivial compute cost even with LoRA.
- The popularity gate is static at inference.
- Future work: confidence-aware gating, LLM-based attribute completion, and distilled or quantized LLMs.

## Transferable ideas for the FYP pipeline
- **Fusion:** a learned gate that weights a "data-rich" representation (e.g., a classifier trained on frequent machine-table fault codes) against an LLM-semantic representation (from documentation text) by how often each fault class occurs. Rare TruLaser fault codes would rely more on documentation semantics.
- **Text/RAG:** LoRA-contrastive tuning of an embedding LLM on co-occurring pairs (e.g., alarm codes that co-occur in machine logs) could improve retrieval embeddings for alarm and manual passages.
- **Evaluation:** report performance stratified by class frequency (head vs. tail faults), not only overall accuracy.
