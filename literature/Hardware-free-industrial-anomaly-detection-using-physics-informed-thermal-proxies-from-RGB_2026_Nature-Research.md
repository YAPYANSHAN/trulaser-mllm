# Hardware free industrial anomaly detection using physics informed thermal proxies from RGB

- **Citation (IEEE):** H. Chanda and N. Sultana, "Hardware free industrial anomaly detection using physics informed thermal proxies from RGB," *Scientific Reports*, vol. 16, art. 29435, 2026, doi: 10.1038/s41598-026-59103-8.
- **Domain:** Industrial visual inspection / unsupervised surface anomaly detection with CLIP + physics priors.
- **Relevance to FYP (1-5):** 3 — industrial RGB defect detection with frozen CLIP patch features and memory-bank kNN, useful as an unsupervised vision front end; but no LLM, and its physics proxy explicitly fails on specular metals like laser-cut sheet.

## Problem
Thermal infrared imaging reveals subsurface/material defects but calibrated cameras are expensive, so most lines use RGB only. The paper derives a synthetic thermal proxy from RGB to bring thermal-like cues to standard cameras.

## Data & modalities
RGB images. MVTec AD (5,354 images, 15 categories) for training/testing; VisA (10,821 images, 12 classes) for zero-shot cross-dataset evaluation; MulSen-AD lock-in thermography used only to validate the proxy.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Under thermal equilibrium and Lambertian assumptions, Kirchhoff's law gives emissivity proxy eps = 1 - L (luminance). ThermalCLIP fuses three streams per 14x14 patch: frozen CLIP ViT-B/16 patch features; multiscale PDE Laplacian residuals of the thermal map at scales {1,2,4} (heat-diffusion pattern disruptions); and a CausalEncoder trained with brightness intervention to disentangle four physical factors (128-d). Combined 2,433-d descriptor stored in a per-category memory bank (mean 430 MB), scored by k=5 nearest neighbours; patch scores upsampled for localisation. Compared with PatchCore, PaDiM, STFPM, CFlow-AD, WinCLIP, etc. under a unified re-implementation. No text prompting or LLM.

## Results (key numbers and metrics)
Proxy vs real thermography: polarity-corrected mean Pearson r = 0.4805, r > 0.78 on Lambertian surfaces. MVTec AD mean image AUROC 0.9441 (+2.72% over STFPM), pixel AUROC 0.9513 (STFPM 0.9595). Grid: 0.9942 vs PatchCore 0.6817. WinCLIP (text-prompt scoring) only 0.4857. VisA zero-shot: image AUROC 0.8724, pixel 0.9164. Ablation: Full and CLIP-only both 0.9442 mean (physics modules change AUROC by at most +/-0.0004); PDE-only 0.5934. Physics module overhead ~2 ms; seed SD 0.0013.

## Limitations
Approximation large-error on polished/specular metals and coatings; physics streams add no measurable AUROC on MVTec beyond CLIP; large memory bank; baselines re-implemented rather than published values; proxy only useful for emissivity-related defects.

## Transferable ideas for the FYP pipeline
- **Vision:** Frozen CLIP ViT-B/16 patch features + kNN memory bank of "good" cut parts gives an unsupervised anomaly score/heatmap for cut edges without labelled defects — a pre-screen whose heatmap can be passed to the multimodal LLM as evidence.
- **Vision (caution):** Specular steel/aluminium sheet violates the Lambertian assumption; use diffuse lighting or avoid luminance-based physics proxies for TruLaser parts.
- **Evaluation:** Note the finding that zero-shot text-prompt scoring (WinCLIP) underperforms feature retrieval on fine textures — benchmark VLM zero-shot defect judgement against a retrieval baseline.
- **Fusion:** Physics-derived features (e.g., Laplacian residuals for periodic striation patterns on cut faces) may help where appearance kNN fails on repetitive textures.
- **Evaluation:** Report image- and pixel-level AUROC plus a cross-dataset (new material/part) zero-shot test, and an honest ablation.
