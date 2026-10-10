# Dynamic baseline-based fault diagnosis method for photovoltaic arrays integrating degradation modeling and CNN-transformer

- **Citation (IEEE):** Z. Tang, C. Wei, L. Zhou, et al., "Dynamic baseline-based fault diagnosis method for photovoltaic arrays integrating degradation modeling and CNN-transformer," *Energy Reports*, vol. 16, Art. no. 109511, 2026, doi: n/a.
- **Domain:** Industrial fault diagnosis (photovoltaic plant O&M) / time-series deep learning
- **Relevance to FYP (1-5):** 2 - a PV domain with no LLM or images. The "dynamic healthy baseline, then deviation features" idea transfers well to drifting laser-machine data.

## Problem
Long-running PV arrays mix natural performance degradation with multi-source faults. Static diagnostic baselines distort fault features, raise false alarms and miss slowly evolving faults.

## Data & modalities
Operational electrical and environmental data from a 10 MW PV plant (2018-2024), as time-series tabular data. Fault types include short circuit, open circuit, degradation, shading and mismatch.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
1. **Dynamic degradation baseline:** built with uncertainty theory, non-parametric kernel density estimation and linear regression. It evolves over time and corrects electrical parameters for natural aging; the extrapolated annual degradation is 0.73%.
2. **Baseline-deviation features:** deviations between the measured data and the dynamic baseline form feature vectors that amplify real fault signals. A clustering module groups operating conditions.
3. **CNN-Transformer hybrid:** the CNN captures local abrupt anomalies (short or open circuit), while the Transformer models long-range dependencies of slowly evolving faults (degradation, shading, mismatch).

## Results (key numbers and metrics)
- Full model: macro-F1 and balanced accuracy of 0.97, with a false-alarm rate below 2.5%.
- A CNN-LSTM variant (LSTM in place of the Transformer) scores 0.69 macro-F1 and 0.74 balanced accuracy.
- Ablations:
  - without degradation features: 0.95 / 0.96
  - without CNN: 0.94 / 0.93
  - without the clustering module: 0.98 / 0.98, slightly higher, as reported in Table 1

## Limitations
- Single plant.
- The baseline relies on long historical records and linear extrapolation of degradation.
- The ablation shows the clustering module is not clearly beneficial.
- No interpretability or reasoning layer.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** model a time-varying "healthy" baseline for TruLaser signals that drift with wear (e.g., laser output vs. setpoint, cutting-gas consumption, nozzle or protective-glass condition). Diagnose faults on the *deviation* from the baseline, not on raw values. This separates normal aging from faults and reduces false alarms.
- **Tabular/time-series:** a hybrid local-CNN + Transformer encoder for abrupt events (collisions, piercing failures) vs. slow drifts (lens contamination).
- **LLM reasoning:** pass deviation magnitudes and their direction to the LLM as evidence.
- **Evaluation:** report the false-alarm rate and balanced accuracy, not only accuracy.
