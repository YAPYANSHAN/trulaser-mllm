# Composite Material Surface Microscopic Defect Detection and Classification Combining Diffusion Models and Zero-Shot Learning

- **Citation (IEEE):** W. Fan, "Composite material surface microscopic defect detection and classification combining diffusion models and zero-shot learning," *Scientific Reports*, vol. 16, art. 388, 2026, doi: 10.1038/s41598-025-29871-w.
- **Domain:** Industrial surface-defect detection (composites; tested on steel/texture benchmarks) / generative + zero-shot learning
- **Relevance to FYP (1-5):** 3 - manufacturing defect detection with scarce labels and unseen defect types via text-attribute descriptions; no LLM reasoning, but the attribute-based zero-shot and diffusion augmentation ideas suit rare laser-cut defects.

## Problem
Microscopic surface-defect detection on composite materials suffers from scarce labelled data and new defect types that supervised detectors cannot recognise; complex textures cause errors.

## Data & modalities
Images (512x512 input) from benchmark datasets NEU-DET, DAGM 2007 and MVTec AD, plus evaluation across different composite matrix materials. Text attribute descriptions of defect types (shape, texture, boundary features, etc.).

## Method
Dual-path architecture trained jointly. (1) Diffusion path: improved conditional denoising diffusion probabilistic model (U-Net encoder-decoder with self-attention bottleneck, conditional and time embeddings, mask guidance) to learn defect distributions and synthesise defects; LoRA-style adaptive adjustment. (2) Zero-shot path: ViT-B/16 (86M) visual encoder and BERT-base (110M) encoder of attribute descriptions, projected to a shared 512-d L2-normalised embedding space; attribute prompt module; meta-learning for adaptive attribute weights. (3) Multi-level fusion via cross-attention and gating across 128/64/32 resolutions, then classification and localisation heads.

## Results
mAP@50 0.777, recall 0.745, inference 140.5 ms per image. Zero-shot (no labels) F1 0.692, reported as equivalent to a supervised method trained with 500 labelled samples. Ablation: LoRA adaptation raised F1 from 0.627 to 0.661; with mask guidance and attribute prompts F1 reached 0.738 and FID fell to 22.4. Good generalisation across composite matrix materials is claimed.

## Limitations
Detection errors remain in very complex texture backgrounds; limited coverage of material types; dependence on pre-trained model domain adaptability; shallow integration with physical modelling; does not yet exploit the common case of a few labels plus unseen classes (semi-supervised extension proposed).

## Transferable ideas for the FYP pipeline
- **Vision:** define each laser-cut defect by interpretable attributes (shape, location on edge, texture, colour/oxidation, boundary) encoded as text; match image embeddings to attribute embeddings to recognise defect types with no or few photos.
- **Data ingestion:** conditional diffusion (with masks) to synthesise rare defect images (e.g. bevel-specific burn-outs) for training/validation of the vision branch.
- **Fusion:** cross-attention + gating between visual and semantic features at multiple scales.
- **LLM reasoning:** attribute vectors give human-readable evidence ("irregular boundary, droplet texture at bottom edge") that an LLM can cite when explaining a diagnosis.
- **Evaluation:** report mAP@50, recall, F1 for zero-shot classes and per-image latency.
