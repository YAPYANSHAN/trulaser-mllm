# A unified deep learning framework for cross-platform harmonization of multitracer PET quantification in neurodegenerative disease

- **Citation (IEEE):** J. Wang, A. Zhong, Q. Xu, et al., "A unified deep learning framework for cross-platform harmonization of multitracer PET quantification in neurodegenerative disease," *npj Digital Medicine*, vol. 9, art. 396, 2026, doi: 10.1038/s41746-026-02570-0.
- **Domain:** Medical imaging (PET-MRI / PET-CT harmonisation)
- **Relevance to FYP (1-5):** 1 - nuclear-medicine quantification; only the general idea of cross-device harmonisation and rigorous agreement statistics loosely transfers.

## Problem
Systematic biases between PET-MRI and PET-CT (mainly from MRI-based attenuation correction) prevent transfer of diagnostic thresholds and cross-site comparability for amyloid, tau and other tracers in neurodegenerative disease.

## Data & modalities
PET with paired MRI or CT anatomy. Paired same-day scans N=70 (18F-FDG, 18F-florbetaben, 18F-florzolotau); zero-shot held-out tracers (18F-florbetapir, 18F-FP-CIT); multicentre validation N=420 (three sites, four vendors). FreeSurfer-derived regional parcellations.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Vision transformer autoencoder learns CT-anchored attenuation representations.
- Contrastive objectives align MRI features to the CT feature space.
- Attention-guided residual correction harmonises PET-MRI uptake toward PET-CT standards.
- Evaluation: Wilcoxon signed-rank tests with Bonferroni correction, Bland-Altman limits of agreement, inter-regional correlation-matrix similarity (RV coefficient, SSIM, Mantel tests), Youden-index thresholds; compared with other harmonisation methods (e.g., ComBat-type with PET-CT as reference batch). No LLM.

## Results (key numbers and metrics)
- Cross-platform bias reduced by more than 80% while preserving inter-regional biological topology.
- Zero-shot generalisation to two held-out tracers without retraining.
- Multicentre: amyloid Centiloid discrepancy reduced from 23.6 to 4.1 (slightly above PET-CT test-retest variability); tau SUVR thresholds aligned.

## Limitations
Residual discrepancy still slightly above test-retest variability; individual-level data not public; medical-specific physics (attenuation correction).

## Transferable ideas for the FYP pipeline
- **Data ingestion / tabular:** if data come from different machines, sensors or camera setups, consider explicit harmonisation (e.g., contrastive alignment of features to a reference machine) before pooling data.
- **Evaluation:** borrow agreement statistics (Bland-Altman limits of agreement, paired Wilcoxon tests) when comparing predicted vs measured cut-quality metrics, and test zero-shot transfer to unseen materials as an analogue of held-out tracers.
