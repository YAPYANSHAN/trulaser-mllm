# FCM-Hash: Label-enhanced cross-modal hashing via adaptive Mamba fusion and Kolmogorov-Arnold networks

- **Citation (IEEE):** Z. You and Z. Li, "FCM-Hash: Label-enhanced cross-modal hashing via adaptive Mamba fusion and Kolmogorov-Arnold networks," *Neurocomputing*, vol. 706, Art. no. 135012, 2026, doi: 10.1016/j.neucom.2026.135012.
- **Domain:** Cross-modal (image-text) retrieval / hashing, parameter-efficient VLM adaptation
- **Relevance to FYP (1-5):** 2 — general image-text retrieval; ideas on label-to-prompt conversion and LoRA on CLIP could support retrieving similar past defect images, but no fault-diagnosis content.

## Problem
Cross-modal hashing usually needs scarce, sentence-level text descriptions and lacks deep image-text interaction; full fine-tuning of large VLMs on sparse labels overfits and is expensive; MLP hash encoders lose information at very low bit lengths.

## Data & modalities
Images + discrete tags/labels (no sentence captions). Benchmarks: MS-COCO, MIRFlickr-25K, NUS-WIDE. Hash lengths 16, 32, 64 bits.

## Method
- Frozen CLIP ViT-B/16 backbone with LoRA (r = 8, α = 16) on Query/Value projections; only ~0.32% of parameters optimized.
- Label-Enhanced Prompt Learning: converts discrete labels into natural-language prompts to activate CLIP's semantic priors.
- FusionTransMamba: linear-complexity selective state-space (Mamba) fusion of visual patches and text tokens with an Adaptive Gate, replacing quadratic cross-attention.
- Kolmogorov-Arnold Network (KAN, 8 B-spline nodes) as hash encoder; Center Aggregation Learning and Adaptive Bit-Aware Loss Weighting.
- Compared with 11 recent baselines (e.g., PromptHash, DEH, DIM-CMH, VTPH, CMCL).

## Results
- Outperforms all 11 baselines across 16/32/64 bits on the three datasets (mAP and PR curves).
- MS-COCO image-to-text 64-bit mAP: FCM-Hash 0.9503 (label-only) vs PromptHash 0.9263 (dense text, full fine-tuning) and PromptHash* 0.7680 (label-only reproduction).
- Mamba fusion ablation improvement of +0.5%; fast convergence (mAP 0.9872 within first 50 epochs in a reported setting).
- Heatmaps suggest Mamba fusion suppresses background noise better than cross-attention.

## Limitations
Evaluated on general web-image datasets only; video-text and online/lifelong learning left to future work; hashing retrieval rather than reasoning or generation.

## Transferable ideas for the FYP pipeline
- **Vision / RAG:** build a retrieval index of past laser-cut defect images with labels (defect type, material, thickness) so a new defect image retrieves similar historical cases plus their root causes as context for the LLM ("case-based RAG").
- **Data ingestion:** convert sparse labels in the machine database ("material=S355, thickness=10mm, defect=dross") into natural-language prompts to exploit CLIP-style text encoders without writing captions.
- **Fine-tuning:** LoRA on CLIP Q/V projections is a cheap adaptation route when only labels, not descriptions, exist.
- **Deployment:** compact binary hash codes allow fast similarity search on modest hardware.
