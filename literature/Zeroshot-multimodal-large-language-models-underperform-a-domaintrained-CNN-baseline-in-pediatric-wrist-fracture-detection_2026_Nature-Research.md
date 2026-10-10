# Zero-shot multimodal large language models underperform a domain-trained CNN baseline in pediatric wrist fracture detection

- **Citation (IEEE):** M. Haupt, D. Weiß, T. Bellersen, et al., "Zero-shot multimodal large language models underperform a domain-trained CNN baseline in pediatric wrist fracture detection," *Scientific Reports*, vol. 16, art. 18873, 2026, doi: 10.1038/s41598-026-58763-w.
- **Domain:** Medical imaging (paediatric radiographs); head-to-head comparison of zero-shot commercial MLLMs with a supervised CNN.
- **Relevance to FYP (1-5):** 3 - a medical domain, but it is the clearest evidence that zero-shot MLLMs fail at detecting and localising subtle, fine-grained visual anomalies. It argues for a trained vision model (or adaptation) in the FYP defect stage, with the LLM reasoning over its outputs.

## Problem
How large is the gap between zero-shot commercial MLLMs and a simple domain-trained CNN on identical clinical images? What failure modes do the MLLMs show in classification, localisation and confidence reporting?

## Data & modalities
- The public GRAZPEDWRI-DX dataset: 20,327 paediatric wrist radiographs from 6,091 patients, with expert fracture labels and bounding boxes.
- A balanced test cohort of 1,000 patients (500 with fractures, 500 without), totalling 2,298 images, excluding casts, implants and uncertainty markers.
- The remaining 5,091 patients were used to train and validate the CNN, with a patient-wise 70/30 split.

## Method
**LLMs:**
- GPT-4o (2024-11-20), Claude 3.5 Sonnet (20241022) and Gemini 1.5 Pro-002, accessed through their APIs at temperature 0.
- Each received one standardised system and user prompt, with enforced JSON output: a binary label, up to 3 bounding boxes and a confidence score from 0 to 100.
- Images were sent in their native PNG resolution. There were no few-shot examples and no fine-tuning.
- A patient is counted positive if any of their views is positive (logical OR).

**CNN baseline:**
- Inception v3 pretrained on ImageNet, at 299×299, fine-tuned in two stages (head first, then the top 60 layers unfrozen).
- Class weights, augmentation, and early stopping on AUROC.
- Operating point chosen by Youden's J; five random seeds.

**Metrics:** balanced accuracy, sensitivity, specificity, F1, MCC, AUROC/AUPRC, IoU, and confidence calibration, with 2,000-sample bootstrap confidence intervals.

## Results

| Model | Accuracy / Balanced acc. | Sensitivity | Specificity | MCC | Other |
|---|---|---|---|---|---|
| CNN (Inception v3) | 0.821 / 0.821 | 0.748 | 0.894 | 0.65 | AUROC 0.905, AUPRC 0.920 |
| GPT-4o | 0.499 | 0.854 | 0.144 | about 0 | 428 false positives |
| Claude 3.5 Sonnet | 0.495 | 0.290 | 0.700 | -0.011 | |
| Gemini 1.5 Pro | 0.546 | 0.402 | 0.690 | 0.096 | |

- The CNN beats each LLM by about 28-33 percentage points in accuracy.
- **Localisation:** mean IoU was 0.072 (GPT-4o), 0.022 (Claude) and 0.094 (Gemini). Only 0.0-0.6% of boxes reached IoU ≥ 0.5. Boxes often landed on growth plates or soft tissue.
- **Confidence:** the scores were useless. Gemini returned 90 for 99.4% of images, and AUROC from signed confidence was about 0.49-0.52.
- **Subtypes:** the LLMs' sensitivity was flat across fracture subtypes, whereas the CNN's tracked fracture severity.

## Limitations
- One dataset and one anatomical region.
- The balanced cohort distorts PPV and NPV.
- Zero-shot only: no few-shot, calibration or fine-tuning arm.
- Closed APIs, so the models cannot be adapted.
- The CNN baseline is deliberately simple.
- Results are sensitive to the prompt, and there is session-level stochasticity.

## Transferable ideas for the FYP pipeline
- **Vision:** for subtle laser-cut defects (micro-burr, fine striations, slight bevel deviation), train or fine-tune a dedicated CNN or detector, even on a modest dataset. Pass its calibrated probabilities and boxes to the LLM rather than relying on the MLLM to detect directly.
- **LLM reasoning:** do not trust self-reported MLLM confidence numbers or bounding boxes. Take uncertainty from the trained model or from repeated sampling instead.
- **Evaluation:**
  - Always include a supervised baseline and use balanced accuracy, MCC and bootstrap confidence intervals.
  - Score localisation with IoU against annotations.
  - Report subgroup results by defect severity or type.
- **Data ingestion:** split by part or job (like patient-wise splits) to avoid leakage between images of the same part. Aggregate multiple views of a part with an explicit rule (e.g. OR).
- **Deployment:** lock API model snapshots and use temperature 0 with enforced JSON for reproducibility.
