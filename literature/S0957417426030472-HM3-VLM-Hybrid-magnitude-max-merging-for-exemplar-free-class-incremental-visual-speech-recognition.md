# HM3-VLM: Hybrid magnitude-max merging for exemplar-free class-incremental visual speech recognition

- **Citation (IEEE):** C. Zheng, Z. Chen, L. Xu, et al., "HM3-VLM: Hybrid magnitude-max merging for exemplar-free class-incremental visual speech recognition," *Expert Systems With Applications*, vol. 331, Art. no. 134141, 2026, doi: n/a.
- **Domain:** Vision-language models / lip reading (visual speech recognition), continual learning
- **Relevance to FYP (1-5):** 2 - unrelated application. The visual-encoder + projector + small LLM with dual-side LoRA, and model merging for adding new classes without old data, are transferable to adding new defect types.

## Problem
Open-world visual speech recognition (VSR) must separate fine-grained homophenes (words that look the same on the lips). Privacy rules forbid replaying stored face videos, so class-incremental learning suffers catastrophic forgetting. Existing exemplar-free methods over-smooth features.

## Data & modalities
- Incremental versions of the lip-reading datasets LRW (i-LRW) and LRW-1000 (i-LRW1000).
- Additional German (i-GLips-Homophene) and Persian homophene sets.
- Modality: video of lip movements, with text labels.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Visual encoder:** pre-trained Auto-AVSR (3D+2D ResNet-18 front end plus a 12-layer Conformer).
- **Modality Projector:** a single linear layer.
- **Semantic decoder:** a frozen Qwen3-0.6B LLM.
- **Dual-side LoRA:** applied to both the encoder and the LLM.
- **Hybrid Magnitude-Max Merging (Sign-Max Merging):** per-task LoRA task vectors are merged under geometric constraints, keeping the top 20% of parameters by magnitude. Sequential Weight Inheritance and a Task-1 anchor keep optimisation in a low-energy manifold. No exemplar replay is used.

## Results (key numbers and metrics)
- **i-LRW:** Avg_T 91.32% and Acc_T 87.23%, beating the runner-up ACMap by 2.16 and 3.02 points.
- **i-LRW1000 (B0-Task20 cold start):** Avg_T is 58.33%, vs. 39.04% for a competing method. HM3-VLM leads ACMap by 5.98 points (Avg_T) and 8.12 points (Acc_T), and even beats replay-based iCaRL by 3.64 and 4.88 points.
- **German set (B0-Task5):** average accuracy 38.10% and final accuracy 26.20%.
- Latency is reported as minimal. Code is released.

## Limitations
- Difficulty with tonal languages, where pitch is not visible on the lips.
- Open-world multilingual deployment remains challenging.
- Evaluated on word-level classification, not open-ended generation.

## Transferable ideas for the FYP pipeline
- **Vision + LLM fusion:** a lightweight VLM recipe of a frozen domain vision encoder, a linear projector and a small LLM (e.g., Qwen3-0.6B) with LoRA on both sides. This is a cheap way to build a defect-image-to-text diagnostic head for TruLaser cut-part images.
- **Deployment/maintenance:** merge task-specific LoRA adapters (e.g., new material or new defect class added later) without retaining old proprietary images. This is useful when new fault types appear over the machine's life.
- **Evaluation:** test incremental "cold-start" scenarios where only a few defect classes are known at first.
