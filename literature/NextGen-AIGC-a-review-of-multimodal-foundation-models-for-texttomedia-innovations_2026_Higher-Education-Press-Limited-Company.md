# Next-Gen AIGC: a review of multimodal foundation models for text-to-media innovations

- **Citation (IEEE):** C. Jin, J. Fan, J. Huang, et al., "Next-Gen AIGC: a review of multimodal foundation models for text-to-media innovations," *Frontiers of Computer Science*, vol. 20, no. 12, art. 2012368, 2026, doi: 10.1007/s11704-025-51171-9.
- **Domain:** Generative AI review — multimodal foundation models (diffusion, MLLMs) for text-to-image/video/music/motion
- **Relevance to FYP (1-5):** 2 — a background survey on multimodal foundation models; the focus is generation, not diagnosis, but it is useful for the literature-review chapter (CLIP, Flamingo, BLIP-2, instruction tuning) and for synthetic defect-image augmentation.

## Problem
No comprehensive review existed of how multimodal foundation models (MFMs) are applied to text-prompt-based AI-generated content (AIGC). The paper surveys four tasks: text-to-image, text-to-video, text-to-music and text-to-motion.

## Data & modalities
Review article (no experiments). It catalogues training datasets per task (large image–text pair corpora at billion scale, video-clip datasets, music and motion-capture datasets), as well as model scales and architectures.

## Method
- Background on foundation models: BERT/GPT, CLIP contrastive pretraining, BEiT, instruction tuning, GPT-4V and Gemini, MLLMs such as Flamingo, BLIP-2, Kosmos-2, MiniGPT-5, SpeechGPT, and any-to-any systems (Visual-ChatGPT, AudioGPT).
- For each task the review covers fundamental concepts, model architectures (GANs/VAEs to diffusion models, e.g. DALL-E 2, Imagen, Stable Diffusion, Make-A-Video, Phenaki, Sora, AudioLM, Stable Audio, TEMOS), training strategies and dataset settings.
- It also discusses the shift from "traditional" to "Next-Gen" AIGC built on adapted MFMs.

## Results
Qualitative synthesis only, with no new quantitative results. The identified challenges are:
- long-context multimodal processing (temporal consistency)
- limited input modalities (sensor data, LiDAR and haptics are rarely supported)
- fine-grained controllability and instruction following
- safety for embodied agents and misuse (deepfakes), which calls for alignment, interpretability and watermarking

## Limitations
- Generation-centric, with little coverage of discriminative or diagnostic use of MLLMs.
- No industrial or manufacturing applications are discussed.
- No benchmark comparison is provided.
- As a broad survey, its depth on any single architecture is limited.

## Transferable ideas for the FYP pipeline
- **Literature review:** use it as a citation source for the evolution from CLIP to instruction-tuned MLLMs (GPT-4V, Gemini, BLIP-2, Flamingo) when justifying the choice of VLM.
- **Data augmentation (vision):** text-to-image diffusion models could generate synthetic cut-defect images (dross, burrs, striations) to balance rare fault classes. Validate them carefully against real samples.
- **Fusion:** the survey notes that most MFMs ingest only text and images. This supports the FYP's choice to serialise sensor and tabular machine data into text, or to add dedicated encoders.
- **Evaluation/safety:** cite the interpretability and alignment challenges when motivating evidence-grounded, explainable diagnosis outputs.
