# Co-Debater: A multimodal dialectical reasoning framework for suppressing reasoning hallucinations in hateful meme detection

- **Citation (IEEE):** C. Cheng, H. Zhong, and Y. Song, "Co-Debater: A multimodal dialectical reasoning framework for suppressing reasoning hallucinations in hateful meme detection," *Neurocomputing*, vol. 706, Art. no. 135027, 2026, doi: 10.1016/j.neucom.2026.135027.
- **Domain:** Multimodal content moderation (image + text), LMM hallucination
- **Relevance to FYP (1-5):** 3 — unrelated domain, but the pro/contra argument generation with a visually grounded judge is a concrete way to reduce sycophantic, ungrounded fault diagnoses from a VLM.

## Problem
Hateful memes combine individually harmless image and text. Generative LMM detectors suffer "reasoning hallucinations" and sycophancy bias: they align with stances implied by the prompt rather than visual facts.

## Data & modalities
Image + overlaid text memes. Benchmarks: Harm-C and Harm-P (from HarMeme, COVID-19 and political), MAMI (misogyny).

## Method
- **Phase I (dialectical reasoning):** backbone LLaVA-1.5-13B with two LoRA adapters trained by bidirectional adversarial fine-tuning using global counterfactual label flipping: one adapter argues the ground-truth stance, the other the opposite stance. A visually-anchored Chain-of-Thought (VCoT) forces arguments to cite visual facts.
- Base model acts as an impartial adjudicator scoring arguments on rationality, multimodal alignment strength and a third criterion, producing preference labels/confidence.
- **Phase II (judge):** lightweight judge on T5-small encoder with bidirectional co-attention after every block, fusing both arguments with frozen visual patch features to output the verdict.
- Five seeds; paired t-tests vs baselines (e.g., Pro-Cap, Evolver, RAG-HM, MemeWeaver).

## Results
- Macro-F1 of 92.11% on Harm-P; state-of-the-art on all three benchmarks, statistically significant (p < 0.05) over strongest baselines.
- Low variance across seeds (e.g., ±0.12% accuracy on Harm-C).
- Qualitative analysis: explanations more faithful to visual content, fewer hallucinated objects.

## Limitations
Requires training two 13B LoRA adapters plus a judge (compute cost); binary classification task; adjudicator prompts rely on the base model's own judgement; domain-specific to memes.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** for a defect image + machine record, generate competing hypotheses (e.g., "dross caused by low gas pressure" vs "caused by worn nozzle / wrong focus") and let a judge decide based on which argument is better grounded in the image and table evidence — reduces confirmation bias from operator prompts like "is it the nozzle?".
- **Prompting:** require visually anchored CoT: each claim must reference an observed visual feature (striation pattern, burr location).
- **Fusion:** a small judge model with co-attention between generated text arguments and image features is a lightweight final classifier.
- **Evaluation:** test for sycophancy by giving misleading prompts and checking whether diagnoses change.
