# Implement the Concept of Artificial Neural Networks in Studying the Sheared Edge Defects at the Sheet Metal Blanking Processes

- **Citation (IEEE):** H. A. Salman, M. Al-Wswasi, W. A. Al-Khaleeli, et al., "Implement the concept of artificial neural networks in studying the sheared edge defects at the sheet metal blanking processes," *Journal Européen des Systèmes Automatisés*, vol. 59, no. 7, pp. 2057-2071, 2026, doi: 10.18280/jesa.590721.
- **Domain:** Manufacturing / sheet metal blanking - process-parameter vs edge-defect modelling
- **Relevance to FYP (1-5):** 4 - sheet-metal cut-edge quality as a function of process parameters, with an ANN surrogate; same "parameters -> edge defects -> optimal settings" logic as laser-cut quality optimisation, though no LLM or images.

## Problem
Blanked parts suffer edge defects (doming, edge taper inclination degree (ETID), dishing). The study quantifies how cutting speed, punch-die clearance and material affect these defects and builds a predictive model to recommend optimal parameters.

## Data & modalities
Experimental, tabular. Circular blanks (30 mm diameter, 2 mm thick) of medium-carbon steel (AISI 1048) and brass; three clearance-to-thickness ratios (3.75%, 4.25%, 5.00%) via different punch diameters; several cutting speeds. Defects measured on sectioned, polished specimens with a PT300 profile projector (x10), three samples per condition averaged. Dataset: 24 trials per output.

## Method
Experimental parametric study followed by three separate MATLAB feed-forward ANNs (one per defect) with architecture 3-10-1 (inputs: material type, cutting speed, C/T), tansig activation, Levenberg-Marquardt training, learning rate 0.01, up to 2000 epochs, 70/15/15 train/validation/test split. 15 vs 10 hidden neurons compared; 10 chosen for simplicity.

## Results
Material is the dominant factor (brass shows higher doming, ETID and dishing than steel). Defect-clearance relation is non-linear; best edge quality at C/T 4.25%. Higher cutting speed reduces defects. Best condition: medium-carbon steel, C/T 4.25%, 480 mm/s. ANN correlation R > 0.99 for training/validation/testing in all three models. Testing metrics: doming MAE 0.008837, RMSE 0.014168, R² 0.9847; ETID MAE 0.048046, RMSE 0.062372, R² 0.9816.

## Limitations
Very small dataset (24 samples) - the ANN is a process-specific interpolator valid only within the tested range; no reported standard deviations/uncertainty; only two materials and one thickness; mechanical blanking, not thermal cutting; very low validation MSEs suggest a risk of overfitting.

## Transferable ideas for the FYP pipeline
- **Tabular:** build a small surrogate model (ANN or gradient boosting) mapping TruLaser parameters (power, feed rate, gas pressure, focus position, nozzle standoff, material/thickness, bevel angle) to measured edge-quality indices (burr height, roughness, dross, kerf taper, bevel-angle error).
- **Process optimisation:** use the surrogate to search for optimal parameter windows; the LLM then explains the recommendation with the surrogate's sensitivities as evidence.
- **Domain knowledge/RAG:** the paper's physical explanations (strain rate, clearance-crack interaction, material ductility) are an example of mechanism text that can be indexed as background knowledge.
- **Evaluation:** report MAE/RMSE/R² on held-out conditions and explicitly state the valid parameter envelope to prevent the LLM from extrapolating.
