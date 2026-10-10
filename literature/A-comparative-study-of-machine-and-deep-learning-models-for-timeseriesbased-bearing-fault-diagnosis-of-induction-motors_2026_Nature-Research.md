# A comparative study of machine and deep learning models for time-series-based bearing fault diagnosis of induction motors

- **Citation (IEEE):** K. Hamani, M. Kuchar, M. Sobek, et al., "A comparative study of machine and deep learning models for time-series-based bearing fault diagnosis of induction motors," *Scientific Reports*, vol. 16, art. 29387, 2026, doi: 10.1038/s41598-026-57638-4.
- **Domain:** Industrial fault diagnosis / condition monitoring (time series)
- **Relevance to FYP (1-5):** 3 - industrial fault diagnosis with multi-sensor fusion and model benchmarking; no LLM, but directly informs the tabular/time-series branch of the pipeline.

## Problem
Bearing-fault detection in induction motors under varying load is difficult; load affects fault-signature detectability. Conventional methods rely on heavy preprocessing and handcrafted features.

## Data & modalities
Custom 15-class dataset: healthy and faulty bearing states at 0%, 50% and 100% load. Signals: stator currents (phase 1, phase 2), rotor speed, and flux-induced voltage (RMSFC voltage). Raw signals are windowed, normalised and resampled/aligned when needed.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Models compared on raw windowed signals: SVM, Random Forest (ML); MLP, LSTM, TCN, Transformer (DL).
- Early (input-level) fusion of signal channels; systematic study of feature (sensor) combinations from 1 to 4 signals; feature-importance analysis.
- Hyperparameter tuning and regularisation search; k-fold cross-validation; separate deployment-oriented test on unseen samples.
- No LLM/VLM, RAG or KG.

## Results (key numbers and metrics)
- LSTM: 100% training/validation accuracy; single-feature average 85.63%; all four features 99.7% accuracy/F1.
- SVM and TCN gave the most consistent generalisation on unseen deployment test data (perfect predictions on tested samples).
- RF: best single feature 99.23% (avg 97.74%), 99.73% with two, 99.80% with three features.
- MLP: single-feature average 55.13%, all four features 97.11% accuracy.
- Transformer: single-feature average 62.20%; best configurations around 99.6-99.7%; authors note it needs more tuning.
- Multi-signal fusion outperforms single-sensor models; no-load condition is the hardest.

## Limitations
k-fold CV is not ideal for temporal data (leakage risk); only bearing faults; no real-time controller or inverter (PWM) supply tested; dataset not public.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** benchmark simple ML (SVM/RF) against LSTM/TCN/Transformer on TruLaser machine signals (laser power, gas pressure, feed rate, focus position) before handing results to the LLM; light models can be the "evidence generators".
- **Data ingestion:** windowing, per-window normalisation and resampling to align channels with different sampling rates.
- **Fusion / evaluation:** perform sensor-combination ablation to identify which machine-database fields are most diagnostic; feed feature-importance rankings to the LLM as evidence.
- **Evaluation:** use time-series split / walk-forward validation instead of k-fold, and stratify results by operating condition (analogous to load = material thickness/speed regime).
