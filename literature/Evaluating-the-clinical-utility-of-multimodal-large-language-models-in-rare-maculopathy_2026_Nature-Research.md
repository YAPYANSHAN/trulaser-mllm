# Evaluating the clinical utility of multimodal large language models in rare maculopathy

- **Citation (IEEE):** M. D. Tran, E. Walker, I. D. Nagel, et al., "Evaluating the clinical utility of multimodal large language models in rare maculopathy," *Sci. Rep.*, vol. 16, art. 54, 2026, doi: 10.1038/s41598-025-29299-2.
- **Domain:** Medical imaging (ophthalmology) — comparison of zero-shot MLLMs vs. specialists
- **Relevance to FYP (1-5):** 2 — medical domain. The transferable lessons are about prompt design: a constrained answer space, combining several image views, and adding structured metadata. These are relevant to rare-defect differentiation.

## Problem
Pentosan polysulfate (PPS) maculopathy is rare and is often misdiagnosed as Stargardt disease or PRPH2 pattern dystrophy. Can general MLLMs distinguish these lookalike conditions from multimodal retinal imaging?

## Data & modalities
Retrospective, two centres: 126 eyes from 63 patients (36 PPS, 50 Stargardt, 40 PRPH2 pattern dystrophy). Three imaging modalities: ultra-widefield colour (UWF-C), UWF autofluorescence (UWF-AF) and OCT. Plus demographic data (age, sex). Two retina specialists also graded the cases.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Models: ChatGPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro and Perplexity (Llama 3.1 Sonar), zero-shot via the chat interfaces. Prompts open with "Answer ... as an ophthalmologist".
- 4 prompts × 4 image configurations (A: UWF-C, B: UWF-AF, C: OCT, D: all combined):
  - P1: long multiple-choice list, no demographics.
  - P2: long list with demographics.
  - P3: restricted 3-disease list.
  - P4: restricted list with demographics.
- No fine-tuning or RAG. Metrics: accuracy, sensitivity and specificity with CIs; human inter-rater kappa.

## Results (key numbers and metrics)
- P1, all modalities: ChatGPT accuracy 0.351 (best), sensitivity 0.267. Claude specificity 1.0. Single modalities scored 0.125–0.387 (Gemini best on UWF-AF).
- P2 (adding demographics to the long list) lowered all-modality accuracy for all models except Perplexity. ChatGPT reached 0.298.
- P3 (restricted choices): ChatGPT all-modality accuracy 0.421, and 0.429 on UWF-C.
- P4: demographics plus restricted choices improved accuracy and sensitivity over P2. ChatGPT was best with all images combined.
- Specialists far outperformed the MLLMs on P1: accuracy 0.714 and 0.571 (kappa ~0.59).
- Conclusion: MLLMs currently perform poorly on this rare disease.

## Limitations
Small, rare-disease cohort. Retrospective. Consumer interfaces with evolving models. Imaging taken at a single time point (no longitudinal data). Possible training-data biases. Demographic information may bias both humans and models.

## Transferable ideas for the FYP pipeline
- **LLM reasoning/prompting:** restrict the candidate diagnosis set. First narrow candidates using machine-table evidence or retrieval (e.g., the TRUMPF defect catalogue entries relevant to the material/thickness), then ask the MLLM to discriminate among a short list. Open-ended lists cause large drops in accuracy.
- **Fusion:** give the model several image views together (top surface, cut edge, bottom dross side). The combined view generally performed best for the strongest model.
- **Metadata:** adding structured context (here demographics; in the FYP, material, thickness, gas, program parameters) helped in the constrained setting but hurt in the open-ended one. Test the effect of metadata explicitly.
- **Evaluation:** benchmark against human experts (machine operators or service engineers) with inter-rater kappa, using a factorial prompt × modality design.
