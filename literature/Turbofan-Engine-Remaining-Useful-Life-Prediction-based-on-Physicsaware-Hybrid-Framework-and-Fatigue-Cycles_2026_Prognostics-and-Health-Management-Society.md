# Turbofan Engine Remaining Useful Life Prediction based on Physics-aware Hybrid Framework and Fatigue Cycles

- **Citation (IEEE):** S. Szrama, "Turbofan engine remaining useful life prediction based on physics-aware hybrid framework and fatigue cycles," *International Journal of Prognostics and Health Management*, vol. 17, no. 1, 2026, doi: 10.36001/IJPHM.2026.v17i1.4733.
- **Domain:** Aerospace prognostics and health management (PHM); remaining useful life (RUL) prediction from sensor time series.
- **Relevance to FYP (1-5):** 2 - no LLM and no images, but its method of building physics-derived features and fusing them with sensor time series transfers to the tabular/time-series stage.

## Problem
Purely data-driven RUL models ignore material-fatigue physics, so they extrapolate poorly. Most studies validate only on simulated data (C-MAPSS), which misses real-fleet noise, missing data and variable operating conditions. No existing hybrid model computes explicit low-cycle fatigue (LCF) damage from operating cycles.

## Data & modalities
Multivariate sensor time series only:
- **Operating settings:** altitude, Mach number, power lever angle.
- **Sensor readings:** temperatures, pressures, N1/N2 rotor speeds, fuel flow, vibration.
- **Derived quantities:** efficiency estimates.

Two datasets are used:
1. A proprietary 12-year fleet dataset of 53 F100-PW-229 engines.
2. The NASA C-MAPSS benchmark (FD001-FD004).

The target on the real-fleet data is a Health Condition Indicator normalised to [0, 1].

## Method
- **Fatigue-cycle analytics module.** From thrust and throttle variations it computes:
  - cumulative strain energy density;
  - LCF cycle counts, using N1 speed reversals as the cycle counter and throttle-induced stress range (Δσ);
  - high-pressure turbine (HPT) efficiency.
- **Hybrid network:**
  - TCN for local transients;
  - two-layer bidirectional LSTM for long-term dependencies;
  - multi-head self-attention (MHSA) to weight fatigue-sensitive channels dynamically.
- **Fusion:** the physics features are fused with the raw sensor features.
- **Validation and regularisation:** cross-validation across engines on the fleet data and the official C-MAPSS test split, with early stopping and regularisation.
- No LLM or vision component.

## Results
**Real-fleet data:**
- Physics-aware model: RMSE 0.3336, Score 0.0184.
- Non-physics baseline: RMSE 0.7153, Score 0.0454. Adding the physics features cut RMSE by about 53% and Score by about 59%.
- Physics-only variant: RMSE 0.4821. Fusing sensor and physics features works best.
- R²: about -0.42 for the physics-aware model and -134.2 for the baseline. The author attributes the negative values to the small variance of the normalised target and to non-linear degradation.
- MAE: 0.188.

**C-MAPSS:**
- RMSE 9.47 (physics-only variant: 11.507); R² about 0.5; MAE about 38.

**Against the literature:** RMSE reductions of 29-48% (abstract) or 24-54% (Table 4) against published hybrids such as AttnPINN (17.21). The author notes these comparisons are approximate rather than exact head-to-head evaluations.

## Limitations
- The real-fleet dataset is proprietary.
- The literature comparisons are approximate.
- R² on real data is negative.
- Material parameters are not calibrated per component.
- The model assumes monotonic degradation and that LCF is the dominant damage mechanism.
- Online deployment is left to future work.
- There is no interpretability layer beyond the physics features.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** build physics-informed features from the TruLaser machine database before modelling. Examples:
  - cumulative nozzle or lens usage (pierce counts, cut hours);
  - laser-on hours;
  - thermal cycles;
  - cumulative energy per cut length.

  These become "damage counters" that act as regularisers, as LCF cycles do here.
- **Fusion:** pass physics-derived health indicators to the LLM next to the raw parameters, so its reasoning rests on interpretable quantities.
- **Evaluation:** run ablations (raw only vs physics only vs fused) and use an asymmetric score that penalises late warnings. Be careful with R² on small-variance normalised targets.
- **Data ingestion:** filter noise and missing data in real machine logs before modelling. The paper shows that real data behaves differently from simulated data.
