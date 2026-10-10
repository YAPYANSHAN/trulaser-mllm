# Multimodal large language models for bladder tumor detection in cystoscopy: a retrospective benchmarking study

- **Citation (IEEE):** Y. Prat, H. Mahmud, A. Tsur, et al., "Multimodal large language models for bladder tumor detection in cystoscopy: a retrospective benchmarking study," *World Journal of Urology*, vol. 44, art. 670, 2026, doi: 10.1007/s00345-026-06761-y.
- **Domain:** Medical imaging (urology) — zero-shot MLLM image classification
- **Relevance to FYP (1-5):** 3 — unrelated domain but a clean protocol for prompt engineering, calibrated probability outputs and confidence-based abstention with off-the-shelf MLLMs, directly reusable for defect-image classification.

## Problem
Visual interpretation of cystoscopy is variable and conventional AI needs large curated datasets. Can general-purpose MLLMs classify cystoscopy images zero-shot, and does prompt engineering improve accuracy and calibration?

## Data & modalities
Public dataset of 1,754 labelled cystoscopy images from 23 TURBT patients (white-light and narrow-band imaging), four classes (high-grade, low-grade, non-tumour lesion, normal tissue); primary task benign vs malignant.

## Method
- Models: GPT-5.2, GPT-5, GPT-5-Mini, GPT-5-Nano via API; 12 conditions × 1,754 images = 21,048 inferences.
- Output constrained to a **JSON schema** with a four-class probability vector summing to 100%.
- Prompts: P-1 direct role prompt (zero-shot); P-2 "book-based" — appends textbook class descriptors (domain-knowledge injection); P-3 optimised — explicit decision rules, self-reflection/backtracking, tiebreakers, ignore artefacts (instruments), conservative guardrails to reduce false negatives.
- Calibration: Brier score, Expected Calibration Error; **high-confidence triage** with abstention thresholds chosen via a loss function; modality-stratified analysis.
- No fine-tuning, RAG or KG.

## Results
- GPT-5 + P-3: accuracy 86.7%, specificity 94.1%, sensitivity 82.5%, F1 88.7%. GPT-5-Mini + P-3: accuracy 89.2%, specificity 88.4%, sensitivity ~89%.
- P-3 vs P-1 accuracy gains 0.4–5.0 points; only GPT-5-Nano's gain significant (P<0.001). Brier score significantly lower with P-3 vs P-2 for all models.
- High-confidence triage (GPT-5 + P-3): 98.1% accuracy, 94.6% specificity, 99.1% sensitivity at 62.0% coverage.

## Limitations
Retrospective, still images rather than video; single public dataset of only 23 patients; no clinical variables integrated; accuracy gains from prompting mostly not significant; closed proprietary models.

## Transferable ideas for the FYP pipeline
- **LLM reasoning / vision:** encode TRUMPF documentation defect descriptions (burr, dross, striations, bevel-angle deviation) as "book-based" class descriptors inside the prompt — the analogue of P-2; add decision rules and artefact-ignoring instructions as in P-3.
- **Output design:** force a JSON probability distribution over fault classes so outputs are machine-checkable and calibratable.
- **Evaluation:** report Brier/ECE alongside accuracy; use an abstention threshold so low-confidence diagnoses are routed to an operator — a safety mechanism for the FYP.
- **Deployment:** compare large vs mini/nano models for cost-performance trade-off.
