# TabPFN-enabled multimodal diagnostic framework with interphase interference compensation for metal oxide surge arresters

- **Citation (IEEE):** L. Zhong, Z. Tang, Y. Liu, et al., "TabPFN-enabled multimodal diagnostic framework with interphase interference compensation for metal oxide surge arresters," *Results in Engineering*, vol. 32, Art. no. 113250, 2026, doi: 10.1016/j.rineng.2026.113250.
- **Domain:** Power equipment fault diagnosis / tabular foundation model (TabPFN), current-temperature fusion
- **Relevance to FYP (1-5):** 3 - a different equipment type, but a tabular foundation model plus physics-based feature correction on small, multimodal tabular datasets. This is highly applicable to the FYP's structured machine-database stage.

## Problem
Diagnosing metal oxide surge arresters (MOSAs) from leakage current is distorted by interphase capacitive interference in compact three-phase layouts. Existing compensation needs detailed station-specific geometric modelling, and fault data are scarce.

## Data & modalities
- **Simulation data:** a multi-physics (FE) dataset covering seven operating conditions, including normal, aging, and wet pollution or moisture in the upper and lower units.
- **Features:** leakage-current phasor features plus temperature features, both tabular.
- **Field data:** in-situ leakage current data from 500 kV MOSAs (Fushun Electric Porcelain Factory), used for compensation validation.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Interference compensation:** a vector-decomposition method compensates the 50 Hz fundamental leakage-current phasors by estimating adjacent-phase capacitive currents from the measured three-phase current vector alone.
- **Feature fusion:** compensated current features are combined with temperature features (multimodal tabular fusion).
- **Classifier:** TabPFN, a pre-trained transformer for small tabular data that predicts in-context without task-specific training (the paper notes it suits up to about 10,000 samples and 500 features). Compared against CatBoost and LightGBM.
- **Evaluation:** phase-blocked, severity-blocked and simulation-sweep-blocked holdouts, with bootstrap (2000 replicates) 95% confidence intervals.

## Results (key numbers and metrics)
- **Compensation accuracy:** maximum amplitude error falls from 6.93% to 0.35%, and maximum phase-angle error from 1.92% to 0.68%. Robust to voltage unbalance, harmonics, capacitance uncertainty, asymmetry and temperature-dependent conductivity.
- **Current-only diagnosis:** compensation raises accuracy and Macro-F1 from 0.757/0.736 to 0.802/0.786.
- **Current + temperature with TabPFN:** accuracy 0.886 and Macro-F1 0.883, numerically above CatBoost and LightGBM but not statistically significant. Aging faults are identified with F1 = 1.000.
- **Field data:** amplitude, phase-angle and resistive-current ranges are reduced by 82.3%, 73.1% and 70.9%.

## Limitations
- Fault classification is trained and evaluated mostly on simulated data.
- TabPFN's advantage over gradient-boosted trees is not statistically significant.
- Some classes have lower F1 under phase-blocked splits.
- Field validation covers compensation, not fault labels.

## Transferable ideas for the FYP pipeline
- **Tabular:** use TabPFN as a strong, training-light baseline classifier on TruLaser machine-database tables (process parameters, alarm counts, sensor summaries → fault class). Compare against CatBoost and LightGBM with bootstrap CIs.
- **Data ingestion:** apply physics-based correction to raw signals before modelling (e.g., normalise cutting parameters by material and thickness, or compensate for known sensor offsets).
- **Fusion:** simple feature-level fusion of two physical modalities (here current + temperature; for the FYP, process parameters + image-derived defect metrics) gave clear gains.
- **Evaluation:** blocked holdouts (by severity, configuration or simulation sweep) for more honest generalisation estimates.
