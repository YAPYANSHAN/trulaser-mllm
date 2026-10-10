# Leakage-aware window-based chemometric monitoring for event-level anomaly detection in batch distillation

- **Citation (IEEE):** A. Marin-Lopez and J. A. Martínez-Cadena, "Leakage-aware window-based chemometric monitoring for event-level anomaly detection in batch distillation," *Chemometrics and Intelligent Laboratory Systems*, vol. 279, Art. no. 105909, 2026, doi: 10.1016/j.chemolab.2026.105909.
- **Domain:** Industrial process monitoring / time-series anomaly detection (chemical engineering)
- **Relevance to FYP (1-5):** 3 — no LLM, but its leakage-aware grouped validation, event-level metrics and alert rules transfer directly to machine-log anomaly detection for the laser cutter.

## Problem
Batch distillation is dynamic and phase-dependent; anomalies may appear only in short segments as changes in variability or trends. Random window-level splits of overlapping windows from the same run leak information and inflate scores, and window-level F1 does not reflect operational usefulness (missed events, false alarms).

## Data & modalities
Public batch-distillation reference dataset of multivariate sensor and actuator time series (temperatures, pressures, actuator signals). Final analytical set: 11,413 windows, 217 predictor variables, 119 experiments (81 anomalous, 38 normal); ~25.23% of windows anomalous. Single modality (tabular time series).

## Method
- Sliding temporal windows described by local statistical descriptors (mean, range, standard deviation, trends, etc.).
- Supervised classifiers compared: Logistic Regression, Decision Tree, Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting.
- Stratified grouped cross-validation with `experiment_key` as group, so all windows of one run stay in one fold.
- Event-level (experiment-level) evaluation, threshold and temporal-persistence alert rules, component-level ablation, permutation importance for interpretation.
- No LLM/VLM, RAG or fine-tuning.

## Results
- Extra Trees best window F1 0.655 ± 0.047; Random Forest F1 0.653 ± 0.037, ROC-AUC 0.862 ± 0.022, AP 0.719 ± 0.083.
- Event level: Random Forest detected 75/81 anomalous experiments (detection rate 0.926) with false alarms in 15/38 normal experiments; chosen as the operational model.
- Persistence/threshold rules trade sensitivity for fewer false alarms.
- Temperature-, pressure- and actuator-related variables most important; range and standard deviation the most informative descriptors.

## Limitations
Modest window-level F1; relatively high false-alarm rate on normal runs (15/38); single process and dataset; supervised labels required; no deep or multimodal models; descriptors are hand-crafted.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** compute windowed statistics (range, std, slope) over TruLaser machine-database signals (laser power, gas pressure, feed rate, nozzle/focus values) as compact features to feed the LLM or a classical detector.
- **Evaluation:** use grouped cross-validation by job/program/sheet so that windows or images of the same cutting job never sit in both train and test; report event-level (per job) detection and false-alarm rates in addition to window-level F1.
- **LLM reasoning:** feed permutation-importance rankings as evidence in the LLM prompt so diagnoses cite which parameters drove the alarm.
- **Deployment:** add persistence rules (N consecutive anomalous windows) before raising an alert to the operator, to control alarm fatigue.
- A Random Forest/Extra Trees baseline is a sensible non-LLM comparison for the FYP.
