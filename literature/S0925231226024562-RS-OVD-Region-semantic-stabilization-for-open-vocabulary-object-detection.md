# RS-OVD: Region-semantic stabilization for open-vocabulary object detection

- **Citation (IEEE):** D. Ju, Y. Fan, L. Shen, et al., "RS-OVD: Region-semantic stabilization for open-vocabulary object detection," *Neurocomputing*, vol. 706, Art. no. 135058, 2026, doi: 10.1016/j.neucom.2026.135058.
- **Domain:** Computer vision — open-vocabulary object detection, continual learning
- **Relevance to FYP (1-5):** 2 — general detection on COCO/LVIS; relevant mainly as a way to detect defect categories named in text (including new ones) without retraining a closed-set detector.

## Problem
Open-vocabulary detectors (OVD) recognise arbitrary category names but suffer from unstable region-level semantic alignment, high-confidence false positives on semantically similar backgrounds, and forgetting when new categories are added incrementally.

## Data & modalities
Images + category-name text. Benchmarks: COCO (seen/novel split) and LVIS (large-vocabulary, long-tailed; rare/common/frequent categories). Incremental-category settings with limited annotations.

## Method
- DETR-style student detector learning a unified region embedding space aligned with category semantics.
- Positive supervision from three role-specific teachers (training only): CLIP category text prototypes, CLIP embeddings of cropped objects, and RegionCLIP region-level targets for local structure.
- Margin-based hard negative suppression: identifies background proposals with low IoU but high semantic similarity to category prototypes and pushes them away.
- Continual learning: memory replay and parameter stabilization to retain old categories while adding new ones.
- Teachers are not used at inference, keeping deployment simple.

## Results
- COCO: 60.4 Seen AP, 42.3 Novel AP, 58.6 AP50, 47.6 AP75.
- LVIS: 35.8 AP and 26.2 APr (rare), with gains across common and frequent categories.
- Improvements in false-positive control and continual incremental stability reported.

## Limitations
Heavy DETR-style student; memory selection is not adaptive; prototypes static; parameter-efficient incremental learning and lightweight students left to future work; evaluated only on natural-image benchmarks.

## Transferable ideas for the FYP pipeline
- **Vision:** an open-vocabulary detector (OWL-ViT/Grounding-DINO-type, or RS-OVD-style) lets the FYP localise defects on cut parts using text queries ("burr", "dross", "burn mark", "micro-joint") with few or no box labels, then send crops to the VLM/LLM.
- **False positives:** the hard-negative idea matters for sheet-metal images where reflections, scratches or edge texture resemble defects; mine look-alike background regions as negatives.
- **Continual learning:** memory replay allows adding new defect types later (e.g., bevel-specific defects on the TruLaser 3000 Bevel Cut) without forgetting earlier ones.
- **Deployment:** teacher-only-at-training distillation keeps the inference model small.
