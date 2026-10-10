# SAM-LLaVA: A segmentation-aware vision-language framework for industrial defect diagnosis

- **Citation (IEEE):** S. An, C. Wang, and X. Dong, "SAM-LLaVA: A segmentation-aware vision-language framework for industrial defect diagnosis," *Pattern Recognition*, vol. 180, Art. no. 114242, 2026, doi: 10.1016/j.patcog.2026.114242.
- **Domain:** Industrial visual defect detection and description with Large Vision-Language Models (LVLMs).
- **Relevance to FYP (1-5):** 5 - directly addresses industrial defect localisation plus LLM-generated, hallucination-reduced defect descriptions, the core of the FYP's vision/diagnosis stage.

## Problem
LVLM defect methods (AnomalyGPT, Myriad, SPGDD-GPT) rely on CLIP patch-level similarity, so micro-defects are poorly localised, and they simply concatenate image features with text tokens, so the language model never "sees" a segmentation mask. Result: imprecise localisation and hallucinated descriptions; "one-class-one-model" methods (PatchCore, SPADE) do not adapt to new defect types.

## Data & modalities
Images + text descriptions. MVTec-AD (15 classes, 1725 abnormal / 3629 normal), VisA (12 classes, 1200 abnormal / 8821 normal) for cross-dataset zero-shot; TADD (Text-Augmented Defect Data Set, ~19,500 abnormal / 16,000 normal, 30+ classes, 21 subsets, 70/15/15 split) for few-shot.

## Method
"Segment-align-describe" pipeline: (1) CLIP ViT-B/16 (LAION-400M) produces a coarse anomaly heatmap from normal/abnormal text prompts, binarised with Otsu threshold; in few-shot mode, a multi-scale memory bank of normal support features (CLIP layers 3/8/12) modulates the heatmap (contextual similarity adaptation). (2) The coarse mask is used as a mask prompt to SAM (ViT-H), with a multi-scale prompt learner (pooling k = 8/4/2) and multi-scale mask decoder trained with Dice + focal loss. (3) Segmentation-Aware Semantic Alignment (SASA): bidirectional cross-attention between mask-weighted visual features and text embeddings, then input to LLaVA with Vicuna-7B-v1.5. LoRA (r = 16, alpha = 32) on Q/V and FFN layers; CLIP/SAM image encoders frozen. Joint loss = segmentation + generation cross-entropy. Adam, lr 1e-4, 50 epochs, 2x NVIDIA L40.

## Results
- Zero-shot VisA->MVTec-AD: Image-AUC 94.8%, Pixel-AUC 95.6% (SPGDD-GPT 93.6/94.8); MVTec-AD->VisA: 86.9 / 95.7.
- TADD average Pixel-AUC 93.3 / 94.0 / 95.0% for 1/2/4-shot, beating SPGDD-GPT by 2.0/1.4/1.3 points.
- Description accuracy (1-shot): 92.3% MVTec-AD, 83.8% VisA (+2.2/+3.2 vs SPGDD-GPT).
- GPT-4V-as-judge description score (0-100): 96.0 vs 94.0 SPGDD-GPT, 83.5 AnomalyGPT, 35.0 PandaGPT.
- Removing SASA cut description accuracy by 2.7 (MVTec) and 3.6 (VisA) points; mask prompts beat point prompts.
- Cost: 8.33B params, 112M trainable (LoRA 31.6M); 1564 ms/image, 21 GB peak GPU memory; ~35 h training.

## Limitations
Slow (0.64 img/s) and memory-heavy, so not real-time; more normal shots made the LLM more conservative (accuracy dropped 92.3 -> 90.8% from 1 to 4 shots on MVTec-AD); evaluation is on generic benchmarks (no metal/laser-cut parts); the description judge is GPT-4V, not human experts; baseline numbers are copied from prior work.

## Transferable ideas for the FYP pipeline
- **Vision:** Use a CLIP-heatmap -> SAM mask cascade to localise burr, dross, striation or bevel-angle defects on cut parts without dense labels; Otsu threshold avoids manual tuning.
- **Vision (few-shot):** Build a small memory bank of "good part" images per material/thickness to calibrate anomaly maps.
- **Fusion:** Feed mask-grounded region features (not the raw image only) into the VLM so it describes defect location/shape faithfully; this is a template for grounding.
- **LLM reasoning / fine-tuning:** LoRA r = 16 on a 7B VLM is a feasible budget for a small domain-specific defect-description dataset.
- **Evaluation:** Adopt Image/Pixel-AUC for localisation plus a VLM-as-judge rubric (correctness, completeness, fine-grained detail, interpretability), checked against an engineer's ratings.
- **Deployment:** Budget about 1.5 s/image on a 48 GB-class GPU; acceptable for offline post-cut inspection, not in-process monitoring.
