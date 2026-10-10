# Zero-shot detection of apical periodontitis on periapical radiographs using multimodal large language models: diagnostic accuracy and error patterns

- **Citation (IEEE):** M. Adıgüzel, F. Özeken, and T. Özeken, "Zero-shot detection of apical periodontitis on periapical radiographs using multimodal large language models: diagnostic accuracy and error patterns," *BMC Oral Health*, vol. 26, art. 1525, 2026, doi: 10.1186/s12903-026-09026-7.
- **Domain:** Dental radiology; zero-shot binary diagnosis with commercial multimodal LLMs (MLLMs).
- **Relevance to FYP (1-5):** 2 - a medical domain, but it shows clearly how different frontier MLLMs have very different implicit decision thresholds (false-positive vs false-negative bias) on binary defect-present/absent questions. That is directly relevant when choosing a VLM to flag cut-quality defects.

## Problem
General-purpose MLLMs are already used informally by clinicians. Their zero-shot diagnostic accuracy and, especially, their error tendencies (false positives vs false negatives) on dental radiographs had not been characterised.

## Data & modalities
- 120 periapical radiographs (60 positive for apical periodontitis, 60 healthy) from one university clinic, screened from 450.
- Exclusions: root-canal-filled teeth, poor image quality, artefacts.
- JPEG images with no preprocessing.
- Reference standard: consensus of two clinicians (Cohen's κ = 0.88), with Periapical Index (PAI) grading for subgroups (PAI = 3, n = 27; PAI ≥ 4, n = 33). There was no CBCT confirmation.
- Sample size was set by a power analysis: at least 108 pairs required for McNemar.

## Method
- **Models:** Claude 4.5 Sonnet, GPT-5.2 Thinking and Gemini 3.0 Pro, used through their standard chat interfaces in February 2026.
- **Prompt:** one standardised prompt that forces a binary "present/absent" answer and says to give "the most likely clinical decision" if uncertain. There were no examples and no fine-tuning.
- **Protocol:** randomised image order, a fresh chat for each image, and one run per image.
- **Metrics:** accuracy, sensitivity, specificity, PPV and NPV with Wilson confidence intervals; Cohen's κ; Cochran's Q with Bonferroni-adjusted McNemar tests; and an analysis of error patterns from the confusion matrices.

## Results

| Model | Accuracy | Sensitivity | Specificity | PPV / NPV | κ | TP/FP/TN/FN |
|---|---|---|---|---|---|---|
| Claude 4.5 Sonnet | 54.17% | 95.00% | 13.33% | 52.29% / 72.73% | 0.08 | 57/52/8/3 |
| GPT-5.2 Thinking | 59.17% | 20.00% | 98.33% | 92.31% / 55.14% | 0.18 | 12/1/59/48 |
| Gemini 3.0 Pro | 71.67% | 95.00% | 48.33% | 64.77% / 90.62% | 0.43 | 57/31/29/3 |

- Accuracy differed significantly across models (Cochran's Q p = 0.036). Gemini was better than Claude (adjusted p = 0.0015).
- The subgroup results did not depend on lesion severity: GPT-5.2 sensitivity was 18.5% at PAI = 3 and 21.2% at PAI ≥ 4, while Claude and Gemini were 92.6% and 97.0%.
- The differences come mainly from different false-positive rates and implicit thresholds.
- None of the models is suitable for independent clinical use; they are better used as clinician-supervised decision support.

## Limitations
- Single centre; the reference standard is 2D-only.
- Excluding difficult cases reduces representativeness.
- One run per image, so repeatability is not measured.
- Forced binary output means there are no probabilities, so ROC/AUC and calibration were not possible.
- Proprietary models change over time.
- There is no comparison with a trained CNN.

## Transferable ideas for the FYP pipeline
- **Evaluation:** for each defect class, report sensitivity, specificity, PPV and NPV, plus the confusion matrix, not just accuracy. Different VLMs (Claude, GPT, Gemini) may be biased towards over-calling or under-calling defects, and in a production setting the costs of these errors differ (scrapping good parts vs passing bad ones).
- **LLM reasoning:** ask for a calibrated confidence score or a graded severity, not a forced yes/no, so that thresholds can be tuned per use case (triage vs final QC) and ROC curves computed.
- **Evaluation:** use paired statistical tests (McNemar, Cochran's Q) to compare VLM backbones on the same image set, and run repeated queries to measure stability.
- **Fusion:** combine VLM outputs with conservative and liberal tendencies, or cross-check them against machine-parameter evidence, to balance false positives and false negatives.
- **Deployment:** keep a human in the loop for defect sign-off, and pin model versions with dated evaluations.
