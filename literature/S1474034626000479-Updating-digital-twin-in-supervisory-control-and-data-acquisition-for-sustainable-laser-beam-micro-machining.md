# Updating digital twin in supervisory control and data acquisition for sustainable laser beam micro machining

- **Citation (IEEE):** K. Venkata Rao and K. Venkata Vaneesha, "Updating digital twin in supervisory control and data acquisition for sustainable laser beam micro machining," *Advanced Engineering Informatics*, vol. 71, Art. no. 104355, 2026, doi: 10.1016/j.aei.2026.104355.
- **Domain:** Laser cutting process optimisation / digital twin and SCADA (manufacturing)
- **Relevance to FYP (1-5):** 5 - directly about laser cutting of stainless sheet on a TRUMPF machine, with process-parameter optimisation for surface roughness and energy. There is no LLM, but it supplies the domain physics, parameters and the closed-loop optimisation baseline.

## Problem
Laser beam machining (LBM) must reduce both surface roughness (Ra) and specific machining energy (SME) for sustainability. Static offline optimisation (e.g., Taguchi) does not adapt to the dynamic behaviour of the process.

## Data & modalities
- **Machine and material:** a TRUMPF TruCoax 2500 CO2 laser (max 2500 W) cutting AISI 316L stainless sheets of 4, 6 and 8 mm.
- **Process parameters:** laser power (LP 1.5-2.5 kW), laser frequency (LF 6/8/10 kHz) and cutting speed (CS, varied by thickness), set by a Taguchi L9 design.
- **Sensing:** a PCB 356A22 accelerometer on the sheet (4 MHz sampling, 100-1000 kHz band-pass), giving 81 vibration samples in total, plus measured roughness and cutting time.
- Modalities: tabular process parameters plus vibration time series.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Analysis:** ANOVA on the significance of the parameters, with mathematical models estimating Ra and SME from the experimental data.
- **Digital twin (DT):** combines those mathematical models with an MLP (4-64-32-5). Inputs are thickness, LP and other rate parameters; outputs are vibration amplitude and frequency in X/Y plus SME. Trained with Adam (65 training, 16 test samples), L2 regularisation, grid-searched hyperparameters and 200 epochs.
- **SCADA loop:** monitoring stages every 10 min. When the estimated Ra or SME deviates more than 10% from its target, the ANN is retrained with new real-time vibration data and re-optimises LP, LF and CS, which are written back to the machine.
- **Comparison:** against Taguchi optimisation.

## Results (key numbers and metrics)
- **ANN fit:** R² of 0.9942 (Ra) and 0.9953 (SME); validation MSE 0.0296.
- **Optimised settings:** 2.15 kW, 6.3 kHz and 0.56 m/min, with target Ra 7.8 µm and SME 3.41 J/mm³.
- **Closed loop in action:** in stage 2 the errors reached 15.6% (Ra) and 12.4% (SME), triggering retraining and new settings of 2.3 kW, 6.2 kHz and 0.51 m/min. Measured Ra values of 7.71 and 7.34 µm closely matched the estimates.
- Control latency is a few seconds.
- **SCADA vs. Taguchi:**

  | Sheet | SCADA Ra reduction | SCADA SME reduction | Taguchi Ra reduction | Taguchi SME change |
  |---|---|---|---|---|
  | 4 mm | 47.44% | 34.92% | 33.86% | +12.98% |
  | 6 mm | 54.67% | 22.61% | 39.23% | −6.67% |
  | 8 mm | 36.99% | 83.66% | 16.26% | −81.49% |

- Higher cutting speed increases Y-direction sheet vibration and roughness but lowers SME.

## Limitations
- Very small dataset (81 samples; 16 test samples).
- One material on a CO2 laser, not a fibre/bevel machine.
- Only vibration sensing; no imaging of the cut.
- Roughness is still estimated by the models between measurements.
- No defect taxonomy (dross, burr).

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** use LP, frequency and CS (plus gas and focus on the TruLaser 3000) and thickness as core features. Ra and SME are useful target KPIs for "process optimisation insights".
- **LLM reasoning:** the ANOVA findings (LP and CS significant for Ra; LP×CS interactions significant for SME) can seed rule knowledge in the RAG knowledge base, letting the LLM explain parameter recommendations.
- **Fusion/deployment:** the closed-loop pattern is worth reusing. Estimate quality → compare with target (±10%) → retrain the surrogate → recommend new parameters. An LLM could wrap this loop to explain each adjustment to operators.
- **Evaluation:** benchmark LLM-proposed parameter changes against a Taguchi or surrogate-model optimiser.
