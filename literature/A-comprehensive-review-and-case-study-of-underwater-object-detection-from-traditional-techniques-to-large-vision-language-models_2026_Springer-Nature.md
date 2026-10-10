# A comprehensive review and case study of underwater object detection from traditional techniques to large vision language models

- **Citation (IEEE):** W. Song, E. Nabahirwa, M. Zhang, et al., "A comprehensive review and case study of underwater object detection from traditional techniques to large vision language models," *Discover Artificial Intelligence*, vol. 6, art. 247, 2026, doi: 10.1007/s44163-026-00895-z.
- **Domain:** Computer vision / underwater object detection (review + case study)
- **Relevance to FYP (1-5):** 3 - different domain, but its head-to-head YOLO11 vs LoRA-tuned Florence-2 comparison and synthetic-data findings directly inform the FYP vision stage (CNN detector vs VLM for defect localisation).

## Problem
Underwater object detection (UOD) suffers from image degradation (colour cast, haze, low contrast, blur), small/occluded targets, scarce and imbalanced labelled data, computational constraints and methodological limits. The review asks how far traditional methods go and whether large vision-language models (LVLMs) can help.

## Data & modalities
RGB underwater images (e.g., DUO dataset); case study test sets: real-world (RW), synthetic (DALL-E 3 generated), mixed, and Roboflow 100 (RF100) underwater subset.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Taxonomy of challenges in five groups linked to solutions (image enhancement/restoration, attention, multi-scale, domain adaptation, augmentation).
- Survey of LVLM evolution (captioning, VQA, open-vocabulary grounding) and how they may be adapted to UOD.
- Case study 1: synthetic underwater image generation with DALL-E 3 plus physics-inspired "aesthetic enhancement" (tint, turbidity noise, vignette scattering, particles, depth of field) and LAB colour transfer.
- Case study 2: Florence-2 fine-tuned with LoRA (backbone largely frozen, domain vocabulary constraints) vs YOLO11, each trained on real-only vs real+synthetic.

## Results (key numbers and metrics)
- YOLO11 had the highest mAP@50 on all test sets; real-only vs real+synthetic made little difference (about 0.905 vs 0.904 on RW).
- Florence-2 was lower in absolute terms but gained more from synthetic data: mAP@50 0.221 to 0.482 on synthetic set, 0.356 to 0.444 on mixed set, with a small drop on RW (0.458 to 0.429).
- Florence-2 produced semantic hallucinations (misspelled/near-synonym class labels) that had to be mapped to valid classes.
- YOLO11 remains preferred for real-time deployment.

## Limitations
LVLM real-time use is under-explored; synthetic images need better realism (physics-aware synthesis); LVLM label hallucination; case study limited in scale.

## Transferable ideas for the FYP pipeline
- **Vision:** use a dedicated detector (YOLO-family) for fast defect localisation on cut parts, and a VLM (Florence-2 / Qwen-VL) for semantic description and reasoning; a hybrid design rather than VLM-only.
- **Data ingestion / augmentation:** generate synthetic defect images (diffusion/DALL-E style) plus physics-inspired corruptions (lighting, reflections on metal, spatter) to rebalance rare defect classes; expect larger gains for VLMs than for CNN detectors.
- **LLM reasoning:** constrain VLM outputs to a closed defect vocabulary (or post-map to nearest valid class) to control label hallucination.
- **Evaluation:** test on real-only, synthetic and mixed sets separately; report latency/FPS alongside mAP for deployment decisions.
