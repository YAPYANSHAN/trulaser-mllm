# A Visual Question Answering Dataset for Benchmarking Vision-Language Models in Plant Science (PlantExpertVQA)

- **Citation (IEEE):** S. N. Sakib, N. Haque, M. Z. Hossain, et al., "A Visual Question Answering Dataset for Benchmarking Vision-Language Models in Plant Science," *Scientific Data*, vol. 13, art. 1161, 2026, doi: 10.1038/s41597-026-07779-y.
- **Domain:** Agricultural plant-disease diagnosis / vision-language models (VQA)
- **Relevance to FYP (1-5):** 3 - different domain, but its knowledge-base-grounded VQA generation and PEFT of a small VLM is a close template for building a laser-cutting defect VQA set.

## Problem
Plant-disease datasets target classification/detection only, so VLMs cannot support interactive, reasoning-based diagnosis. Existing agri-VQA resources rely on LLM-generated text without rigorous expert verification.

## Data & modalities
Images + text QA. 150,841 images from 45 open datasets (incl. PlantVillage), 38 crops, 89 disease conditions; 765,186 QA pairs across 9 question categories and 3 cognitive levels (identification to causal/counterfactual). A structured Disease Knowledge Base of 203 JSON cards (pathogen taxonomy, transmission, risk factors, severity rubric, organ-specific symptoms, lookalike conditions with differentiating features, management).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Image curation: MD5 + perceptual-hash de-duplication, aspect-ratio-preserving padding, Laplacian-variance blur filter, histogram exposure filter, HSV background-bias check.
- Two-stage QA generation: template-based synthesis from image metadata and KB cards, then multi-stage linguistic re-engineering; two rounds of botanist review.
- Benchmark: zero-shot evaluation of 9 open VLMs (BLIP-2, LLaVA-1.5/1.6, Qwen2-VL, Qwen3-VL, Gemma-3, etc.).
- Parameter-efficient fine-tuning of Qwen3-VL-2B on 2,337 QA pairs (a fraction of 1% of training split).
- Metrics: EM, Token-F1, BLEU-1/2, ROUGE-L, BERTScore.

## Results (key numbers and metrics)
- Best zero-shot model (Gemma-3-4B-IT): ROUGE-L 15.26, BERTScore 11.20, EM 2.04.
- Fine-tuned Qwen3-VL-2B: EM 18.85, Token-F1 64.65, BLEU-1 66.18, ROUGE-L 61.70, BERTScore 63.27, surpassing all larger zero-shot models.
- High BLEU-1 can coexist with low/negative BERTScore, so lexical overlap does not imply semantic correctness. Authors argue failures reflect a knowledge gap rather than capability gap.

## Limitations
Proof-of-concept fine-tuning (one architecture, small subset); English only; geographic/crop bias inherited from sources; KB not exhaustive and static; automated metrics only, no human expert evaluation of outputs.

## Transferable ideas for the FYP pipeline
- **Data ingestion / text:** build a "defect knowledge card" schema per defect type (burr, dross, incomplete cut, bevel angle error): causes, process parameters implicated, visual symptoms, lookalikes and differentiators, corrective actions. Use it to template QA pairs grounded in TRUMPF documentation.
- **Data ingestion / vision:** reuse the image quality audit (pHash dedup, blur, exposure checks) for cut-part photos.
- **LLM reasoning:** LoRA-style PEFT of a 2B-class VLM on a few thousand domain QA pairs may beat large zero-shot models; good for a resource-limited FYP.
- **Evaluation:** structure questions by cognitive level (identify / explain cause / counterfactual "what if power increased") and report lexical + semantic metrics; add human expert scoring.
