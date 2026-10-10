# Compact Vision Language Models Enable Efficient and Interpretable Optical Coherence Tomography through Layer-Specific Multimodal Learning

- **Citation (IEEE):** T. Haghighi, S. Gholami, J. T. Sokol, et al., "Compact vision language models enable efficient and interpretable optical coherence tomography through layer-specific multimodal learning," *Communications Medicine*, vol. 6, art. 32, 2026, doi: 10.1038/s43856-025-01293-9.
- **Domain:** Medical imaging (ophthalmology, OCT) / compact VLM for report generation + classification
- **Relevance to FYP (1-5):** 3 - medical domain, but shows that a small (247M) domain-trained VLM with structure-specific (region-wise) text supervision beats much larger general/medical VLMs at both narrative generation and classification - a viable alternative to a large VLM for cut-part images.

## Problem
Turning OCT B-scans into accurate clinical narratives requires fusing visual features with anatomical expertise. Existing medical VLMs (RetinaVLM, LLaVA-Med) are large, generalise poorly and give weak layer-level descriptions; CNNs give only labels or segmentations.

## Data & modalities
40,000 OCT B-scans from public repositories and private clinical cohorts, each paired with expert-validated summaries; six classes (DME, DR, geographic atrophy, drusen, CNV, healthy). Text descriptions per retinal layer (NFL, GCL, IPL, OPL, IS/OS). Modalities: grayscale images + structured text.

## Method
LO-VLM (247M parameters) built on a BLIP encoder-decoder (ViT image encoder + transformer text encoder/decoder). Training prompts of the form "<LayerName>: summary" inject anatomical priors. Three objectives: retina layer-text matching (RLTM), retina-layer contrastive alignment (RLCA) and layer-conditioned language modelling (LCLM). Trained 50 epochs, batch 32 on a 49 GB GPU; max output 256 tokens. Baselines: RetinaVLM (Llama 3 backbone + ResNet encoder), LLaVA-Med, ViT-Base vision-only, and PaLI-Gemma 2 (3B) fine-tuned in ablation. Saliency heatmaps for explanation. Text metrics: SBERT similarity (MedEmbed-large), BERTScore, BLEU-4, ROUGE-L, CIDEr.

## Results
Blinded rating by three retina specialists: LO-VLM 8.5 (SD 1.15)/10 vs RetinaVLM 5.5 (SD 1.13), p<0.0001. SBERT similarity 80.3% and BERTScore F1 71.5%, improvements of 8.2% and 28.8% over specialised VLM baselines. Classification accuracy 96% (F1 96%), 13% above ViT and more than 62% above medical VLM benchmarks (p<0.05).

## Limitations
Data from a limited number of institutions/devices; only six disease classes and five layers; no OCT angiography or longitudinal analysis; small evaluator panel; research-only, not for clinical deployment.

## Transferable ideas for the FYP pipeline
- **Vision / LLM reasoning:** train or fine-tune a compact BLIP-style VLM on cut-part images paired with region-specific descriptions ("Top edge: ...", "Bottom edge / dross: ...", "Bevel face: ...", "Kerf: ..."), mirroring layer-specific prompts; produces structured, grounded defect narratives cheaply.
- **Fusion:** joint objectives (matching + contrastive + conditioned captioning) give one model for retrieval, classification and description.
- **Evaluation:** combine semantic text metrics (SBERT with a domain embedding model, BERTScore) with blinded expert scoring out of 10, and compare compact model vs large general VLM.
- **Deployment:** a sub-1B model is easy to run on-premise beside the TruLaser.
