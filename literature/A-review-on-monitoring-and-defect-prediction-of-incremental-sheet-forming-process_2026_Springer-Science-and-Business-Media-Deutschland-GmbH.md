# A review on monitoring and defect prediction of incremental sheet forming process

- **Citation (IEEE):** J. Song, L. Wang, F. Han, et al., "A review on monitoring and defect prediction of incremental sheet forming process," *The International Journal of Advanced Manufacturing Technology*, vol. 145, pp. 7525-7544, 2026, doi: 10.1007/s00170-026-18716-z.
- **Domain:** Sheet-metal manufacturing / process monitoring and defect prediction (review)
- **Relevance to FYP (1-5):** 4 - sheet-metal process defect mechanisms, multi-sensor monitoring, hybrid physics-ML prediction and a monitoring-prediction-control framework map closely onto laser-cut quality diagnosis and optimisation (no LLM content).

## Problem
Incremental sheet forming (ISF), a die-less process using a ball-end tool along a toolpath, accumulates small deviations into geometric errors, surface defects or fracture. Empirical design cannot predict complex failures and post-process inspection cannot prevent losses, so real-time monitoring and defect prediction are needed.

## Data & modalities
Review of: process parameters (step size, tool diameter, feed, spindle speed, sheet thickness, material), force sensors, temperature fields (thermography), strain fields (stereo-vision DIC), surface morphology/optical measurements, simulation (FE) data.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Defect taxonomy and mechanisms: geometric (springback/contour deviation, twist, wrinkling, pillow effect), surface defects, fracture failure.
- Monitoring technologies for force, temperature and strain.
- Prediction models: physics-based (analytical, FE), machine learning/neural networks (e.g., CNN forming prediction framework CNN-FP), hybrid physics-informed models (PIDD, TG-DNN), and transfer learning (including a GNN-based transfer framework) for cross-material/geometry generalisation under limited data.
- Proposes an integrated monitoring-prediction-control intelligent ISF system framework.

## Results (key numbers and metrics)
Review findings: hybrid modelling + transfer learning best balance physical interpretability and data-driven generalisation; one cited neural-network prediction/compensation study reduced average geometric error by 68.5%. No new experiments.

## Limitations
Monitoring mostly single-parameter, missing coupled effects; process-parameter/defect relationships not quantitatively mapped for multi-parameter coupling; simulations miss local loading-path dependence; ISF-specific (not cutting).

## Transferable ideas for the FYP pipeline
- **Data ingestion / KG:** adopt the defect taxonomy pattern (defect type -> features -> formation mechanism -> influencing parameters) for laser-cut defects (dross, burr, striations, kerf/bevel deviation, incomplete cut) as the backbone of the knowledge base the LLM reasons over.
- **Tabular/time-series:** build a process-parameter-to-defect mapping model (power, speed, gas pressure, focus, nozzle, thickness) with physics-informed features; use transfer learning across materials/thicknesses where data is scarce.
- **LLM reasoning:** have the LLM explain predictions using the mechanism tables (interpretability), and propose parameter adjustments as in the monitoring-prediction-control loop.
- **Deployment:** frame the FYP as monitoring -> prediction -> recommended control action, with a digital-twin-style closed loop comparing predicted vs observed quality.
