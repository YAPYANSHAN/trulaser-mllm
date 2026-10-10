# Evaluating commercial multimodal AI for diabetic eye screening and implications for an alternative regulatory pathway

- **Citation (IEEE):** M. S. Hunt, T. Dai, M. D. Abràmoff, "Evaluating commercial multimodal AI for diabetic eye screening and implications for an alternative regulatory pathway," *npj Digit. Med.*, vol. 9, art. 42, 2026, doi: 10.1038/s41746-025-02216-7.
- **Domain:** Medical imaging (ophthalmology) — benchmarking off-the-shelf MLLMs plus regulatory policy
- **Relevance to FYP (1-5):** 2 — medical domain, but it offers a rigorous, reproducible protocol for evaluating off-the-shelf MLLMs on image classification: frozen versions, temperature 0, JSON outputs, token-probability ROC and reportability. This is directly usable for the FYP's evaluation stage.

## Problem
Off-the-shelf generative AI models (OTSAIs) are being tried clinically without validation. Can they match purpose-built autonomous AI or experts for referable (more-than-mild) diabetic retinopathy (mtmDR) screening, and what regulatory path could exist?

## Data & modalities
Messidor-2: 1,748 macula-centred fundus images from 874 examinations, with a level-3 reference standard. Inputs are images plus a structured text prompt. Subject-level evaluation (either eye positive).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Models: gpt-4o-2024-08-06, gpt-4o-mini, grok-2-vision-1212 and gemini-1.5-pro via API, temperature 0, with versions frozen and "containerised"/bundled.
- Three prompts:
  - **Minimal:** a Boolean mtmDR grade in JSON.
  - **Background:** adds ETDRS severity definitions.
  - **Few-shot:** 5 image–answer pairs.
- **Reportability** = % of properly formatted JSON outputs.
- **ROC** from summed token probabilities of "true". The operating point is set where the lower 95% CI bound of sensitivity is ≥80% (2,000 stratified bootstraps).
- False-negative overlap between models measured with IoU.
- Human graders' sensitivity/specificity points are used to estimate expert AUC.

## Results (key numbers and metrics)
- AUC:
  - GPT-4o: 0.83 (minimal), 0.83 (background), 0.80 (few-shot).
  - GPT-4o-mini: 0.63–0.66.
  - Grok-2-vision: 0.63–0.66.
  - Gemini: AUC not calculable.
- Retina specialists: estimated AUC 0.94.
- Best operating point: GPT-4o with background prompt, sensitivity 0.88 / specificity 0.63.
- Reportability: 100% for OpenAI and xAI models. Gemini returned 85% (minimal), 89% (background) and 100% (few-shot).
- GPT-4o false negatives were mostly mild NPDR with dot-blot haemorrhages. Overlap of false-negative sets across models was limited.
- Few-shot examples did not improve GPT-4o.
- Performance is far from FDA endpoints. The authors propose task-specific licensing (like physician assistants) as a possible future pathway.

## Limitations
One public dataset. API models change over time. No "ungradable" option. Probability extraction is not available for all models. General models are not trained for the task. The regulatory proposal is speculative.

## Transferable ideas for the FYP pipeline
- **Evaluation:** pin model versions, use temperature 0, enforce JSON outputs and track the format-compliance rate (reportability) as a metric.
- **LLM reasoning/calibration:** where log-probs are available, derive a continuous fault score from token probabilities. This enables ROC/AUC and selecting an operating threshold (e.g., guaranteed defect recall) rather than relying on verbalised confidence.
- **Prompting ablation:** compare minimal vs. domain-background (e.g., ISO 9013 cut-quality definitions, TRUMPF defect catalogue) vs. few-shot prompts. Few-shot does not always help.
- **Error analysis:** examine false negatives by defect severity. Subtle defects (fine burr, slight striation) will likely be missed, as mild lesions were here.
- **Baselines:** compare against human-expert inter-rater points.
