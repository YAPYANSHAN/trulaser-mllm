# Mitigating multimodal hallucinations through visual attention tracing and origin-point regeneration

- **Citation (IEEE):** B. Li, H. Yu, Y. Han, et al., "Mitigating multimodal hallucinations through visual attention tracing and origin-point regeneration," *Scientific Reports*, vol. 16, Art. no. 25596, 2026, doi: 10.1038/s41598-026-52390-1.
- **Domain:** Multimodal LLM reliability: training-free decoding to reduce visual hallucinations.
- **Relevance to FYP (1-5):** 3 - general natural images, not industrial, but hallucinated defect descriptions are a key risk for the FYP and this is a plug-in, training-free guard for open VLMs.

## Problem
MLLMs describe objects, attributes or relations that are not in the image. Existing fixes either retrain (RLHF, DPO; expensive) or apply global decoding penalties/contrastive decoding (OPERA, VCD, DoLa, DeCo) that do not locate *where* the hallucination began, so the triggering token stays in the sequence and corrupts what follows.

## Data & modalities
Image + text generation. MSCOCO-based benchmarks: POPE (500 images; random/popular/adversarial object-existence probing), CHAIR (500 images, "Please describe this image in detail"), AMBER (existence, attributes, relations). A human-annotated set of 200 MSCOCO captions from LLaVA-1.5 with token-level hallucination onsets.

## Method
Hallucination Backtracking (HB), training-free, white-box decoding:
- **Visual Attention Score (VAS):** at each generated token, take final-layer attention mass on visual tokens, max over heads (max beats mean by 2.2 POPE-F1 points).
- **Origin detection:** monitor the VAS decline (delta VAS) over a window k = 10; when it falls below threshold tau = 0.15, locate the token of maximum drop as the origin.
- **Backtracking and regeneration:** truncate at the origin, reinitialise beam search (beam 5) and regenerate with an attention bias toward visual tokens and VAS-guided sampling; at most 3 backtracks.
- Tested on LLaVA-1.5-7B, InstructBLIP-7B, MiniGPT-4-7B and Shikra-7B (all Vicuna-7B); A100 80 GB.

## Results
- LLaVA-1.5: POPE F1 91.4%, CHAIR_S 40.2 (+1.5 F1 and -4.4 CHAIR_S vs OPERA).
- Across all four models HB beats DeCo by 0.8-1.3 POPE-F1 and 1.1-1.6 AMBER points.
- Origin localisation: 41.8% exact match (OPERA 28.2%, probability-based 21.5%); 84.1% flagged at or before the first hallucinated token.
- VAS is about 0.52 in faithful text vs 0.18 in hallucinated spans; the drop precedes the hallucination by 1-3 tokens.
- Ablation: confidence-based detection instead of VAS gives -2.7 F1 and +4.6 CHAIR_S; a penalty in place of backtracking gives -2.2 F1.
- Cost: 2.0x greedy decoding, about 1.11x over beam search; 0.4 backtracks per sequence on average.

## Limitations
False negatives 15.9% (hallucinations from scene priors with stable VAS); false positives 12.3%; 3.2% unresolved after 3 backtracks; about 8.4% of errors are high-VAS misrecognitions. Needs access to attention weights (open models only). Weak for short VQA answers. English, natural photos only; not tested on industrial images.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** If the FYP uses an open VLM (LLaVA/Qwen-VL), log VAS while it writes a defect description of a cut part; a sharp drop flags claims (e.g., "burr on the bevel edge") that are not grounded in the image.
- **Deployment:** This is a training-free plug-in with about 11% overhead over beam search, acceptable for offline diagnosis reports.
- **Fusion / evaluation:** Combine VAS with the other grounding checks the FYP can do (segmentation mask agreement, database parameter consistency), since VAS misses prior-driven errors.
- **Evaluation:** Adapt POPE-style yes/no probing ("Is there dross on the lower edge?") and CHAIR-style counting of mentioned-but-absent defects to build a laser-cut hallucination benchmark.
- **Vision:** Keep long-form descriptions short and structured; hallucinations cluster in later "elaboration" phases (20-35% and 55-80% of the sequence).
