# Diagnostic performance of a multimodal large language model in assessing the index of complexity, outcome, and need: comparison with orthodontist evaluation

- **Citation (IEEE):** R. Bilici Geçer, A. Tabancalı, Ç. Hasgül, et al., "Diagnostic performance of a multimodal large language model in assessing the index of complexity, outcome, and need: comparison with orthodontist evaluation," *BMC Oral Health*, vol. 26, art. 1775, 2026, doi: 10.1186/s12903-026-09094-9.
- **Domain:** Medical (orthodontics) — MLLM image-based scoring against an expert reference
- **Relevance to FYP (1-5):** 2 — dental domain, but it shows how a general MLLM handles multi-component, rubric-based visual scoring. Analogous to scoring cut quality against a standard (e.g., ISO 9013 criteria) from photos.

## Problem
Manual ICON scoring of orthodontic treatment need is slow and varies between examiners. The study tests whether ChatGPT-5.5 (Thinking mode) can score the five ICON components and decide treatment need from images.

## Data & modalities
104 patients: 520 intraoral photographs and 520 2D rendered digital-model images (rendered from STL, with a 50 mm scale bar and labelled views). Reference standard: two orthodontists' scores, keeping only cases with complete agreement between them. Inputs are images plus a structured text prompt.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- ChatGPT-5.5 "Thinking" via the web UI, default settings, with memory and training-data sharing disabled so each case is independent.
- Structured ICON prompt optimised by **Iterative Prompt Calibration (IPC)**: wording refined over pilot cases. An exploratory chain-of-thought prompt was shown qualitatively only.
- No fine-tuning or RAG.
- Statistics: accuracy, sensitivity, specificity, F1, exact agreement, Cohen's kappa, ICC, ROC/AUC.

## Results (key numbers and metrics)
- Binary treatment-need accuracy: 74.0% (photographs) and 72.1% (model images).
- Recall for treatment-required cases was 0.871 / 1.00, but for no-treatment cases only 0.471 / 0.147. The model systematically overestimates need.
- ICC for the total ICON score: 0.463 for photos (moderate) and 0.154 for models (poor). AUC: 0.671 and 0.574.
- Component agreement varied. Crowding/spacing and vertical relationship differed significantly between photos and models, while the anteroposterior relationship was better on model images.

## Limitations
General model not trained on dental images. 2D renders rather than native 3D. Web-UI access limits reproducibility as the model changes. Excluding cases where experts disagreed under-represents borderline cases. Opaque closed model, and CoT explanations are sometimes inconsistent with final outputs. Errors accumulate across multi-stage categorical scoring.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** multi-component weighted scoring compounds errors. Have the MLLM extract per-criterion observations (e.g., burr, dross, striation, bevel angle, kerf) and compute the aggregate score deterministically in code.
- **Prompting:** iterative prompt calibration on a pilot set is a cheap, documentable method for building a structured diagnosis prompt. Freeze the prompt before the test evaluation.
- **Vision/data ingestion:** labelled views and a scale bar in images help the model judge geometry. Include a scale reference in cut-part photos.
- **Evaluation:** report per-class recall and use ICC/kappa against expert raters. Watch for a bias toward "defective/high-risk", which inflates false alarms.
- **Deployment:** use API access with pinned model versions for reproducibility rather than a consumer UI.
