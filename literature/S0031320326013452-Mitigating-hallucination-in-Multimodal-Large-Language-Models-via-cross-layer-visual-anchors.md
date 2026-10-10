# Mitigating hallucination in Multimodal Large Language Models via cross-layer visual anchors

- **Citation (IEEE):** C. Yang, S. Cai, J. Yuan, et al., "Mitigating hallucination in Multimodal Large Language Models via cross-layer visual anchors," *Pattern Recognition*, vol. 180, Art. no. 114380, 2026, doi: 10.1016/j.patcog.2026.114380.
- **Domain:** General-purpose MLLMs; hallucination mitigation; interpretability of attention.
- **Relevance to FYP (1-5):** 3 - Not industrial, but a training-free, low-overhead way to reduce visual hallucination in open MLLMs (LLaVA/Qwen-VL) is directly relevant to trustworthy defect-image descriptions in the FYP.

## Problem
MLLMs fabricate objects/details inconsistent with the image. Contrastive decoding doubles inference cost; attention amplification can amplify hallucinations; layer-injection methods lack interpretability. The paper asks why factual grounding degrades in deeper layers.

## Data & modalities
Image + text prompts. Benchmarks: POPE (MSCOCO, A-OKVQA, GQA; random/popular/adversarial; 500 images x 6 questions each; accuracy/F1), CHAIR (500 MSCOCO 2014 val images, 128-token captions; CHAIRs/CHAIRi, recall), MME full set.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Analysis of LLaVA-1.5-7B (32 layers x 32 heads) attention heatmaps shows visually sensitive heads focus sharply on query-relevant regions in mid layers, while deep-layer attention drifts back toward the diffuse patterns of early-layer visually insensitive heads. CLVA (Cross-Layer Visual Anchors) is a training-free, single-pass, plug-and-play inference intervention: classify heads as visually sensitive/insensitive by image-token attention; extract a positive anchor (mid-layer concentrated regions) and a negative anchor (early-layer noisy regions); in the drift layers reweight text-to-image attention A' = A(1 + alpha*Zpos - beta*Zneg) and renormalise. Applied to LLaVA-1.5, Qwen-VL and InstructBLIP (Q-Former). No fine-tuning, no RAG.

## Results (key numbers and metrics)
- POPE: accuracy gains 0.59-7.13% and F1 gains 0.28-6.33% over baselines; competitive with state-of-the-art training-free methods (IMCCD better on some results).
- CHAIR: LLaVA CHAIRs -5%, CHAIRi -2.5%; InstructBLIP CHAIRs -6.8%, CHAIRi -2.7%; recall also improves.
- Improves under stochastic sampling (top-p 1.0, T 1.0) and on MME perception for LLaVA-1.5.
- Minimal latency/memory overhead on a single NVIDIA H20; up to ~2x faster than IMCCD.

## Limitations
Post-hoc stabiliser only: depends on the vision encoder; cannot recover details never encoded; ineffective when attention is diffuse or anchors unreliable; evaluated on natural-image object hallucination only, not domain-specific fine detail; requires white-box access to attention (not usable with API-only models).

## Transferable ideas for the FYP pipeline
- **LLM reasoning / vision:** If the FYP uses an open-weight VLM (LLaVA, Qwen-VL) locally, CLVA-style attention re-anchoring is a zero-training option to reduce invented defects (e.g., describing dross that is absent).
- **Evaluation:** Adapt POPE-style yes/no probing ("Is there burr on the bottom edge?") and CHAIR-style hallucination rates over a labelled set of cut-part images to quantify VLM grounding.
- **Explainability:** Attention heatmaps from mid layers can be shown to the operator as visual evidence supporting a diagnosis.
- **Deployment:** Prefer single-pass interventions over contrastive decoding for latency on shop-floor hardware.
