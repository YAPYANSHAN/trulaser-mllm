# Sequential sensitivity analysis of multimodal large language models for rare orbital disease detection

- **Citation (IEEE):** C. Lei, K. Ji, C. Zhao, et al., "Sequential sensitivity analysis of multimodal large language models for rare orbital disease detection," *Communications Medicine*, vol. 6, Art. no. 175, 2026, doi: 10.1038/s43856-026-01447-3.
- **Domain:** Medical imaging / ophthalmology, MLLM diagnosis
- **Relevance to FYP (1-5):** 3 - medical domain, but it measures how each added modality and prompt changes MLLM diagnostic accuracy, and it builds a CLIP-specialist + GPT-4o agent. Both carry over to multimodal fault diagnosis.

## Problem
Rare orbital diseases (orbital inflammation, orbital tumours, thyroid eye disease (TED)) are often diagnosed late. It is unclear whether MLLMs can detect them, and how much each additional clinical input (image, chief complaint, race, reasoning prompt, specialist model output) contributes.

## Data & modalities
- **Dataset 1:** 6,786 single-eye external photographs from China, used to fine-tune CLIP for 3-way triage (healthy / orbital / non-orbital).
- **Dataset 2:** 170 participants from China, Singapore and Thailand, used to evaluate GPT-4o-Latest.
- Modalities: external eye photographs, chief-complaint text, race metadata, and the CLIP classifier output.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **CLIP** fine-tuned with symmetric InfoNCE loss (AdamW, two-stage learning rate). Compared with three traditional and three newer models, and with Gemini 2.0 and GPT-4o zero-shot.
- **Sequential sensitivity analysis** of GPT-4o-Latest. Each stage adds one input to the previous ones:
  - Stage A: image only
  - Stage B: + chief complaint
  - Stage C: + race
  - Stage D: + structured diagnostic-reasoning prompt
  - Stage E: + CLIP output, forming an "AI agent"
- Outputs: top-1/3/5 differential diagnoses, plus a generated medical report and examination recommendations rated for accuracy, readability, completeness and harm.
- Statistics: paired Wilcoxon tests; ICC for repeatability.

## Results (key numbers and metrics)
- CLIP triage accuracy 90.21%, better than all baselines.
- GPT-4o, Stage A (image only): top-1 13.72%, top-3 21.37%, top-5 25.68%.
- Stage E (agent): top-1 49.41%, top-3 75.88%, top-5 85.29%.
- TED top-1 rose from 26.51% (A) to 87.37% (E). Orbital inflammation peaked at Stage D, and the agent lowered its accuracy because of class imbalance.
- Harm score 2.84 ± 0.02 (low risk).
- Simulated hard triage: 2.82% missed diagnosis, 88.18% of orbital cases flagged.

## Limitations
- Retrospective study with a small, Asian-only sample. Possible selection and hindsight bias.
- Only one MLLM (GPT-4o) evaluated.
- Class imbalance (TED-dominant) skews results.
- Data are not public.

## Transferable ideas for the FYP pipeline
- **Evaluation:** run a staged ablation that adds one input at a time:
  - defect image only
  - + machine-table parameters
  - + error/alarm logs
  - + RAG manual excerpts
  - + structured reasoning prompt
  - + specialist vision-classifier output

  Report top-k cause accuracy at each stage. This quantifies what each modality adds.
- **Vision + LLM reasoning (agent):** a fine-tuned lightweight classifier (CLIP or CNN on defect types such as burr, dross or roughness) feeds its label and confidence into the general MLLM. This gave the largest gain here, because zero-shot VLMs are weak on specialised images.
- **LLM reasoning:** output a top-k differential diagnosis rather than a single answer, and generate recommendations (here: process-parameter changes). Score them for correctness, completeness and potential harm.
- **Deployment:** use a two-stage triage: a cheap classifier flags abnormal cuts, and only flagged cases go to the expensive MLLM.
- **Evaluation:** check repeatability across runs (ICC) and watch class imbalance in the fault categories.
