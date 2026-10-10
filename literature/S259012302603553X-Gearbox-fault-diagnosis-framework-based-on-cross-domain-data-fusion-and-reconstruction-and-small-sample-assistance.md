# Gearbox fault diagnosis framework based on cross domain data fusion and reconstruction and small sample assistance

- **Citation (IEEE):** X. Sun, L. Zhang, X. Zheng, et al., "Gearbox fault diagnosis framework based on cross domain data fusion and reconstruction and small sample assistance," *Results in Engineering*, vol. 32, Art. no. 112537, 2026, doi: n/a.
- **Domain:** Industrial fault diagnosis (planetary gearbox vibration) / small-sample learning, simulation-to-real
- **Relevance to FYP (1-5):** 2 - vibration-based gearbox diagnosis with no LLM, images or text. The approach of using a few real fault samples to calibrate simulated data is transferable when laser-cutting defect data are scarce.

## Problem
Real fault vibration samples of planetary gearboxes are scarce: operating conditions are complex, fault testing raises safety concerns, and testing is costly. Data-driven models trained on little data generalise poorly, and GAN-generated samples may lack physical fidelity.

## Data & modalities
- **Test bench:** a planetary gearbox (sun, planet and ring gears) with artificially fabricated faults: broken tooth, wear and pitting.
- **Measured signals:** vibration signals under normal and fault conditions.
- **Simulated signals:** fault signals from a multi-source, real-time speed-driven ADAMS multibody dynamics model.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
1. Generate physically realistic simulated fault signals with ADAMS, driven by measured variable-speed data.
2. Decompose the simulated fault signals and the measured normal signals into IMFs using Cochlear-Inspired Variational Mode Decomposition (CI-VMD, with a tonotopic prior).
3. Optimise the IMF contribution weights (42 weights) with the Whale Optimization Algorithm (WOA). The fitness is the validation accuracy of a CNN on a *small set of real fault samples*, which act as "knowledge guidance" and not as training data.
4. Train an optimised CNN on the reconstructed signals and test it on unseen real faults.

## Results (key numbers and metrics)
- With 10 real fault samples per fault type (30 total) as the validation set, validation accuracy reaches 96.67%.
- Test accuracy on unseen real fault signals stays above 90%, including at a 1:5 validation-to-test ratio (averaged over 20 random test draws).
- Ablations confirm each component's contribution.

## Limitations
- Requires building an accurate dynamic simulation model (ADAMS), which is system-specific.
- Only three fault types on one test bench.
- WOA optimisation over CNN validation runs is computationally costly.
- Future work: industrial-scale data and more realistic simulation constraints.

## Transferable ideas for the FYP pipeline
- **Data ingestion/vision:** if real TruLaser defect images or logs are scarce, generate simulated or synthetic samples (e.g., from cut-quality physics models or rendered defect images). Use a *small real labelled set only as a calibration/validation signal* to tune the mix of synthetic samples, rather than training on it directly.
- **Tabular/time-series:** use signal decomposition (VMD) for any high-rate sensor data (e.g., process-monitoring photodiode signals) before classification.
- **Evaluation:** report accuracy on unseen *real* samples when training on synthetic data, with repeated random test draws.
