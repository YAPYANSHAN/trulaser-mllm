# Multi-objective optimization of stamping process based on physics-guided extra trees for large thin-walled parts

- **Citation (IEEE):** X. Wen, T. Zhu, J. Wang, et al., "Multi-objective optimization of stamping process based on physics-guided extra trees for large thin-walled parts," *International Journal of Mechanics and Materials in Design*, vol. 22, art. 128, 2026, doi: 10.1007/s10999-026-09950-0.
- **Domain:** Sheet metal forming — surrogate modelling and process-parameter optimisation
- **Relevance to FYP (1-5):** 3 — sheet-metal process optimisation from small tabular datasets with physics-derived features; no LLM or imaging, but the optimisation stage maps directly onto laser-cut parameter tuning.

## Problem
Stamping of large thin-walled covers involves conflicting defects (cracking, wrinkling/thickening, springback/warpage). FEM is too expensive for full optimisation, and purely data-driven surrogates generalise poorly with few samples, especially near failure boundaries.

## Data & modalities
- Tabular simulation data only: 100 parameter combinations from Optimal Latin Hypercube Sampling, simulated in AutoForm R8 (DX53D_Z_100 galvanised steel, 55-inch TV backplane), plus 27 orthogonal-design simulations for analysis.
- Four inputs: friction coefficient μ ∈ [0.10, 0.25], blank-holder force BHF ∈ [250, 450] kN, die gap ∈ [0.50, 0.60] mm, fillet radius R ∈ [2.0, 4.0] mm. Outputs: thinning, thickening, springback.

## Method
- **Physics-guided feature pool** (13-D) of high-order coupling descriptors from plastic deformation and frictional instability mechanisms (e.g. μ·BHF, BHF/…), automatically expanded from the 4 raw parameters.
- Target-specific feature decoupling via **permutation importance**.
- **Yeo-Johnson** target transformation to handle skewed tails near forming limits.
- **Extra Trees** regressor (fully randomised splits) for robustness to collinearity (PG-ET).
- Surrogate coupled with **NSGA-II** multi-objective search and **TOPSIS** decision-making under a thinning constraint. No LLM/deep learning.

## Results
- Thinning: R² 0.8300, extreme absolute error 0.0024 mm; thickening R² 0.9662; springback R² 0.8637 (up from 0.8051, MAE −14.3% via feature decoupling).
- Optimum: μ = 0.184, BHF = 272.2 kN, gap = 0.567 mm, R = 2.82 mm.
- Industrial validation: macro-warpage −48.5%, maximum thickening −26.6%, no cracking.

## Limitations
Static process parameters only (no time-varying blank-holder trajectories); data from simulation with deterministic material properties; single part/material; online sensing and closed-loop control left to future work.

## Transferable ideas for the FYP pipeline
- **Tabular stage:** build physics-motivated derived features from TruLaser logs (e.g. line energy = power/feed rate, gas pressure × nozzle diameter, focus position relative to thickness, bevel angle effects) before feeding tree models — better small-sample generalisation than raw columns.
- **Process optimisation:** a tree-based surrogate (Extra Trees/XGBoost) trained on machine-DB rows can predict quality (dross, roughness, kerf) and be searched with NSGA-II + TOPSIS; the LLM can then explain the Pareto-optimal recommendation using permutation-importance evidence.
- **Data handling:** Yeo-Johnson transform for skewed defect metrics; Latin-hypercube DOE for planning cutting trials.
- **Evaluation:** report R²/MAE per quality target and validate recommended settings on physical parts.
