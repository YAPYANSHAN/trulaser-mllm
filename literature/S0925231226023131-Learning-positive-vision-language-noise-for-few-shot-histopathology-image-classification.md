# Learning positive vision-language noise for few-shot histopathology image classification

- **Citation (IEEE):** Y. Meng, H. Guo, M. Li, et al., "Learning positive vision-language noise for few-shot histopathology image classification," *Neurocomputing*, vol. 705, Art. no. 134915, 2026, doi: 10.1016/j.neucom.2026.134915.
- **Domain:** Medical imaging (histopathology), few-shot VLM adaptation
- **Relevance to FYP (1-5):** 2 — unrelated domain, but a cheap few-shot adaptation of CLIP-type models is transferable to classifying laser-cut defect images when labelled examples are scarce.

## Problem
Adapting VLMs (CLIP, PLIP) to histopathology classification is hard due to few annotations, domain shift and costly full fine-tuning. Existing parameter-efficient methods (Linear Probe, adapters, CoOp prompt learning) leave room for improvement.

## Data & modalities
Images plus class-name text prompts. Four datasets: SICAP-MIL (prostate, Gleason-related categories), NCT-CRC (colorectal tissue types), LC-LUNG (lung/colon), SkinCancer (fine-grained skin lesions). Few-shot settings up to 16 shots.

## Method
- HiPN (Histopathology Positive Noise), based on positive-incentive noise theory.
- Image encoder, text encoder and logit scale are frozen; a lightweight noise generator (MLP; cross-attention variant evaluated) learns a conditional, sample-specific noise distribution injected into the vision-language classification process.
- Optimized only via the few-shot classification loss.
- Backbones: CLIP (ViT-B/16) and PLIP (ViT-B/32). Baselines: zero-shot, Linear Probe, CLIP-Adapter, CoOp.
- No LLM generation, RAG or LoRA.

## Results
- CLIP, 16-shot vs Linear Probe: LC-LUNG accuracy 83.42% → 91.56% (+8.14), SkinCancer 56.34% → 70.76% (+14.42).
- Macro-F1: LC-LUNG 83.17% → 91.61%; SkinCancer 49.98% → 63.68%.
- Consistent gains on both CLIP and PLIP across datasets and shot settings.
- Extra overhead ~0.5-2% of backbone compute; visualizations show noise concentrated on diagnostically meaningful regions.

## Limitations
Patch-level classification only (whole-slide analysis left for future work); limited public histopathology datasets; no textual prompt co-learning; no uncertainty estimation; classification rather than explanation/report generation.

## Transferable ideas for the FYP pipeline
- **Vision:** with few labelled TruLaser defect photos per class (e.g., dross, burr, burn-through, striation, bevel-angle error), freeze a CLIP/SigLIP encoder and train a tiny adapter or noise generator rather than full fine-tuning; compare against zero-shot CLIP with text prompts like "a laser-cut steel edge with heavy dross".
- **Evaluation:** report macro-F1 alongside accuracy because defect classes will be imbalanced; run 1/2/4/8/16-shot curves to show data efficiency.
- **Fusion:** the CLIP defect label and similarity scores can be passed as structured evidence to the LLM reasoning stage.
- **Explainability:** visualize where the adaptation focuses (cf. noise maps) to verify that the model looks at the cut edge, not the background.
