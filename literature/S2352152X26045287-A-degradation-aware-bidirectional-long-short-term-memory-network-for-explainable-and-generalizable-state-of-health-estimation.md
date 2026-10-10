# A degradation-aware bidirectional long short-term memory network for explainable and generalizable state-of-health estimation

- **Citation (IEEE):** S. Ben Atitallah, I. Jarraya, M. Driss, et al., "A degradation-aware bidirectional long short-term memory network for explainable and generalizable state-of-health estimation," *Journal of Energy Storage*, vol. 182, Art. no. 124864, 2026, doi: n/a.
- **Domain:** Battery prognostics (SOH estimation) / explainable time-series deep learning
- **Relevance to FYP (1-5):** 2 - batteries, no LLM. The evaluation rigour (leave-one-unit-out), MC-dropout uncertainty and SHAP/LIME explanations are transferable to the tabular/time-series stage.

## Problem
Deep SOH estimators are often evaluated with random splits that leak cycles of the test cell into training, give little evidence of generalisation across cells, and are opaque about which signals drive their predictions.

## Data & modalities
The NASA Ames battery dataset (eight cells), with timestamp-level electrochemical measurements as time series.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Features:** a 17-dimensional engineered representation of raw measurements, capacity lags, rolling statistics, degradation-rate indicators, smoothed trends and a normalised aging-stage indicator.
- **Model:** a compact BiLSTM (47,169 parameters) over sliding windows of 10 observations. Trained with Huber loss, batch normalisation, dropout and L2 regularisation.
- **Evaluation protocols:** pooled 5-fold CV, per-cell within-distribution testing, and Leave-One-Battery-Out (LOBO).
- **Uncertainty and explanation:** Monte Carlo dropout for uncertainty; SHAP and LIME for feature attribution.

## Results (key numbers and metrics)
| Protocol | RMSE | R² |
|---|---|---|
| 5-fold CV | 0.00697 ± 0.00086 | 0.9993 ± 0.0002 |
| Per-cell | 0.00499 | 0.9964 |
| LOBO | 0.00545 | 0.9960 |

SHAP and LIME mainly emphasise capacity-history and degradation features. MC-dropout shows that predictive spread varies across cells and degradation regions.

## Limitations
- Small benchmark (eight NASA cells) with a single chemistry.
- The aging-stage normalisation depends on training-derived cycle counts.
- Broader distribution shifts (temperature, chemistry) are not tested.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** engineer lag, rolling-statistic and trend features from TruLaser machine-table logs (e.g., nozzle usage, lens contamination indicators, laser power drift) for a compact sequence model or tree model.
- **Evaluation:** use leave-one-machine-out, leave-one-job-out or leave-one-material-out splits to avoid temporal leakage, since random splits overstate accuracy.
- **LLM reasoning:** pass SHAP/LIME attributions and MC-dropout uncertainty to the LLM as structured evidence. The LLM's explanation can then cite which parameters drove a predicted fault and how confident the model is.
