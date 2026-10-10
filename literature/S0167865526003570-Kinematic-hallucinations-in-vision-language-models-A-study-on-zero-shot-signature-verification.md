# Kinematic hallucinations in vision-language models: A study on zero-shot signature verification

- **Citation (IEEE):** M. Robledo-Moreno, R. Vera-Rodriguez, R. Tolosana, et al., "Kinematic hallucinations in vision-language models: A study on zero-shot signature verification," *Pattern Recognition Letters*, vol. 210, pp. 89-95, 2026, doi: 10.1016/j.patrec.2026.09.042.
- **Domain:** Biometrics / forensic handwriting; zero-shot VLM evaluation and hallucination auditing.
- **Relevance to FYP (1-5):** 3 - Different domain, but highly transferable lessons: encoding time-series into images for a VLM, extracting calibrated scores from logprobs, two-stage JSON verdicts with CoT, and auditing whether VLM explanations cite evidence that is not actually in the input.

## Problem
Can commercial VLMs act as zero-shot forensic examiners for online signature verification, and does their natural-language reasoning stay faithful to the visual evidence? Static images lack dynamics (speed, pressure), so VLMs may "rationalize" with fabricated kinematic attributes.

## Data & modalities
Online signatures (pen/finger time series incl. pressure) rendered as static images. SVC benchmark: Task 1 stylus 6,000 comparisons, Task 2 mobile finger 9,520, Task 3 combined 12,000; plus e-BioSign DS2 for generalization. 45,520 evaluations total.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Preprocessing encodes normalised pressure as grayscale stroke intensity (RGB colormaps and thickness modulation were tried and found harmful). GPT-5.2 and Gemini 2.5 Pro via API, temperature 0, prompted as "Forensic Document Examiner", output strict JSON: initial verdict, reasoning, final verdict, certainty 0-100. Scores: S_v1/S_v2 from token log-probabilities of the initial/final verdict (GPT only), S_text from self-reported certainty. Kinematic Hallucination Index (KHI) = share of kinematic vs. static keyword types in rationales; adjective density via spaCy POS tags. No fine-tuning or RAG. Open-source VLMs (LLaVA-1.5, Open-Vision-Reasoner) were insufficient in preliminary tests.

## Results (key numbers and metrics)
- Random forgeries: GPT-5.2 EER 0.21% (Task 1 binary), 0.49% pressure-encoded; Gemini 3.41% on Task 2 (beats SIG winner 3.62%); e-BioSign GPT 0.68%.
- Skilled forgeries: far worse than supervised SOTA (DLVC-Lab 4.66%); GPT pressure encoding worsened EER 43.07% to 48.08% (Task 1) and 30.72% to 32.20% (Task 3); best GPT Task 2 18.64% vs. baseline 20.58%; TA-RNN 3.70% vs. ~24% best zero-shot on e-BioSign.
- Adjective density: GPT-5.2 ~27.39% vs. Gemini ~19.65%.
- CoT rarely flips verdicts, but whenever probability rose >50% after CoT the verdict was correct.

## Limitations
Only two closed models; Gemini exposes no logprobs; KHI keyword lists manually curated; static rendering loses dynamics; models unreliable for fine-grained (skilled) discrimination.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series to vision:** Rendering machine signals as plots/images for a VLM is risky - extra encodings can confuse it; prefer feeding numeric tables as text or summarised features.
- **LLM reasoning:** Two-stage JSON output (initial verdict, reasoning, final verdict, confidence) for each fault diagnosis; track verdict shift as a calibration signal.
- **Evaluation:** Use logprob-derived scores for ROC/EER-style thresholds; build a domain "hallucination index" - e.g., flag explanations citing parameters (gas pressure, focus position) not present in the supplied evidence.
- **Vision:** Expect VLMs to do well on coarse defect separation but poorly on subtle look-alike defects; keep a supervised specialist model for fine distinctions.
