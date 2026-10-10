# Diagnostic accuracy of multimodal large language models in differentiating epileptic from functional seizures in smartphone recorded videos

- **Citation (IEEE):** A. Patel, S. K. Vallamchetla, A. Safa, et al., "Diagnostic accuracy of multimodal large language models in differentiating epileptic from functional seizures in smartphone recorded videos," *Sci. Rep.*, vol. 16, art. 11719, 2026, doi: 10.1038/s41598-026-46333-z.
- **Domain:** Medical (neurology) — zero-shot video diagnosis with multimodal LLMs
- **Relevance to FYP (1-5):** 2 — medical domain, but a useful benchmark of zero-shot MLLM diagnosis from visual input, with findings on input quality, calibration and over-confidence.

## Problem
Differentiating epileptic from functional seizures normally needs expert review of video or video-EEG, which causes delays. The study asks whether general-purpose multimodal LLMs can classify seizures from bystander smartphone videos without clinical context or domain training.

## Data & modalities
Prospective study: 24 smartphone videos from 15 patients (19 epileptic, 5 functional), with EMU video-EEG diagnosis as the gold standard. Videos were uncropped, in portrait or landscape, and annotated for quality, lighting, focal region and semiology (motor vs. non-motor). Input is video only.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Four Gemini models (1.5 Pro, 2.0 Flash, 2.5 Flash, 2.5 Pro) accessed through Vertex AI.
- One standardised single-turn prompt per video in a fresh session. The prompt asks for a diagnosis plus a self-reported 1–10 confidence score.
- Default sampling: temperature 1.0, top-p 0.95. No fine-tuning, RAG or clinical context.
- Metrics: accuracy, sensitivity, specificity, PPV, NPV and F1 with Clopper–Pearson confidence intervals. Pairwise model comparisons, subgroup analyses and a patient-level sensitivity analysis.

## Results (key numbers and metrics)
- Accuracy: Gemini 1.5 Pro 33.3%, 2.0 Flash 25.0%, 2.5 Flash 54.2%, 2.5 Pro 54.2%. 2.5 Pro beat 1.5 Pro (p = 0.01) and 2.0 Flash (p = 0.003).
- Gemini 2.5 Pro had the best balance: sensitivity 52.6%, specificity 60.0%, F1 64.5%. The older models had 100% specificity but sensitivity of only 5.3–42.1%.
- A majority-class baseline would reach 79.2% accuracy, but with 0% specificity.
- Videos framed on the upper body or face gave 80–90% accuracy for the 2.5 models vs. 28.6–35.7% for whole-body views. Poor or low-light videos gave ~0%.
- Median confidence was 8–9 regardless of correctness. For 2.5 Pro, mean confidence was 8.45 when wrong vs. 8.46 when right, i.e. "confidently wrong".

## Limitations
Very small and imbalanced sample (only 5 functional events) with wide confidence intervals. Single centre. Proprietary black-box models. Self-reported confidence is not a calibrated probability. Explanations may be hallucinated justifications.

## Transferable ideas for the FYP pipeline
- **Evaluation:** never report accuracy alone on imbalanced defect classes. Use per-class sensitivity/specificity and F1, compare against a majority-class baseline, and add confidence intervals for small test sets.
- **LLM reasoning / calibration:** do not trust verbalised confidence. Use evidence-based scoring instead: agreement with retrieved manual entries and table anomalies, self-consistency, or a calibrated classifier score.
- **Vision/data ingestion:** image framing and quality strongly affect MLLM accuracy. Standardise how cut-part and defect photos are captured (close-up of the cut edge, lighting, scale reference) and add quality gating before inference.
- **Baseline study design:** benchmark several VLM versions under a fixed prompt as the zero-shot baseline before domain adaptation (fine-tuning or RAG).
