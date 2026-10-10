# Tracking pleural sliding motion to assess lung overdistention using an open source algorithm: a proof-of-concept study on lung ultrasound scans

- **Citation (IEEE):** A. Costamagna, M. R. Smit, E. Pivetta, et al., "Tracking pleural sliding motion to assess lung overdistention using an open source algorithm: a proof-of-concept study on lung ultrasound scans," *Critical Care*, vol. 30, Art. no. 37, 2026, doi: 10.1186/s13054-025-05742-8.
- **Domain:** Medical imaging / ultrasound video motion tracking (critical care)
- **Relevance to FYP (1-5):** 1 - clinical ultrasound study with classical computer-vision tracking. It has no LLM or multimodal fusion and little that transfers beyond the general idea of quantifying motion in video with open-source tools.

## Problem
Pleural-line (PL) movement in lung ultrasound is used to detect pneumothorax and may indicate overdistention during mechanical ventilation. However, it is judged visually, and there is no quantitative tool. The questions are whether PL movement can be quantified with open-source motion tracking and whether it identifies overdistention.

## Data & modalities
Lung-ultrasound video clips from three cohorts:
1. 143 clips from 7 healthy volunteers (functional residual capacity vs. quiet breathing).
2. 336 clips from 40 ICU patients with blinded visual grading of lung sliding (absent, doubtful, limited, extensive).
3. 358 clips from 30 severe COVID-19 patients during PEEP titration, with electrical-impedance tomography (EIT) as the overdistention reference.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Open-source Python "Motion Tracker Beta" using OpenCV's CSRT (Channel and Spatial Reliability Tracking) tracker.
- Three PL landmarks plus a soft-tissue reference are tracked. Curves are smoothed and normalised to soft-tissue displacement.
- PL movement is defined as the maximum lateral displacement.
- Statistics: ordered logistic regression and Spearman correlation with EIT.
- No deep learning or LLM.

## Results (key numbers and metrics)
- Healthy volunteers: 1.2 ± 0.6 mm (FRC) vs. 5.4 ± 2.5 mm (quiet breathing), p < 0.01.
- ICU patients: 2.7 ± 1.2 mm (absent sliding) vs. 14.7 ± 5.8 mm (extensive), p < 0.01. Ordered logistic regression predicted absent sliding with 71% balanced accuracy.
- PEEP cohort: PL movement correlated with EIT overdistention (Spearman ρ = -0.6) and decreased from low to high PEEP (p < 0.01).

## Limitations
- Only lateral (X-axis) movement was used, with no vertical or 2D displacement.
- No lung-pulse filtering.
- The operator was not blinded and placed the landmarks manually.
- Clip durations and respiratory cycles were not standardised.
- Proof of concept: prospective studies and automated PL recognition are needed.

## Transferable ideas for the FYP pipeline
- **Vision (minor):** if the FYP uses process video (e.g., cutting-head or spark/plume camera), classical OpenCV trackers (CSRT) can extract simple, interpretable motion features. Normalising against a reference landmark removes camera or fixture motion, and the features can be fed to the LLM as numbers.
- **Evaluation:** validate a new quantitative indicator against an independent reference measurement with rank correlation, as PL movement is validated against EIT here. For example, validate an image-derived dross or roughness metric against profilometer measurements.
- Otherwise, little applies directly to the multimodal LLM pipeline.
