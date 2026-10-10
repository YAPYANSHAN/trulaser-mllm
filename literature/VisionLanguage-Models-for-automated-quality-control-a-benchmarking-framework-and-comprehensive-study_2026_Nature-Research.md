# Vision-Language Models for automated quality control: a benchmarking framework and comprehensive study

- **Citation (IEEE):** M. Abdelkader, "Vision-language models for automated quality control: a benchmarking framework and comprehensive study," *Scientific Reports*, vol. 16, art. 24047, 2026, doi: 10.1038/s41598-026-55179-4.
- **Domain:** Computer-vision quality control; open-source VLMs as semantic meta-assessors of object-detection output across medical, aerial, industrial and general domains.
- **Relevance to FYP (1-5):** 4 - a direct reality check for using local open VLMs on industrial inspection images. The industrial domain scored only 25.4% mean accuracy zero-shot. The paper also gives a reusable evaluation harness (JSON prompts, cascading parser, stability metrics, deployment tiers).

## Problem
Deployed detectors (such as YOLO) degrade under distribution shift. Statistical drift monitoring lacks semantic understanding. Can VLMs verify whether a detection's class label is semantically correct, so that they could trigger autonomous fine-tuning?

## Data & modalities
- Images, optionally with highlighted detection regions, plus text prompts.
- Five domains with 200 stratified samples each (1,000 per model): COCO, VisDrone, Brain Tumor (MRI), Carparts (Roboflow, industrial components) and HAM10000 (dermatology).
- Ground truth is the original dataset's class labels, scored by exact match.

## Method
- **Models.** Nine open, locally deployed VLMs, mostly run through Ollama on RTX 4070 GPUs: DeepSeek-VL-1.3B, LLaVA-7B-v1.6, LLaVA-13B, LLaMA-3.2-Vision-11B, Mistral-Small3.2-24B, Qwen2.5-VL-7B, Gemma3-4B, Gemma3-12B and Granite3.2-Vision-2B. API models were excluded for privacy and cost reasons.
- **Prompting.** Zero-shot, with a three-part prompt: context, task with the class list, and a JSON schema `{classification, confidence, reasoning}`. There is no fine-tuning or RAG.
- **Parsing.** A six-strategy cascading response parser extracted 98.7% of answers successfully.
- **Statistics.** Bootstrap confidence intervals, Kruskal-Wallis tests, effect sizes, and coefficient of variation (CV) across domains. A composite QC Score = 0.6 × Accuracy + 0.4 × Stability.
- **Deployment tiers.** Production-assistant thresholds of ≥80% for medical, ≥70% for industrial and ≥60% for surveillance; then supervised; then research-stage.

## Results
- **Overall:** accuracy ranged from 8.5% to 82.8% (mean 45.7%, SD 18.5%). LLaVA-13B was best overall at 48.6%. Qwen2.5-VL-7B reached 82.8% on VisDrone and 67.8% on COCO.
- **Carparts (industrial):** mean 25.4%, best 40.0% (Qwen2.5-VL-7B), worst 8.5% (DeepSeek-VL-1.3B). Models confused similar parts, such as hood vs fender.
- **HAM10000:** mean 7.3%; six of nine models scored about zero and defaulted to the majority class.
- **Brain Tumor:** mean 48.9%; DeepSeek-VL-1.3B reached 63.0%.
- **Stability:** Gemma3-12B was the most consistent across domains (CV 13.5%).
- **QC Score:** only Qwen2.5-VL-7B met the production-ready criterion (QC Score 0.47), still below the 0.6 threshold for full autonomy.
- **Latency:** compact models ran in under 2 s per image; 11-24B models took 11-44 s per image.
- **Encoders:** CLIP-ViT-L encoders (LLaVA family) did well on natural images; SigLIP encoders (Gemma3, Granite) were more balanced across domains.
- **Conclusion:** the VLMs are suitable for supervised deployment, not autonomous deployment.

## Limitations
- Zero-shot only; fine-tuned VLMs may score much higher.
- Semantic assessment only; no spatial or IoU assessment.
- 200 samples per domain, with labels checked by a single author.
- The "industrial" domain is car-part classification, not true defect inspection.
- Wide confidence intervals.

## Transferable ideas for the FYP pipeline
- **Vision:** do not expect zero-shot open VLMs to classify fine-grained laser-cut defects reliably. Plan for LoRA fine-tuning or few-shot exemplars, or use a dedicated defect detector with the VLM as a verifier and explainer.
- **LLM reasoning:** use a JSON output schema with classification, confidence and reasoning, plus a robust cascading parser, so that the outputs can feed the fusion and decision stages.
- **Evaluation:**
  - Report per-class accuracy, bootstrap confidence intervals and stability across runs.
  - Define acceptance tiers, for example a ≥70% industrial threshold before moving from assistant to autonomous.
  - Check for majority-class collapse.
- **Deployment:**
  - Run local Ollama models (Qwen2.5-VL-7B, Gemma3) on a single consumer GPU to keep machine data on-premise.
  - Budget per-image latency (under 2 s for small models).
  - Prefer consistent models over ones with high peak but unstable accuracy.
