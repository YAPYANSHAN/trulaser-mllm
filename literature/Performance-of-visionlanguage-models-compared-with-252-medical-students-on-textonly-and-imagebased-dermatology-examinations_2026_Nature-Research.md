# Performance of vision-language models compared with 252 medical students on text-only and image-based dermatology examinations

- **Citation (IEEE):** O. Erdem, A. Yilmaz, A. S. Şahin, et al., "Performance of vision-language models compared with 252 medical students on text-only and image-based dermatology examinations," *Scientific Reports*, vol. 16, art. 30214, 2026, doi: 10.1038/s41598-026-68943-3.
- **Domain:** Medical education / dermatology — VLM benchmarking against humans
- **Relevance to FYP (1-5):** 2 — unrelated domain; useful mainly as evidence that VLM text knowledge does not imply visual-reasoning competence and for its repeated-run variability evaluation protocol.

## Problem
VLMs score highly on text-based medical exams, but their performance on visually intensive assessments, and whether visual recognition translates into causal/treatment reasoning, is poorly understood.

## Data & modalities
Ten consecutive dermatology clerkship examinations (Sept 2023–Jan 2025) at a Turkish medical school, original non-English materials: text-only questions (multiple-choice, multiple-select, matching; 60% of score) and image-based structured open-ended questions (40%) across seven sub-domains. Human comparator: 252 fifth-year medical students.

## Method
- VLMs: GPT-4o and GPT-5 (via ChatGPT), Gemini 2.5 Flash, Gemini 3 Pro; zero-shot, no fine-tuning or RAG.
- Expert-validated answer keys and rubrics; five repeated runs per exam session to measure output variability; first-run sensitivity analysis; Kruskal–Wallis/Wilcoxon tests; difficulty correlation and sub-domain analyses (visual description, diagnosis, etiology, differential, treatment).

## Results
- Text-only: all VLMs > 95 mean vs students 84.91 ± 9.04 (p < 0.001); Gemini 3 Pro highest (98.45 ± 1.42); little sensitivity to exam difficulty.
- Image-based: Gemini 3 Pro 93.94 ± 3.41, GPT-5 87.24 ± 6.97 vs students 82.94 ± 9.69 (both significantly higher); GPT-4o 77.36 ± 5.40 and Gemini 2.5 Flash 70.34 ± 5.08 significantly lower than students.
- Students had the smallest text-vs-image gap. Weaker models were accurate in visual description/diagnosis but dropped in etiological reasoning. Gemini 3 Pro had the lowest run-to-run variance; Gemini 2.5 Flash the highest.

## Limitations
Single centre and curriculum; structured academic exams, not clinical practice; repeated model runs vs single-attempt students not directly comparable; static images only; open-ended answers not scored by blinded independent raters (no inter-rater reliability); no student sub-domain data.

## Transferable ideas for the FYP pipeline
- **Evaluation:** benchmark the MLLM separately on text-only fault questions (manual knowledge) and image-based defect questions — expect a gap; report both rather than a pooled score.
- **LLM reasoning:** score not just defect labelling but "root cause" and "corrective action" sub-tasks with a rubric, since correct visual labels may not yield correct causal reasoning.
- **Reliability:** run each query multiple times and report variance; prefer models with low run-to-run variability for operator-facing deployment.
- **Model selection:** model choice matters greatly for image tasks; compare frontier vs lighter models before fixing the VLM.
- **Human baseline:** compare against operators/technicians to contextualise performance.
