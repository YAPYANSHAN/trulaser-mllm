# Toward intelligent clinical support for personalized sport training rehabilitation via large language models

- **Citation (IEEE):** S. Wang, Z. Bai, and Y. Gai, "Toward intelligent clinical support for personalized sport training rehabilitation via large language models," *Health Information Science and Systems*, vol. 14, Art. no. 17, 2026, doi: 10.1007/s13755-025-00416-9.
- **Domain:** Health informatics / recommender systems (LLM text + sequence fusion)
- **Relevance to FYP (1-5):** 2 - unrelated domain using proxy data. The transferable idea is fusing LLM text embeddings with a Transformer over temporal logs through cross-attention.

## Problem
Rehabilitation exercise prescriptions should adapt to each patient's changing symptoms and adherence. Existing recommenders use either numerical logs or handcrafted rules and ignore free-text feedback (e.g., "my knee clicks when I squat"). The goal is to combine text with temporal behaviour when data is sparse.

## Data & modalities
Two public recommendation datasets used as proxies: Epinions and Amazon Sports & Outdoors. Products are mapped to exercises, reviews to patient feedback, and ratings to tolerance scores. Modalities are free text plus chronological interaction sequences. There are no real physiological or clinical data.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
"ReLite" (also called RehabGPT-Lite):
1. A semantic encoder: a fine-tuned LLM-style text encoder (hidden size 768) over reviews.
2. A lightweight Transformer sequence encoder (2 layers, 4 heads) over session histories.
3. Multi-head cross-attention that aligns text embeddings with the rating sequence.
4. A dual-head MLP that outputs continuous and ordinal tolerance scores.

Attention heat-maps are used for interpretability. Baselines: NGCF, NegAIT, XLNet, Transformer, BERT, CPSRP, RoBERTa, GPT-3, GPT-4 and prompting.

## Results (key numbers and metrics)
| Model | Epinions acc / prec / F1 | Sports acc / prec / F1 |
|---|---|---|
| ReLite | 71.08 / 68.45 / 69.58 | 73.55 / 71.92 / 72.21 |
| GPT-4 (best baseline) | 67.86 / 66.05 / 68.11 | 70.22 / 71.56 / 70.77 |

The authors report that GPT-4 tops precision on both datasets, though in the table ReLite's precision is slightly higher. Ablation and attention analyses support the cross-attention fusion.

## Limitations
- Proxy datasets with no real physiological signals or clinical outcomes.
- The introduction says plans were "verified by licensed physiotherapists", but the limitations section says the generated prescriptions and justifications have *not* been systematically evaluated by clinicians.
- No user studies.
- Gains over GPT-4 are modest (about 2-3 points).

## Transferable ideas for the FYP pipeline
- **Fusion:** cross-attention between text embeddings (operator notes, alarm messages, maintenance logs) and a Transformer encoding of the machine-event sequence (job history, parameter changes, error codes). This links symptoms reported in text with temporal process data.
- **Output:** dual heads, one regressing a continuous quality or severity score and one classifying an ordinal severity level, for both precise and actionable output.
- **Evaluation:** compare against general LLM baselines (GPT-4-style prompting) as well as classic ML. Be careful not to claim expert validation unless it was actually done.
- **Data:** proxy datasets can bootstrap development, but real laser data is needed for any claim of applicability.
