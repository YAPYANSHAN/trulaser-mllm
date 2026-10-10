# Hierarchical vision-driven automatic control of quality and speed in fusion laser cutting

- **Citation (IEEE):** S. Guerra, L. Caprio, M. Pacher, et al., "Hierarchical vision-driven automatic control of quality and speed in fusion laser cutting," *Optics & Laser Technology*, vol. 200, art. 114980, 2026, doi: 10.1016/j.optlastec.2026.114980.
- **Domain:** Laser cutting process monitoring and closed-loop control (coaxial vision + ML)
- **Relevance to FYP (1-5):** 5 — this is the same process family as the FYP (fibre-laser fusion cutting of stainless sheet with N2). It links melt-pool image features to dross and fault states (plasma, loss of cut) and to speed optimisation. It provides domain ground truth for fault classes and parameter–quality relations, although it uses no LLM.

## Problem
Industrial laser cutters use fixed, conservative parameters per material and thickness. This limits productivity and does not react to process variability. The goal is real-time quality assurance and productivity optimisation, handling several defects at once:
- dross attachment
- plasma-dominated cutting
- loss of cut
- grid-related disturbances

## Data & modalities
- **Setup:** 6 kW IPG fibre laser cutting 5 mm AISI 304 stainless steel with nitrogen assist gas. Baseline settings: maximum power, focus −5.7 mm, 18 bar, stand-off 0.7 mm. Cutting speed is varied (about 5500–8250 mm/min).
- **Sensing:** a coaxial NIR CMOS camera (1280×1024) acquires at 750 Hz.
- **Melt-pool features:** geometric and intensity features (width, area, length, perimeter, centroid, plasma index), taken as mean and standard deviation over a 100 ms window.
- **Dross ground truth:** measured on the cut edge, binarised, converted to the time domain and expressed as a 0–1 dross-occurrence indicator.
- **Dataset size:** 18,900 datapoints. Replicas 1–2 are used for training and replica 3 for testing.

## Method
**Feature selection:** Pearson relevance (threshold 0.5) followed by redundancy filtering (pairwise correlation above 0.6 removed).

**Models:** lightweight models are chosen so inference keeps up with 750 fps; the authors note CNNs would be too slow.
- A linear regressor estimates dross.
- A classification tree identifies the process state. Its nodes are threshold classifiers for loss of cut (Width255_mean) and plasma (Plasma_Index), plus a linear SVM for grid disturbance.

**Control:** a hierarchical double loop.
- The inner discrete PI loop adjusts cutting speed to track a target dross level.
- The outer supervisory loop detects and suppresses plasma and loss-of-cut states, including under grid disturbances.

## Results
- Dross regressor: R² of about 90%, with MAE and RMSE below 0.1 mm. The acceptance thresholds were R² 85%, SMAPE 50% and 0.1 mm error.
- State classifier: accuracy, precision, recall and F1 all above 85% (the abstract says above 90%).
- In real-time tests from different initial conditions, the system recovered optimal states and minimised dross.
- On a complex-geometry case study it gave about 18–20% productivity gain.

## Limitations
- The ML models are specific to one material and thickness. New materials need new data collection and retraining, although the architecture itself transfers.
- Only speed is regulated.
- Only fusion cutting of 5 mm AISI 304 was tested. Bevel cutting was not covered.

## Transferable ideas for the FYP pipeline
- **Fault taxonomy:** adopt dross, plasma cutting, loss of cut and grid (slat) disturbance as labelled fault classes. Use the documented parameter levers (speed, focus, pressure, stand-off) as the action space for optimisation advice.
- **Tabular/time-series:** compute windowed statistics of sensor features (mean and std over 100 ms) and apply relevance/redundancy feature selection before giving evidence to the LLM.
- **LLM reasoning:** let the LLM explain the outputs of fast classical estimators (dross estimate, state class) rather than run in the real-time loop. The paper shows real-time control needs lightweight models.
- **Evaluation:** use industrially meaningful acceptance thresholds (for example 0.1 mm dross tolerance) and test across replicas and initial conditions.
