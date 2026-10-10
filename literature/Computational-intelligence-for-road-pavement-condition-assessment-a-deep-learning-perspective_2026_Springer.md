# Computational intelligence for road pavement condition assessment: a deep learning perspective

- **Citation (IEEE):** Y. Hu, R. Rayhana, L. Bai, et al., "Computational intelligence for road pavement condition assessment: a deep learning perspective," *Urban Lifeline*, vol. 4, art. 18, 2026, doi: 10.1007/s44285-026-00073-8.
- **Domain:** Civil infrastructure / computer vision survey (pavement defect detection: cracks, potholes, rutting).
- **Relevance to FYP (1-5):** 2 — review of visual surface-defect detection (CNN, Transformer, CLIP/VLM, SAM+LoRA) with a useful perception-vs-engineering-utility evaluation idea, but road domain, no LLM fault reasoning over machine data.

## Problem
Manual pavement inspection is slow, subjective and unsafe. Existing reviews focus on 2D images, miss recent Transformer/VLM progress, and rarely connect detector outputs (boxes, masks) to engineering indicators such as PCI and IRI that drive maintenance decisions.

## Data & modalities
Survey of 2D RGB imagery, RGB-T, stereo, 3D LiDAR/point clouds, 1D longitudinal profiles, and subsurface Ground Penetrating Radar (GPR); summarises public crack datasets (e.g., CRACK500, CFD, DeepCrack) and metrics (IoU, F1).

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Review structured as an Observation -> Primitives -> Indicators (O -> P -> I) pipeline. Covers CNN segmentation, Transformers for long thin cracks, 2D/3D multimodal fusion networks, label-efficient (semi/weak/unsupervised) learning, and VLMs: CrackCLIP (frozen CLIP + linear adapters + GradCAM pseudo-masks + crack prompts), LSeg/OVSeg open-vocabulary segmentation, OWL-ViT / Grounding DINO + SAM detect-then-segment, CoOp prompt learning and Tip-Adapter few-shot, URAVLM (generative VLM + multistep prompting + RAG), DamageQwen (VLM + detector), and CrackSAM (SAM fine-tuned with adapters and LoRA). Proposes a "Two-Tier Evaluation": Tier-1 perception metrics vs Tier-2 engineering indicators.

## Results (key numbers and metrics)
Survey; compiles benchmark tables of crack segmentation models (e.g., CT-crackseg, LECSFormer, AFFormer with scores in roughly the 50-77 range on reported metrics). Reports that an LLM-VLM stack reached expert-level PSCI-aligned assessment zero-shot (cited work). No new experiments.

## Limitations
Vision-only methods are sensitive to lighting and cannot measure depth; VLM outputs are not tightly coupled to engineering indicators and add prompt-design complexity; Tier-2 datasets with calibrated physical measurements are scarce; domain shift across regions remains an open issue.

## Transferable ideas for the FYP pipeline
- **Vision:** Use Grounding DINO/OWL-ViT + SAM as a detect-and-segment front end for cut-part defects (burr, dross, striations) before VLM description; consider CrackSAM-style LoRA/adapter fine-tuning of SAM on a small labelled set of TruLaser cut-edge images.
- **Vision (few-shot):** CLIP with CoOp prompts / Tip-Adapter cache for classifying new defect types with very few samples.
- **Evaluation:** Adopt a two-tier evaluation: Tier-1 = defect detection/classification accuracy; Tier-2 = engineering utility (correct root-cause, correct parameter adjustment such as gas pressure, focus position, feed rate). Report both.
- **Fusion:** Cross-check visual evidence against machine-database parameters, analogous to surface + subsurface cross-validation.
- **Text/RAG:** URAVLM's multistep prompting + RAG pattern for hazard reporting maps to retrieving TRUMPF manual sections for defect explanations.
