# Gear fault diagnosis of wind turbine drivetrains using multi-source information fusion and ensemble learning in a simulation bench study

- **Citation (IEEE):** X. Kang, L. Shao, B. Zhao, "Gear fault diagnosis of wind turbine drivetrains using multi-source information fusion and ensemble learning in a simulation bench study," *Scientific Reports*, vol. 16, art. 11321, 2026, doi: 10.1038/s41598-026-41117-x.
- **Domain:** Mechanical engineering / rotating-machinery condition monitoring (planetary gearbox fault diagnosis).
- **Relevance to FYP (1-5):** 3 — industrial machine fault diagnosis with classical multi-sensor feature fusion and ensembles; no LLM or images, but provides a strong interpretable tabular/signal baseline and an ablation template.

## Problem
Under variable wind-turbine speeds, static filtering misses gear fault frequency bands and single-source signals are swamped by noise; unsupervised dimensionality reduction (PCA, t-SNE) ignores labels and blurs class boundaries.

## Data & modalities
Open WT-Planetary Gearbox Dataset (Liu et al., Beijing University of Technology) from a Drivetrain Dynamic Simulator: orthogonal X/Y piezoelectric accelerometer vibration + rotary-encoder speed, synchronously sampled at 48 kHz. Five sun-gear states (healthy, tooth breakage, wear, root crack, missing tooth) at eight motor input frequencies (20-55 Hz).

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
(1) Z-score standardisation (99.20% vs 91.60% with Min-Max, which is outlier-sensitive). (2) Closed-loop "speed smoothing - dynamic filtering - envelope analysis": Gaussian-smoothed speed drives adaptive band-pass parameters around the mesh/fault frequencies before envelope demodulation. (3) Feature-level fusion of time-domain statistics, frequency-domain energy, wavelet-packet energies and gear meshing features from vibration and speed. (4) LDA supervised dimensionality reduction. (5) Accuracy-weighted voting ensemble of SVM (RBF, C=10, sigma=10 via grid search), KNN, Random Forest and Naive Bayes, weights normalised from validation accuracies. No deep LLM; compared with 1D-CNN and Bi-LSTM.

## Results (key numbers and metrics)
SVM accuracy: X-vibration only 80.4%, dual-direction vibration 89.6%, speed only 92.8%, fused + LDA 99.2%. Individual classifiers: KNN 88.8%, RF 98.4%, NB 95.2%, SVM 99.2%; ensemble 98.8% (reported as final, more robust). Baselines: 1D-CNN 97.20%, Bi-LSTM 50.00%. Ablation: raw + SVM 76.7% -> +closed-loop preprocessing 80.4% -> +multi-source fusion 95.7% (+15.3, largest gain) -> +LDA 96.1% -> +ensemble 98.8%.

## Limitations
Single simulation bench; transferability to other test benches/real turbines not verified; small sample counts per class; ensemble accuracy slightly below best single SVM on test.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** Engineer physics-informed features from TruLaser logs (e.g., gas pressure stability, laser power ramp, feed-rate deviations, nozzle temperature) and standardise with z-score; condition features on operating regime the way speed drives the filter here (material/thickness-adaptive thresholds).
- **Fusion:** Demonstrates that multi-source fusion gives the largest gain; justify fusing machine-database parameters with images rather than relying on one modality.
- **LLM reasoning:** Use a classical ensemble (SVM/RF) as a fast, verifiable fault-class predictor whose output and top features are passed to the LLM as evidence.
- **Evaluation:** Copy the stepwise ablation table format (baseline -> +each stage) and compare against 1D-CNN/LSTM baselines; test across operating conditions.
