# Artificial Intelligence-Assisted Quality Assessment of Mid-Trimester Ultrasound Examinations Using Large Vision-Language Models

- **Citation (IEEE):** J. Zhang, B. Feng, Y. Cheng, et al., "Artificial intelligence-assisted quality assessment of mid-trimester ultrasound examinations using large vision-language models," *BMC Pregnancy and Childbirth*, vol. 26, art. 614, 2026, doi: 10.1186/s12884-026-09073-6.
- **Domain:** Medical imaging / quality control of ultrasound examinations
- **Relevance to FYP (1-5):** 3 - medical domain, but the CNN-to-text + LoRA-fine-tuned VLM pattern with JSON-structured verdicts and listed defects is a near-direct template for image-based quality/fault assessment in the FYP.

## Problem
Quality control of mid-trimester fetal ultrasound (are all 20 required standard planes present and of adequate quality?) is labour-intensive, subjective and operator-dependent. CNN plane classifiers judge images in isolation and give no examination-level, interpretable verdict.

## Data & modalities
22,544 ultrasound planes: 273 internal and 29 external examinations (each with 20 required standard planes + 10-20 non-standard) plus 1,762 public Fetal Planes DB cases (12,400 images) for pre-training. Labels by two senior sonographers: plane type (21 classes), key-structure visibility, structural quality. Internal split 7:1:2; external set test-only. Modalities: images + CNN-generated text descriptors.

## Method
Two-stage system. (1) SonoNet-based CNN classifies standard planes and detects key structures; predictions converted to structured textual statements. (2) Open-source VLMs (Qwen2.5-VL-7B, Qwen2.5-VL-3B, LLaVA-1.6-7B, DeepSeek-VL2-2.8B) receive 25 image thumbnails plus per-plane CNN summaries in a structured prompt (system instruction + images + descriptors), LoRA fine-tuned to output standardised JSON: "qualified / not qualified" plus missing or inadequate planes/structures. Baseline: rule-based aggregation of CNN outputs. Locally deployed for privacy. Two-phase reader study with six sonographers (junior/mid/senior), two-week washout.

## Results
Examination-level F1 up to 0.944 (internal) and 0.922 (external) for fine-tuned VLMs, beating the CNN rule baseline and zero-shot models. Zero-shot DeepSeek-VL2-2.8B: accuracy 0.529, AUC 0.454. External LLaVA-1.6-7B: accuracy 0.966, AUC 0.974. Best plane-level F1 0.820 across error categories (missing plane, structure-poor, quality degradation). With AI assistance, reader F1 improved by 6.9-18.9 points, recall by 13.6-26.3 points, reading time fell by about 44-55%; MRMC p = 0.003.

## Limitations
Small external validation; CNN precision dropped across centres (vendor/preset variation); binary qualified/not-qualified output rather than graded score; treats independent 2D images, not video sweeps; same cases reviewed in both reader-study phases.

## Transferable ideas for the FYP pipeline
- **Vision -> fusion:** run a specialised detector/classifier on cut-part images (defect type, location, severity) and serialise its outputs as text alongside the raw images into the VLM - the VLM aggregates and explains rather than doing raw perception alone. The paper notes this made exam-level output robust to individual CNN errors.
- **LLM reasoning:** LoRA fine-tune a 3B-7B open VLM (Qwen2.5-VL) to emit JSON (verdict, defects found, likely cause, evidence) for a TruLaser job/part.
- **Evaluation:** compare against a rule-based aggregation baseline and a zero-shot VLM; run a small operator reader study measuring accuracy and time saved.
- **Deployment:** local deployment for confidential machine data.
