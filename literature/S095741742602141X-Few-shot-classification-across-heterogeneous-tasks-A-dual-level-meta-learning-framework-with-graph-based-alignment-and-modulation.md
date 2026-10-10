# Few-shot classification across heterogeneous tasks: A dual-level meta-learning framework with graph-based alignment and modulation

- **Citation (IEEE):** M. Wang, X. Li, Z. Leng, et al., "Few-shot classification across heterogeneous tasks: A dual-level meta-learning framework with graph-based alignment and modulation," *Expert Systems With Applications*, vol. 331, Art. no. 133232, 2026, doi: 10.1016/j.eswa.2026.133232.
- **Domain:** Computer vision; few-shot learning / optimization-based meta-learning; applied to rock photomicrographs.
- **Relevance to FYP (1-5):** 2 - No LLM or industrial data, but few-shot image classification across heterogeneous tasks is relevant when only a handful of labelled cut-defect images exist per material/thickness.

## Problem
Optimization-based meta-learning (MAML, ANIL, GAP) overfits task-specific features when tasks come from heterogeneous (multimodal) distributions - e.g., some tasks hinge on colour, others on texture or shape - causing intra-task and inter-task feature distribution discrepancies and poor cross-task generalization.

## Data & modalities
Images only. CIFAR-FS, miniImageNet (64/16/20 classes, 600 images/class), CUB (200 birds, fine-grained), DTD (47 texture classes); real-world Nanjing University rock photomicrograph dataset (108 classes, 2,634 polarized-light micrographs from 324 thin sections), resized to 84x84. 5-way 1-shot and 5-shot episodes; cross-domain miniImageNet to CUB/DTD/Rock.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
MGAM (Meta-learning with Graph-based Alignment and Modulation), plug-and-play over optimization-based meta-learners. (1) Graph-based Task Alignment (GTA): task embeddings, a task-similarity graph, and collective-perception soft labels from multiple related tasks used as regularization (replacing single-teacher distillation, e.g., MLFDA). (2) Meta Semantic Modulator (MSM): partitions features into semantic clusters and modulates their activation strengths in the outer loop to ease inner-loop adaptation. Backbones: 4-layer ConvNet (main) and ResNet12; Adam, inner lr 0.01, outer lr 0.001, 5 inner steps train / 10 test. No language models.

## Results (key numbers and metrics)
- CIFAR-FS: ANIL +5.92% (1-shot) / +4.32% (5-shot); MAML +4.48% / +5.88%. miniImageNet: ANIL +3.14% / +4.80%; MAML +3.39% / +4.18%; GAP and ProtoNet also improve.
- Cross-domain to CUB/DTD gains up to 8.20% (1-shot); vs. MLFDA +2.80-3.99% on DTD.
- Rock dataset: 1-shot ANIL +4.96%, MAML +5.91%; 5-shot +2.25% / +4.10%; MAML+MGAM 5-shot target-domain 93.66%.
- Over random seeds, ANIL 1-shot 57.28% to 63.49%. GTA adds negligible time/memory.

## Limitations
Low-resolution (84x84) images; small backbones; ANIL+MGAM slightly below MLTI in some Rock settings; parameter overhead depends on backbone; code only on request; no multimodal or text information.

## Transferable ideas for the FYP pipeline
- **Vision:** Few-shot episodic training for defect recognition when each material/thickness/gas combination is a separate "task" with different discriminative cues (edge texture vs. dross shape vs. colour/oxidation).
- **Vision/fusion:** Task-similarity graphs - relate cutting jobs by parameter similarity (from the machine database) to share knowledge between sparse job types.
- **Evaluation:** Report N-way K-shot accuracy with 95% CI and cross-domain transfer (e.g., mild steel to stainless) retention ratios.
- Lower priority versus VLM-based zero/few-shot approaches; useful mainly as a non-LLM baseline.
