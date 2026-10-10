# Information Content Analysis of Direct and Indirect Force Measurements for Machine Learning-Based Process State Classification in Multi-stage Sheet Metal Forming

- **Citation (IEEE):** M. Schumann, J. Moske, F. Divo, et al., "Information content analysis of direct and indirect force measurements for machine learning-based process state classification in multi-stage sheet metal forming," *Transactions of the Indian Institute of Metals*, vol. 79, art. 140, 2026, doi: 10.1007/s12666-026-03839-4.
- **Domain:** Sheet metal forming - sensor-based process monitoring with explainable ML
- **Relevance to FYP (1-5):** 3 - sheet-metal process-state classification from machine sensor time series with XAI attribution; relevant to the tabular/time-series branch, but no LLM or images and forming rather than laser cutting.

## Problem
Which force-sensing concept (direct vs indirect) and which process phase carry the most information for detecting subtle die-roughness changes in a progressive deep-drawing + ironing process, and does high signal-to-noise ratio (SNR) imply better ML performance?

## Data & modalities
Time-series force signals. Bruderer BSTA 410-110 press, 200 strokes/min, 0.5 mm DC04 sheet; progressive die with deep drawing (DD) and redrawing/ironing (IR) stages. Three indirect piezo strain sensors (Kistler 9240A) and three direct force rings (Kistler 9051C), sampled at 25 kHz (NI cRIO-9047). Full-factorial 3x3 design of die roughness (Rz approx. 1.5, 5.5, 10 µm) for DD and IR = nine configurations x 500 strokes; 66 tactile roughness measurements; zero-load reference run for baseline.

## Method
SNR computed per channel via baseline subtraction of the unloaded reference run (RMS residuals, dB). Stroke-segmented, normalised signals fed to a 1D CNN (four Conv1D-BatchNorm-ReLU-MaxPool-Dropout blocks, global average pooling, linear head); 70/10/20 split. Classification of DD and IR roughness states per sensor channel and channel groups, on full signals and selected time windows. Integrated Gradients used for attribution analysis.

## Results
Direct sensors have clearly higher SNR. Roughness propagates down the process chain (e.g., coarsest DD die roughness reduced by roughly 40% during runs) and downstream signals contain information about upstream states. Counter-intuitively, high-SNR direct signals sometimes gave weaker or misleading CNN predictions because the model attributed importance to the signal onset where small temporal misalignments (<1% onset differences) occurred; restricting to later signal phases raised F1. Noisier indirect signals with distributed dynamics produced more robust predictions.

## Limitations
Single press, material and process; roughness states artificially created; only 1D CNN examined; dataset from controlled lab experiments; no domain-shift testing beyond the factorial design.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series ingestion:** align machine signals (e.g., per-contour laser power, feed, gas pressure, piercing time) to process events before modelling; misalignment can create spurious "features".
- **Evaluation/XAI:** use Integrated Gradients (or SHAP) to check that the model attends to physically meaningful phases; feed attribution summaries to the LLM as evidence for its explanation.
- **Sensor/feature selection:** do not equate clean, human-readable signals with informative ones; test channel subsets with identical pipelines.
- **LLM reasoning:** encode cross-stage causality (upstream state influencing downstream quality), analogous to piercing quality affecting subsequent contour cutting.
