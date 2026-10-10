# Surrogate assisted artificial neural network and NSGA II framework for continuous multi-objective optimization of sheet metal blanking

- **Citation (IEEE):** S. Bhoir and M. Verma, "Surrogate assisted artificial neural network and NSGA II framework for continuous multi-objective optimization of sheet metal blanking," *Discover Mechanical Engineering*, vol. 5, Art. no. 171, 2026, doi: 10.1007/s44245-026-00352-2.
- **Domain:** Manufacturing process optimisation / sheet-metal forming (blanking)
- **Relevance to FYP (1-5):** 4 - sheet-metal process optimisation that predicts burr (edge quality) from process parameters and material. This is a direct template for the process-optimisation module, though it involves no LLM and is not laser cutting.

## Problem
Blanking parameters are usually optimised with DOE, Taguchi or response-surface methods. These evaluate only discrete level combinations, so better operating points between levels are missed. Burr height, force and energy also trade off against each other.

## Data & modalities
Tabular experimental data: 100 observations from Taguchi L25 orthogonal arrays on four materials (SS316, C110 copper, AA1100 aluminium, C26000 brass). Inputs are sheet thickness, punch-die clearance and one-hot material type. Output is measured burr height. Blanking force, shearing energy and specific work come from analytical formulas.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- A unified ANN surrogate for burr height. The architecture search covered 420 networks and chose 6-12-1.
- Robustness checks: repeated 5-fold CV (50 runs, about 1,000 predictions), sensitivity analysis, residual diagnostics, and comparison with six alternative surrogates (including Gaussian process regression).
- The ANN is coupled with **NSGA-II** for four-objective optimisation (burr, force, shearing energy, specific work) over the *continuous* design space.
- The knee-point solution is chosen by normalised Euclidean distance to the utopia point.
- 12 Pareto solutions were validated experimentally.
- No LLM is used.

## Results (key numbers and metrics)
- Selected ANN: MSE 6.71×10⁻⁶, RMSE 0.00259 mm, R² 0.995. Repeated CV average R² 0.850 ± 0.145.
- Squared-exponential GPR scored marginally higher in validation.
- 140 continuous Pareto-optimal solutions found beyond the DOE grid.
- Experimental validation of 12 solutions: MAE 0.0023 mm, MAPE 3.31%, per-point errors 2.47-4.39%.

## Limitations
- Only four materials and two process variables, with material encoded as one-hot rather than by its properties.
- Force, energy and specific work are strongly correlated, so the objectives conflict less.
- Tool wear, punch velocity, lubrication, thermal effects and machine dynamics are ignored.
- Valid only inside the tested ranges; other settings need retraining.
- The small dataset (100 points) explains the CV variance.

## Transferable ideas for the FYP pipeline
- **Process optimisation (tabular):** train a surrogate (ANN or GPR) mapping laser parameters (power, speed, focus position, gas type and pressure, nozzle, bevel angle, material and thickness) from TRUMPF tables to quality outcomes (burr or dross height, roughness, kerf). Run NSGA-II over it to propose Pareto-optimal settings with a knee-point recommendation.
- **LLM reasoning:** the LLM can call this optimiser as a tool and explain its trade-offs, e.g. "reducing speed by X lowers dross but increases cycle time". This grounds recommendations in a validated numerical model instead of LLM guesses.
- **Tabular:** encode material by properties (thickness, tensile strength, conductivity) rather than one-hot, so the model generalises to new materials.
- **Evaluation:** validate surrogate-recommended settings with a few physical test cuts and report MAE/MAPE. Use repeated k-fold CV for small datasets.
