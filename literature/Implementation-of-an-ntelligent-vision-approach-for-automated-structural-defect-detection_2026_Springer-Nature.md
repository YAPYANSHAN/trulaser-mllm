# Implementation of an intelligent vision approach for automated structural defect detection

- **Citation (IEEE):** H. Matich and H. Mousannif, "Implementation of an intelligent vision approach for automated structural defect detection," *Discover Artificial Intelligence*, vol. 6, art. 225, 2026, doi: 10.1007/s44163-026-00961-6.
- **Domain:** Structural health monitoring / visual defect detection + vision-language captioning
- **Relevance to FYP (1-5):** 4 - an end-to-end defect pipeline (detect -> segment -> generate engineering-language description -> web report) that maps closely onto the FYP's vision branch for cut-part defect images.

## Problem
YOLO/CNN defect detectors output only boxes/masks without contextual, actionable explanations; generic VLMs produce non-technical captions and are expensive. Goal: real-time detection, segmentation and domain-specific natural-language descriptions of structural defects (cracks, spalling, corrosion, etc.).

## Data & modalities
Curated dataset of 300,000 annotated structural defect images (images + boxes + masks + captions). Field validation with professional inspectors.

## Method
Multi-stage pipeline: (1) YOLOv10 for real-time detection; (2) DeepLabV3+ for pixel-wise segmentation; (3) domain-fine-tuned CLIP visual encoder whose local features are refined with Graph Attention Networks (GAT) modelling spatial relationships among defect regions, plus multi-scale semantic guidance; fused feature projected (linear) to 768-d and decoded by GPT-2 Small (124M) with constrained beam search and template guidance toward engineering sentence structures. Deployed as "BuildCaption" web/mobile app (plus offline desktop version) producing defect reports. Baselines included newer YOLO variants, transformer detectors, foundation segmentation, BLIP-2, and Grounded-SAM + GPT-4V.

## Results
96.5% mAP detection, 95.1% IoU segmentation, 0.86 BLEU-4 captioning, 0.3 s per image on off-the-shelf GPU. BLIP-2 reached BLEU-4 0.79; Grounded-SAM + GPT-4V 0.83 but at much higher computational cost; the proposed captioner uses ~62x fewer parameters than BLIP-2. Inspectors rated captions 4.3/5 accuracy and 4.5/5 usefulness; field inspection time reduced by 58%. Ablations confirm the value of GAT local features and multi-scale guidance.

## Limitations
Degrades in poor lighting, rain, fog, shadows; captions' quantitative statements can be off by about ±15% and need inspector verification; dataset lacks some rare defect types and materials; outputs are decision support, not replacement for engineers.

## Transferable ideas for the FYP pipeline
- **Vision:** cascade a fast detector (YOLO) for defect localisation on cut parts (burr, dross, incomplete cut, gouging, bevel-face striations) and a segmenter for measuring defect area/length, then pass measured geometry to the LLM.
- **Fusion:** graph-based relational features (GAT over defect regions) to describe spatial relations, e.g., dross concentrated at corners or along bevel edges.
- **LLM reasoning:** template-guided/constrained decoding to force engineering vocabulary and a fixed report schema; consider a small domain captioner vs a large VLM for cost/latency.
- **Deployment:** web app where an operator uploads a cut-part photo and receives a structured report - a direct analogue for the FYP demo; show confidence scores and require human validation.
- **Evaluation:** combine mAP/IoU/BLEU with expert Likert ratings of accuracy and usefulness, and a time-saved field study.
