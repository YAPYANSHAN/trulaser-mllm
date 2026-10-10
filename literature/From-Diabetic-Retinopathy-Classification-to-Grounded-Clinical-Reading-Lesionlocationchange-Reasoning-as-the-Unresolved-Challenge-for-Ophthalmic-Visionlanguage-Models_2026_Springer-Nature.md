# From Diabetic Retinopathy Classification to Grounded Clinical Reading: Lesion-location-change Reasoning as the Unresolved Challenge for Ophthalmic Vision-language Models

- **Citation (IEEE):** H. Tabuchi, M. Tanabe, K. Kihara, et al., "From diabetic retinopathy classification to grounded clinical reading: lesion-location-change reasoning as the unresolved challenge for ophthalmic vision-language models," *SN Comprehensive Clinical Medicine*, vol. 8, art. 321, 2026, doi: 10.1007/s42399-026-02549-8.
- **Domain:** Medical imaging / ophthalmology; critical narrative review of VLM grounding, hallucination and RL alignment.
- **Relevance to FYP (1-5):** 3 — medical domain, but its argument (global labels are not enough; VLM outputs must bind defect identity + location + change with verifiable spatial evidence) and its grounding-aware evaluation/reward design map directly onto evidence-based laser-cut defect diagnosis.

## Problem
AI can classify diabetic retinopathy (DR) at image level and even segment lesions, but clinical reading requires statements like "hard exudates have increased in the macula", binding lesion identity, anatomical location and longitudinal change. Current VLMs/LVLMs/MLLMs (GPT-4V, GPT-4o, ophthalmic LVLMs) fail here through spatial errors, hallucination and weak localisation.

## Data & modalities
No new data. Reviews fundus photographs, lesion masks (IDRiD, DeepDR), retinal foundation models (RETFound), contrastive ophthalmic VLMs (FLAIR — 38 public fundus datasets, EyeCLIP, RetiZero), general MLLM evaluations and regulatory documents.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Critical narrative review. Defines a six-step grounded chain: anatomy (fovea/macula) localisation, lesion detection, spatial relation inference, longitudinal registration, quantification, text generation. Argues saliency maps (Grad-CAM, attention) are not verifiable grounding; prefers structured outputs (coordinates, masks, lesion-location-change triples). Discusses RL: final-diagnosis rewards cannot teach localisation; proposes dense verifiable rewards (fovea error, lesion Dice/IoU, lesion-to-fovea distance, registration error, text-triple agreement), citing ViGoR and Visual-RFT; RLHF reserved for narrative fluency. Proposes a lesion-location-change grounding benchmark comparing general VLMs, domain VLMs, segmentation-first pipelines + LLM report generation, and specialists.

## Results (key numbers and metrics)
Narrative; no pooled estimates. Summarises that cited GPT-4V/GPT-4o ophthalmic studies found accuracy insufficient for clinical decisions. Recommends reporting localisation error, Dice/IoU/AUC, relation metrics, longitudinal agreement, calibration, abstention and text-image consistency.

## Limitations
Conceptual, not empirically validated; proprietary models change rapidly; includes some non-clinical CS papers and one arXiv preprint; dense annotation for rewards is expensive and vulnerable to reward hacking.

## Transferable ideas for the FYP pipeline
- **Vision + LLM reasoning:** Use a segmentation/detection-first pipeline (defect masks on cut edge, location on part contour) and pass structured triples (defect type, location e.g. corner/lead-in/bevel edge, severity) to the LLM rather than raw images only.
- **LLM reasoning:** Require the LLM to output structured, checkable evidence (defect, location, linked machine parameter, change vs previous job) before the narrative diagnosis.
- **Tabular/time-series:** "Longitudinal change" maps to comparing current job against previous runs/settings in the machine database (e.g., dross increasing since nozzle change).
- **Evaluation:** Score text-image consistency, localisation accuracy, calibration and abstention ("insufficient evidence") — not just final fault-label accuracy.
- **Fine-tuning:** If doing RL/GRPO-style tuning, use verifiable rewards (correct defect class, IoU, correct parameter direction) rather than only final-answer reward.
