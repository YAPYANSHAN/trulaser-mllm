# Predicting Invasiveness of Lung Adenocarcinoma from Chest CT with Few-shot Vision-Language Ternary Classification Model

- **Citation (IEEE):** N. Xu, Q. He, L. Wang, et al., "Predicting Invasiveness of Lung Adenocarcinoma from Chest CT with Few-shot Vision-Language Ternary Classification Model," *npj Digital Medicine*, vol. 9, art. 60, 2026, doi: 10.1038/s41746-025-02229-2.
- **Domain:** Medical imaging (radiology) — few-shot in-context learning with a VLM
- **Relevance to FYP (1-5):** 3 — different domain, but a strong template for feature-checklist prompting + few-shot exemplars with an MLLM on subtle visual defects, with shot-count ablation and a human-in-the-loop reader study.

## Problem
Pre-operative ternary classification of pure ground-glass nodules (pre-invasive vs minimally invasive vs invasive adenocarcinoma) is hard; subtle features (air bronchograms, vacuolisation, vascular penetration) are difficult for conventional CV models, and prior work is mostly binary.

## Data & modalities
Retrospective multicentre cohort of 848 patients (333 pre-invasive, 376 MIA, 139 IAC) across four centres; each nodule's CT slices converted to a video (848 videos, mean 17.07 s, 512×512×N); text prompts with prior knowledge; nodule coordinates supplied.

## Method
- **GPT-4o** (video-capable VLM) compared with **Molmo**.
- **Textual prior knowledge:** ten guideline-derived features (volume, mass, density, shape, margin, vacuolisation, air bronchogram, vascular penetration, vessel thickening, pleural indentation) in the prompt.
- **In-context few-shot "training":** 0/1/3/5/10/20/30-shot exemplar videos with class ratio ~40:40:20.
- Step-by-step prompting: locate lesion from given coordinates → segment/draw boundary → detect the ten features → give diagnosis.
- Evaluation: Dice vs radiologist masks, accuracy/sensitivity/specificity/F1/AUC with DeLong tests; six radiologists rated output quality (reliability, harm, missing content); reader study with six other radiologists with/without GPT-4o assistance (four-week washout). No fine-tuning or RAG.

## Results
- Boundary delineation mean Dice 0.76.
- Twenty-shot best: accuracy 0.75, sensitivity 0.74, specificity 0.86, precision 0.75, F1 0.74, AUC 0.80 (95% CI 0.77–0.83); significantly better than <20 shots (P<0.01); 30-shot not significantly different (P=0.311). Accuracy rose from 0.57 (zero-shot) to 0.79 with more shots. Molmo AUC 0.45.
- Reader study (110 patients): unaided radiologist accuracy 0.34–0.67 vs GPT-4o 0.73; with assistance 0.62–0.86 (11–29% gains, McNemar P<0.001).

## Limitations
Nodule coordinates were provided (no automatic detection); further external validation needed; privacy risk of online models; only GPT-4o and Molmo compared; benign GGNs excluded; no longitudinal data.

## Transferable ideas for the FYP pipeline
- **Vision / LLM reasoning:** give the MLLM an explicit checklist of laser-cut quality features (striation angle, dross presence/height, burr, edge discolouration/oxidation, kerf width, bevel-angle deviation, top-edge rounding) drawn from TRUMPF/ISO 9013 guidance, and have it report each before diagnosing.
- **Few-shot design:** ablate shot count (0→30) with class-balanced exemplar images of each defect type; expect plateauing returns.
- **Localisation:** supply ROI coordinates (from a detector or part geometry) so the VLM focuses on the relevant edge.
- **Evaluation:** run an operator reader study (with/without LLM assistance) and collect ratings of reliability, harm and missing content.
