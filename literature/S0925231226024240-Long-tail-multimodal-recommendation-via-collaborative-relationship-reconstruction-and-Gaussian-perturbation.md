# Long-tail multimodal recommendation via collaborative relationship reconstruction and Gaussian perturbation

- **Citation (IEEE):** X. Wang and X. Huang, "Long-tail multimodal recommendation via collaborative relationship reconstruction and Gaussian perturbation," *Neurocomputing*, vol. 706, Art. no. 135026, 2026, doi: 10.1016/j.neucom.2026.135026.
- **Domain:** Recommender systems (multimodal, e-commerce)
- **Relevance to FYP (1-5):** 1 — e-commerce recommendation; only the long-tail (rare class) handling ideas are loosely transferable to rare fault types.

## Problem
Multimodal recommenders use images and text to ease sparsity and cold-start, but long-tail items have too few interactions to learn collaborative signals; collaborative representations are noisy; and multimodal semantics may disagree with users' actual collaborative preferences.

## Data & modalities
User-item interaction graphs plus item images and text. Three public Amazon datasets: Baby, Sports, Clothing (high sparsity, many long-tail items; Clothing the most extreme).

## Method
CRGP (Collaborative Relationship Reconstruction and Gaussian Perturbation):
- **Semantic-guided long-tail collaborative relationship reconstruction:** uses multimodal semantic similarity to select "head" anchor items and transfers their collaborative behaviour to long-tail items.
- **Gaussian perturbation augmentation:** adaptive, sample- and dimension-specific noise on collaborative representations for robustness.
- **Semantic calibration distillation loss:** transfers collaborative preference information from the fused multimodal representation to each modality-specific representation.
- Graph-based multimodal recommendation backbone compared with representative baselines (e.g., VBPR, MGCN-style methods). No LLM.

## Results
- Consistently outperforms evaluated baselines on overall performance, long-tail item modelling and robustness.
- Up to 4.04% improvement in Recall@20 over the strongest baseline.
- Analysis: semantically selected head anchors generally have higher behavioural relevance.

## Limitations
Semantic similarity is not a sufficient condition for preference consistency or transferable behaviour; anchor selection lacks behavioural consistency measures and confidence estimation (future work); evaluated only on Amazon datasets.

## Transferable ideas for the FYP pipeline
- **Tabular/vision (rare faults):** rare fault classes on the TruLaser (e.g., lens contamination, collision damage) have few examples; borrow information from semantically similar, well-represented faults (anchor transfer), e.g., by retrieving similar common cases as context or few-shot examples.
- **Fusion:** a distillation loss aligning each modality's embedding with the fused embedding could keep image and table encoders consistent with the overall diagnosis.
- **Robustness:** adaptive Gaussian feature perturbation as a cheap augmentation for small industrial datasets.
