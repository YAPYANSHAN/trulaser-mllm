# Few-shot cross-episode adaptive memory for metal surface defect semantic segmentation

- **Citation (IEEE):** J. Zhang, H. Ding, M. Peng, et al., "Few-shot cross-episode adaptive memory for metal surface defect semantic segmentation," *Sci. Rep.*, vol. 16, art. 5660, 2026, doi: 10.1038/s41598-026-36445-x.
- **Domain:** Industrial visual inspection — few-shot semantic segmentation of metal surface defects
- **Relevance to FYP (1-5):** 3 — metal surface defects with very few labelled samples, which matches the FYP's likely scarcity of labelled laser-cut defect images. Purely a vision method, with no LLM, tabular data or reasoning.

## Problem
Defect segmentation networks need large pixel-annotated datasets and do not transfer to unseen defect classes. Existing few-shot segmentation (FSS) methods learn within single episodes, overfit to episode-specific cues (e.g., the brightness of a scratch) and produce coarse masks.

## Data & modalities
Public benchmarks:
- **Surface Defect-4i:** 12 metal-surface defect classes.
- **FSSD-12:** 12 strip-steel defect classes.

RGB/grey images with pixel masks. 3-fold cross-validation over disjoint class splits (train on 2 folds of classes, test on unseen classes), with 1-shot and 5-shot settings and five random-seed trials.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
EAMNet, built on a ResNet-50 or VGG-16 backbone with 4-level features:
- **Episode Adaptive Memory Unit (EAMU):** an adaptive factor models semantic dependencies across training episodes, acting as cross-episode memory.
- **Context Adaptation Module (CAM):** aggregates hierarchical support–query features for fine-grained masks.
- **Global Response Mask Average Pooling (GRMAP):** applies ConvNeXt-v2-style global response normalisation to the support prototype.
- **Attention Distillation (AD):** transfers high-resolution semantic attention to stabilise cross-episode learning.

Implemented in PyTorch: 200 episodic epochs, learning rate 1e-4, trained on 4× RTX 3090.

## Results (key numbers and metrics)
- Surface Defect-4i (VGG-16): mIoU 35.13% vs. 23.08% for the baseline. Beats the previous SOTA, MAPTNet, by +4.43 (1-shot) and +5.89 (5-shot) mIoU points.
- FSSD-12 (ResNet-50): +1.92 mIoU over MAPTNet (1-shot) and +0.73 over HDMNet (5-shot).
- 54.47 GFLOPs (lightweight).
- Ablations support each module. Code and data are on Zenodo.

## Limitations
Absolute mIoU remains modest. Fails on subtle, low-contrast defects against background texture. Benchmarks are curated public datasets, not production lines. Segmentation only, with no causal or diagnostic output.

## Transferable ideas for the FYP pipeline
- **Vision (low-label regime):** few-shot segmentation lets the FYP add new laser-cut defect types (e.g., bevel-edge gouging, micro-joint failure) from 1–5 annotated examples, without retraining a detector from scratch.
- **Vision → reasoning:** pixel masks give quantitative evidence such as defect area, location along the contour and extent along the bevel. These can be passed to the LLM as structured facts, which is more reliable than asking a VLM to estimate sizes.
- **Evaluation:** use class-disjoint folds to test generalisation to unseen defect types, report mIoU/FB-IoU with multiple seeds, and analyse low-contrast failure cases.
- **Data ingestion:** pretraining on public metal-defect datasets (Surface Defect-4i, FSSD-12, NEU) can bootstrap the vision module before fine-tuning on TruLaser images.
