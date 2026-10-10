# A physics-guided deformable convolution with cross-scale kernel transfer for interpretable few-shot fault diagnosis of cylindrical roller bearings

- **Citation (IEEE):** J. Shi, L. Xue, Z. Xue, et al., "A physics-guided deformable convolution with cross-scale kernel transfer for interpretable few-shot fault diagnosis of cylindrical roller bearings," *Applied Acoustics*, vol. 254, art. 111455, 2026, doi: 10.1016/j.apacoust.2026.111455.
- **Domain:** Industrial fault diagnosis — vibration-based bearing diagnosis (physics-guided deep learning, few-shot)
- **Relevance to FYP (1-5):** 2 — industrial diagnosis with physics priors and small/imbalanced data, but 1-D vibration only, rotating machinery, and no LLM or multimodal component.

## Problem
Purely data-driven CNNs learn statistical correlations rather than fault physics, overfit with scarce and imbalanced samples, and lack interpretability; unconstrained deformable convolution on vibration signals can break physical structure (transient impacts, periodic modulation).

## Data & modalities
1-D vibration signals (accelerometer, 51.2 kHz).
- Case 1: RV-reducer crankshaft cylindrical roller bearings with prefabricated inner/outer race faults, 3 speeds (10, 15, 18 rpm) × 3 loads (625, 937, 1250 Nm), 200 sliding-window samples per state per condition.
- Case 2: few-shot / imbalanced bearing dataset (classes RF, HS, IRF, ORF).

## Method
- **Physics-guided deformable convolution (PGDC)** layer with an impulse-feature branch and four differentiable constraint losses (impulse, sparsity, smoothness, periodicity) embedding fault priors.
- **Impulse-factor-driven cross-scale feature extraction (PGMFE):** ranks channel impulse sensitivity and propagates the most sensitive kernels across scales.
- **Adaptive physics-constrained fusion:** gating unit balances classification vs constraint losses.
- Baselines: 1DCNN, WDCNN, ResNet18, TFF-MSA, LTFAFormer; K-fold (5-fold) cross-validation; t-SNE and confusion matrices.

## Results
- Case 1: precision 99.34%, recall 99.37%, F1 99.35% vs WDCNN 96.34%, LTFAFormer 93.34%, TFF-MSA 89.69%, ResNet18 87.64%.
- Case 2 (few-shot/imbalanced): F1 99.58%.
- Only 22,379 parameters (WDCNN 22,707; ResNet18 11,321,155); ~2 s per training epoch.
- Ablation: removing PGDC drops IRF recognition 100%→85.70% and RF 98.30%→86.70%; removing PGMFE drops RF to 75.80%.

## Limitations
Lab test rig with prefabricated faults; limited fault types; complex cross-condition transfer, other components and online adaptation left for future work.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** if TruLaser exposes vibration or drive signals (e.g. axis drives, cutting head), small physics-constrained 1-D CNNs are a cheap, interpretable sub-model whose class probabilities can be passed to the LLM as evidence.
- **Training under scarcity:** adding domain-prior losses (e.g. expected periodicity, smoothness) is a generic way to regularise models trained on few labelled laser-fault samples.
- **Evaluation:** use K-fold CV, per-class confusion matrices and ablations under deliberately imbalanced splits, reporting parameter counts for deployability.
