# A Global-Context Vision Transformer for Facial Age Estimation

- **Citation (IEEE):** G. Maroun, S. E. Bekhouche, J. Charafeddine, et al., "A Global-Context Vision Transformer for Facial Age Estimation," *Cognitive Computation*, vol. 18, art. 72, 2026, doi: 10.1007/s12559-026-10605-7.
- **Domain:** Computer vision / facial analysis (image regression)
- **Relevance to FYP (1-5):** 2 - unrelated domain, but the local-global ViT backbone and region-replacement augmentation are transferable to fine-texture defect imaging (dross, striations) under limited data.

## Problem
Estimating chronological age from one face image is hard because ageing cues are subtle, non-linear and confounded by identity, pose, illumination and demographics. Pure transformers are under-explored for this task, which needs both fine local texture (wrinkles) and global structure.

## Data & modalities
Single modality (RGB face images). Benchmarks: MORPH II, IMDB-Clean, AFAD, UTKFace; zero-shot cross-dataset transfer evaluation. Inputs at 224x224.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Backbone: GC-ViT (Global Context Vision Transformer, Small), hierarchical 4-stage encoder with convolutional 7x7 stride-4 patch stem, windowed local self-attention plus global-context tokens at each stage.
- Lightweight MLP regression head for scalar age; no auxiliary CNN branch, no test-time post-processing.
- Composite loss: MAE plus a secondary stabilising term (MSE or SmoothL1, dataset-dependent), warmup-cosine LR schedule.
- Age-aware Region Replacement (ARR) augmentation: semantically defined facial regions replaced with age-proximal donor content (or self-flipped content), blended with a feathered mask and area-proportional soft-label interpolation.
- Optional pretraining on IMDB-Clean then fine-tuning. No LLM/VLM, RAG or LoRA.

## Results (key numbers and metrics)
- MAE 2.41 on MORPH II, 3.11 on AFAD, 4.26 on UTKFace (AFAD/UTKFace fine-tuned from IMDB-Clean pretraining); also Pearson correlation and CS@5/CS@10 reported.
- Consistently better than vanilla ViT baseline; competitive with recent transformer methods.
- Zero-shot cross-dataset MAE in the same range as ResNet/FaRL baselines but with substantial degradation in several transfer directions.

## Limitations
- Accuracy-oriented, large model; not deployment-optimised.
- Trained/validated only at 224x224; test-time resolution scaling unreliable.
- Strong performance drops under domain shift and with narrow/biased training data; fairness/calibration not yet studied.

## Transferable ideas for the FYP pipeline
- **Vision:** a local-global attention backbone (GC-ViT / Swin-style) suits cut-edge images where fine striation/dross texture and global part geometry both matter; could serve as the image encoder for defect classification or severity regression (e.g., roughness, burr height).
- **Vision / data ingestion:** region-replacement augmentation with soft-label interpolation can be adapted to paste defect regions (burr, dross) onto clean cut-edge images to enlarge scarce defect classes.
- **Evaluation:** report cross-condition (material/thickness) zero-shot transfer separately, mirroring the cross-dataset protocol, to quantify domain shift between machine settings.
- **Tabular / regression:** composite MAE+SmoothL1 loss is a simple robust choice for regressing continuous quality metrics.
