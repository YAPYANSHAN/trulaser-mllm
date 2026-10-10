# Fidelity-driven data augmentation for multimodal large language model on architectural heritage interpretation

- **Citation (IEEE):** R. Huang, H.-C. Lin, W. Zeng, "Fidelity-driven data augmentation for multimodal large language model on architectural heritage interpretation," *npj Heritage Science*, vol. 14, art. 179, 2026, doi: 10.1038/s40494-026-02446-2.
- **Domain:** Architectural heritage / MLLM domain adaptation (facade visual question answering).
- **Relevance to FYP (1-5):** 4 — different domain, but a complete recipe for adapting an open MLLM (Qwen2.5-VL-7B + LoRA) to a data-scarce visual domain via controlled synthetic images and templated VQA, with expert audit of reasoning — directly reusable for cut-part defect images.

## Problem
General MLLMs (GPT-4o etc.) fail on fine-grained spatial (element position, symmetry) and semantic (material, style) interpretation of heritage facades, because high-fidelity domain training data is scarce.

## Data & modalities
Images + text QA. 258 street images (377 facades) of Guangzhou arcade buildings, rectified and polygon-annotated in LabelMe (parapets, walls, windows, columns, floors, shops); 50 images held out for test, 208 used as augmentation seeds. 60 multiple-choice question templates over a six-task taxonomy (visual perception, spatial reasoning, contextual reasoning). Supplementary CMP Facade dataset for European typology. Output: 1,672 synthetic images and 59,884 VQA samples; test set 70 real images, 3,550 expert-validated QA pairs.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Synthesis on a Flux Redux diffusion model with (1) Structure-aware Augmentation via ControlNet conditioned on layout edges/segmentation and (2) Semantic-aware Augmentation via typology-specific LoRA adapters (one per style class, applied to DoubleStream blocks). VQA labels inherited from structural annotations. Downstream: supervised fine-tuning of Qwen2.5-VL-7B with LoRA (r=8 on q/k/v of the LLM only; vision encoder and projector frozen), AdamW, 3 epochs, LR 1e-4 cosine, ~3 h on 4x H800. Evaluation prompt asks for answer first, then rationale.

## Results (key numbers and metrics)
Preliminary benchmark: GPT-4o 57.8% average accuracy, Gemini-2.5-Pro 52.7%, Claude-3.5-Sonnet 52.4%, Qwen-VL-MAX 51.5%, Qwen-7B 38.7%. Expert ratings of synthetic images: top-tier plausibility 74.7% vs 34.0% baseline; failure rate 1.3% vs 34.0%; interpretive accuracy 84.7% vs 72.0%. Fine-tuned 7B model on augmented joint data had the highest overall accuracy, surpassing GPT-4o, Gemini and Claude (e.g., per-task 59.6% vs 54.4% real-only on overall composition). Blind expert reasoning score (0-2): baseline 0.84, real-data FT 1.27, augmented FT 1.63. Six-category error taxonomy (rule-based failure, knowledge gap, omission, conceptual confusion, object hallucination, localization/calculation error).

## Limitations
Synthesis can lose environmental context; legible text/signage rendering is poor; model detects defects (e.g., cracks) but lacks expert severity judgement; multiple-choice format chosen because open-ended GPT-scoring was unreliable.

## Transferable ideas for the FYP pipeline
- **Vision (data ingestion):** Use ControlNet + per-class LoRA diffusion to synthesise extra cut-edge/defect images (dross, burrs, striation roughness) conditioned on real part contours, expanding scarce TruLaser defect data.
- **LLM reasoning:** LoRA-fine-tune Qwen2.5-VL-7B (LLM side only, frozen vision tower) on templated defect VQA; a small tuned model can beat frontier APIs in a narrow domain.
- **Evaluation:** Build a task taxonomy (defect identification, location, severity, cause, corrective parameter) and score per task; adopt their six-way error taxonomy and blinded expert 0/1/2 rubric for reasoning traces.
- **Prompting:** "Answer first, then rationale" structured prompts for auditable diagnoses.
- **Evaluation gap:** Explicitly annotate severity and intervention thresholds — their noted failure mirrors the need to link defects to actionable parameter changes.
