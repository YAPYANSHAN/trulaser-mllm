# A vision-language model-based approach for lung cancer diagnosis using lossless 3D CT images: evaluation of GPT-4.1 and GPT-4o for patient-level malignancy assessment

- **Citation (IEEE):** N. Shi, Z. Liu, Z. Wan, et al., "A vision-language model-based approach for lung cancer diagnosis using lossless 3D CT images: evaluation of GPT-4.1 and GPT-4o for patient-level malignancy assessment," *Health Information Science and Systems*, vol. 14, art. 16, 2026, doi: 10.1007/s13755-025-00417-8.
- **Domain:** Medical imaging / VLM-based diagnosis (prompting, no fine-tuning)
- **Relevance to FYP (1-5):** 4 - medical domain, but its guideline-grounded, mask-guided prompting of off-the-shelf VLMs (GPT-4.1/4o) with hierarchical item-to-case reasoning is a direct template for prompting a VLM with defect crops, overlays and TRUMPF guidance.

## Problem
Large VLMs have shown promise in medicine, but lossless 3D image analysis is under-explored; without clinical context they may fabricate findings. Goal: interpretable, guideline-consistent patient-level lung-cancer diagnosis from native 3D CT.

## Data & modalities
3D chest CT (DICOM converted to NIfTI, voxel fidelity preserved) + nodule annotations + text guidelines. LIDC-IDRI final cohort: 72 patients (31 benign, 41 primary lung cancer), 171 nodules. External validation: LNDb, 30 patients (15 benign / 15 malignant).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- VLMs: GPT-4.1 and GPT-4o, zero-shot via prompting.
- Multi-stage workflow emulating radiologists: extract nodule coordinates; present multi-slice visual inputs (bounding annotations, segmentation overlays, cropped views); nodule-level malignancy prediction with rationale; synthesis into a patient-level assessment.
- Consensus guidelines (Fleischner, BTS, ACCP) embedded in prompts.
- Three input settings: (1) coordinates only; (2) coordinates + guideline prompting; (3) segmentation overlays + guideline prompting.
- Compared with deep-learning baselines and radiologist readers.

## Results (key numbers and metrics)
- GPT-4.1 outperformed GPT-4o overall, especially with full-context input; GPT-4o had higher sensitivity with limited input.
- GPT-4.1 with segmentation + guidelines: accuracy 0.722, AUC 0.780 on LIDC-IDRI; external LNDb accuracy 0.767, AUC 0.780.
- Competitive with representative DL baselines and radiologists, with explicit textual justifications.

## Limitations
Small cohorts (72 and 30 patients); closed commercial models (reproducibility, privacy); modest absolute accuracy; generalisation to broader populations left for future work.

## Transferable ideas for the FYP pipeline
- **Vision / LLM reasoning:** feed the VLM structured visual inputs (full part photo + bounding box + segmentation overlay + zoomed crop of the defect) rather than raw images; ablate the three input levels as here.
- **Text/RAG:** embed TRUMPF cutting-quality guidelines/parameter tables in the prompt (analogous to Fleischner/BTS) so diagnoses are standard-aligned and justified.
- **Fusion / reasoning:** hierarchical reasoning: defect-level assessments first, then a part- or job-level verdict and recommended parameter changes.
- **Evaluation:** compare GPT-class VLMs against a trained CNN baseline and human technicians; keep an external validation set (different machine/material).
- **Data ingestion:** preserve full image resolution and metadata (lossless) when passing images to the model.
