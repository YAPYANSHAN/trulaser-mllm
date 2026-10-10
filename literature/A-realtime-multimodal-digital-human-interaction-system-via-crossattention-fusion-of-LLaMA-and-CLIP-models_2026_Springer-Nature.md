# A real-time multimodal digital human interaction system via cross-attention fusion of LLaMA and CLIP models

- **Citation (IEEE):** Y. Qiu and P. Feng, "A real-time multimodal digital human interaction system via cross-attention fusion of LLaMA and CLIP models," *Discover Artificial Intelligence*, vol. 6, art. 1075, 2026, doi: 10.1007/s44163-026-02107-0.
- **Domain:** Human-computer interaction / multimodal LLM (digital humans)
- **Relevance to FYP (1-5):** 3 - different application, but the token-level cross-attention fusion of CLIP visual features into LLaMA, with ablations and edge-latency benchmarks, is a concrete fusion and deployment reference.

## Problem
Digital-human systems have shallow multimodal understanding (single LLM or loose image-text retrieval), weak dynamic personalisation and poor end-to-end real-time performance.

## Data & modalities
Video/image + text: MSVD and MSR-VTT (official splits) and 1,000 annotated interaction samples (8:1:1 split); user interaction history for profiling; speech and facial-animation output layers.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Layered architecture: multimodal perception, core processing, personalised interaction, rendering output.
- CLIP vision encoder + LLaMA language model fused via a token-level cross-attention module aligning CLIP visual features with LLaMA hidden states.
- Interest-decay LSTM updates a user profile after each interaction for personalised recommendation.
- Training: AdamW, LR 2e-5, batch size 32. Baselines: LLaMA-only, CLIP-only, text-driven system.

## Results (key numbers and metrics)
- Image-text matching 90.3% (LLaMA-only 76.5%, CLIP-only 81.2%); intention recognition 87.6% (74.2% / 70.5%); personalised recommendation 82.5%.
- User satisfaction 4.6/5, dialogue naturalness 4.5/5.
- Inference latency (batch 1): 180 ms A100, 260 ms RTX 4060, 420 ms Jetson AGX; end-to-end response 2.4 s vs 1.8 s for a text-only system.
- Scenario metrics up to 86.7% emotional-interaction success, 94.5% lip-sync accuracy, 90.1% gesture success.

## Limitations
Small custom interaction set (1,000 samples); data available only on request; multimodal pipeline adds latency over text-only; deeper user-state modelling left for future work.

## Transferable ideas for the FYP pipeline
- **Fusion:** cross-attention from LLM tokens to CLIP image patch features is a simple, trainable alternative to prompt-only fusion for combining cut-part images with textual machine context; run the same unimodal ablations (text-only, image-only, fused) to quantify each modality's contribution.
- **Tabular/time-series:** the decay-weighted LSTM state concept could maintain a running "machine health profile" (e.g., nozzle/lens condition) updated after each job, fed to the LLM as context.
- **Deployment / evaluation:** benchmark latency on server GPU vs consumer GPU vs Jetson-class edge device and separate model latency from end-to-end latency; add a user (operator) satisfaction rating for report usefulness.
