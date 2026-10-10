# Evaluation of cross-ethnic emotion recognition capabilities in multimodal large language models using the reading the mind in the eyes test

- **Citation (IEEE):** E. Refoua, Z. Elyoseph, D. Piterman, et al., "Evaluation of cross-ethnic emotion recognition capabilities in multimodal large language models using the reading the mind in the eyes test," *Sci. Rep.*, vol. 16, art. 9975, 2026, doi: 10.1038/s41598-026-39292-y.
- **Domain:** Psychology / affective computing — benchmarking MLLM emotion recognition and bias
- **Relevance to FYP (1-5):** 1 — unrelated domain, and the only method is zero-shot multiple-choice testing of commercial chatbots. The one minor takeaway is evaluation practice: test–retest consistency, a chance baseline and contamination checks.

## Problem
Can MLLMs recognise complex mental states from eye-region images, and are they consistent across ethnic groups, i.e. do they show the human "other-race effect"? Previous tests used ethnically homogeneous stimuli.

## Data & modalities
Three Reading the Mind in the Eyes Test (RMET) versions: original White, Black (B-RMET) and Korean (K-RMET). 36 eye-region photographs each, with 4-option forced choice. Image plus text options. Human normative data for comparison.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- ChatGPT-4, ChatGPT-4o and Claude 3 Opus, accessed manually via public chat interfaces. Each test was administered twice to check test–retest consistency.
- Accuracy compared to the 25% chance level (binomial tests, Cohen's h, risk difference) and to percentiles of human norms.
- No fine-tuning, retrieval or special prompting. The hypotheses were not preregistered.

## Results (key numbers and metrics)
- ChatGPT-4o: 83.3% (30/36, White), 94.4% (34/36, Black) and 86.1% (31/36, Korean). This corresponds to the 85th, 94th and 90th human percentiles. Well above chance (p < .001; Cohen's h 1.253–1.619).
- ChatGPT-4: near the human average (9.6th, 43rd and 17th percentiles).
- Claude 3 Opus: near chance (percentiles 0.012, 4.00 and 0.045).
- Performance was consistent across ethnic versions, with high test–retest agreement.

## Limitations
RMET validity is contested (poor factor structure; it may measure vocabulary or elimination strategies). Stimuli may have leaked into training data. Static, constrained images only. Small number of items. Consumer interfaces. Results do not generalise to real-world social cognition.

## Transferable ideas for the FYP pipeline
- **Evaluation:** run each query at least twice to measure test–retest stability of MLLM diagnoses. Report performance against a chance or majority baseline with effect sizes, not just raw accuracy.
- **Evaluation (bias/consistency):** test whether diagnostic accuracy is consistent across subgroups. In the FYP these could be material types (mild steel, stainless, aluminium), thicknesses or lighting conditions, analogous to the cross-ethnic consistency check.
- **Contamination awareness:** public benchmark images may be in training data. Use in-house TruLaser defect photos for the held-out evaluation.
- **Model selection:** the large spread between model versions (near chance vs. above human) argues for benchmarking several MLLMs before committing to one in the pipeline.
