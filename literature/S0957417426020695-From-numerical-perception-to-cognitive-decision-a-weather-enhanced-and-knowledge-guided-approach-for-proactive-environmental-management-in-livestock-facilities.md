# From numerical perception to cognitive decision: a weather-enhanced and knowledge-guided approach for proactive environmental management in livestock facilities

- **Citation (IEEE):** M. Wang, C. Zhang, X. You, et al., "From numerical perception to cognitive decision: a weather-enhanced and knowledge-guided approach for proactive environmental management in livestock facilities," *Expert Systems With Applications*, vol. 331, Art. no. 133160, 2026, doi: 10.1016/j.eswa.2026.133160.
- **Domain:** Cyber-physical systems / precision livestock farming — time-series forecasting + knowledge-guided LLM decision support
- **Relevance to FYP (1-5):** 4 — different application, but a complete "sensor time series → LLM-based forecasting → knowledge-base-constrained LLM report with risk attribution and graded interventions" pipeline, very close to the FYP's tabular-to-insight stage.

## Problem
Closed sheep barns trade off heat preservation against ventilation. Data-driven models ignore external weather ("physical-environmental decoupling") and give black-box numbers that cannot support interpretable welfare decisions ("data-decision gap").

## Data & modalities
Indoor sensors in a large meat-sheep facility sampled every 1 min (NH3, CO2, PM2.5, PM10, temperature, humidity, etc.), plus external meteorology from ECMWF ERA5 reanalysis (2 m temperature, wind components, surface pressure) on a 3 × 3 virtual grid, aligned hourly-to-minute. Domain knowledge base: physiological thresholds, causal logic, synergistic risk rules.

## Method (Hd-LLM)
- **Perception:** physics-guided hybrid forecaster with a Micro-scale Meteorological Grid Feature Extractor (3 × 3) for wind/thermal pressure gradients; FiLM conditioning of internal pollutant dynamics on external weather.
- **Frequency-Aware Adapter (FA-Adapter)** inserted into a frozen pre-trained GPT-2 backbone for parameter-efficient fine-tuning, separating low-frequency physical trends from high-frequency biological rhythms.
- **Decision:** Knowledge-Guided Reasoning Module using DeepSeek-V2.5 API constrained by the knowledge base (neuro-symbolic): converts predicted trajectories (with key-point sampling) into structured reports with risk attribution, comfort grading and graded ventilation interventions.
- Baselines include Informer and TimeLLM.

## Results
- Ammonia MAE reduced by up to 56.4% vs strong baselines (abstract); NH3 MAE 0.71, RMSE 1.33, MAE 58.7% lower than Informer (conclusion).
- Identifies composite risks (e.g., high humidity + high ammonia); threshold-sensitivity tests show bounded, rule-governed escalation (e.g., NH3 9.8 → 10.2 ppm triggers Level 1 → Level 2 warning).

## Limitations
Single cold-region site and single livestock scenario; frozen GPT-2 still costly for ultra-light devices (edge server / industrial PC needed); ERA5 is retrospective reanalysis rather than real-time forecast input.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** use an LLM-backbone forecaster with adapters (or simpler models) on TruLaser machine logs to predict drifts (e.g., nozzle wear, focus drift, gas consumption) before defects occur.
- **Conditioning:** FiLM-style conditioning of process signals on job context (material, thickness, bevel angle) mirrors conditioning on external weather.
- **LLM reasoning:** constrain the LLM with an explicit rule/knowledge base from TRUMPF documentation (thresholds, cause-effect rules, combined-risk rules) so outputs are graded warnings + interventions with risk attribution, suppressing hallucination.
- **Evaluation:** threshold-sensitivity tests to show recommendations change only when rule boundaries are crossed.
- **Deployment:** target an industrial-PC/edge server next to the machine.
