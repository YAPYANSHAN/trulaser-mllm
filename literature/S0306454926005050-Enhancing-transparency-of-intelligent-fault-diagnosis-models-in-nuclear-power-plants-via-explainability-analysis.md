# Enhancing transparency of intelligent fault diagnosis models in nuclear power plants via explainability analysis

- **Citation (IEEE):** G. Qian, Y. Huang, H. Zhu, et al., "Enhancing transparency of intelligent fault diagnosis models in nuclear power plants via explainability analysis," *Annals of Nuclear Energy*, vol. 239, Art. no. 112617, 2026, doi: 10.1016/j.anucene.2026.112617.
- **Domain:** Industrial fault diagnosis / explainable AI (nuclear power, rotating equipment)
- **Relevance to FYP (1-5):** 3 — industrial fault diagnosis on both signal and structured tabular data with SHAP/Grad-CAM explanations checked against physics; no LLM or images of parts.

## Problem
ML fault-diagnosis models for nuclear power plants (NPPs) perform well but are black boxes, blocking deployment and regulatory acceptance in safety-critical settings. The study asks whether model decision logic can be shown to match fault mechanisms at equipment and system levels.

## Data & modalities
- **Equipment level:** CWRU bearing vibration data as raw 1-D signals (Dataset A1) and as STFT time-frequency spectrogram images (Dataset A2).
- **System level:** PCTRAN-simulated PWR transients (Dataset B), structured tabular time-varying process parameters, 10 classes: normal, LOCA cold/hot leg, MSLB inside/outside containment, SGTR, rod withdrawal, load rejection, turbine trip, loss of flow.

## Method
- Classifiers: 1-D CNN, 2-D CNN (spectrograms), SVM, Random Forest, XGBoost.
- Explainability: Grad-CAM (CNN), SHAP (model-agnostic), XGBoost intrinsic feature importance; layer-wise CAM entropy to show progression from dispersed to focused attention; t-SNE and SSIM for data analysis.
- Cross-method consistency checks (Grad-CAM vs SHAP; SHAP vs tree importance; SHAP across XGBoost and SVM) and comparison of top features with known fault physics.
- No LLM, RAG or fine-tuning.

## Results
- Dataset A1 (raw): 1D-CNN 89.87%; SVM 53.27%, RF 58.93%, XGBoost 53.10%.
- Dataset A2 (STFT): 2D-CNN 99.50%.
- Dataset B (tabular): XGBoost 99.73%, RF 98.61%, SVM 97.16%, 1D-CNN 89.57%.
- Grad-CAM and SHAP highlighted consistent physically meaningful time-frequency regions; SHAP feature rankings agreed with XGBoost importance and with fault mechanisms.

## Limitations
System-level data are simulated (PCTRAN), so sim-to-real shift remains; explanation robustness under noisy, incomplete or imbalanced data not addressed; post-hoc explanations only; no integration with physical models or operator knowledge yet (stated as future work).

## Transferable ideas for the FYP pipeline
- **Tabular:** for TruLaser machine-database tables, a gradient-boosted tree (XGBoost) is a strong baseline; its SHAP values give per-prediction parameter attributions.
- **LLM reasoning:** pass top-k SHAP features (e.g., "gas pressure −0.3 contribution") into the LLM prompt as evidence, and ask the LLM to explain them against TRUMPF documentation — turning numeric XAI into readable diagnosis.
- **Vision:** use Grad-CAM on a defect-image CNN to show which part of the cut edge drove the prediction, and include the heatmap in the report.
- **Evaluation:** check explanation consistency across two methods and against known physics/expert rules as an explanation-quality metric.
- **Data:** transforming raw signals to spectrogram images can make them usable by vision models/VLMs.
