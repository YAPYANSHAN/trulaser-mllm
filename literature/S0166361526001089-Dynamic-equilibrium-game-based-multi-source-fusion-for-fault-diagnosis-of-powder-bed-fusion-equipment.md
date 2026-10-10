# Dynamic equilibrium game based multi-source fusion for fault diagnosis of powder bed fusion equipment

- **Citation (IEEE):** L. Wang, W. Liu, J. Shi, et al., "Dynamic equilibrium game based multi-source fusion for fault diagnosis of powder bed fusion equipment," *Computers in Industry*, vol. 181, Art. no. 104541, 2026, doi: 10.1016/j.compind.2026.104541.
- **Domain:** Additive manufacturing (laser powder bed fusion) equipment fault diagnosis; multi-sensor time-series fusion.
- **Relevance to FYP (1-5):** 4 - Laser-based metal processing machine with gas/atmosphere subsystems (analogous to TruLaser assist-gas and extraction systems); fault diagnosis from heterogeneous machine sensor tables, though no LLM, images or documentation.

## Problem
PBF machines produce high-dimensional, correlated, redundant multi-sensor time series. Existing fusion methods (D-S evidence, weighted averaging, mRMRMI, EFS, MsTsDS, time-window AA, CNN fusion nets) optimise accuracy or redundancy but do not explicitly trade off fusion cost against information gain under stage-wise, time-varying operation.

## Data & modalities
Tabular/time-series sensor data only, from the sealed-chamber and recirculation-filtration systems during the gas-washing process: 11 variables (3 airflow, 2 oxygen concentration, 1 chamber pressure, 3 air velocity, 2 chamber-door states), sampled every 500 ms; 17,263 samples (12,163 train / 5,100 test). Four fault classes: splash, pores, sealed-chamber air leak, gas-pipeline air leak. Signal signatures documented (e.g., splash: intake air velocity rises from 2.07 to 2.61 m/s).

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
DGAM (dynamic equilibrium game mechanism): each feature subspace/source is a player in an allocation game; a composite payoff combines information gain (IG) and fusion cost (FC) weighted by eta, plus a coordination term delta. Recursive weight updating with numerical stopping; a Subgame Perfect Nash Equilibrium-inspired strategy treats each gas-washing stage as a subgame, with threshold-triggered stage transitions warm-starting the next stage's allocation. DGAM is a plug-in over fusion backbones (mRMRMI, EFS, MSFFNet, CMFCNN, MsTsDS, AFCNet, AA, WLRCNN - wavelet local response CNN). No LLM, RAG or KG.

## Results (key numbers and metrics)
- DGAM + WLRCNN best overall: fusion cost 0.35 to 0.27, MSE 0.052 to 0.041, RMSE 0.216 to 0.193, information gain 0.044 to 0.043.
- Test-set classification: accuracy 98.86% to 99.58%, macro-F1 98.57% to 99.39%.
- Runtime 0.54 s to 0.58 s (~7.4% overhead), deemed acceptable for online diagnosis.
- DGAM consistently improved cost-performance across all eight backbones; ablations, eta/delta sensitivity, and perturbation robustness tests reported; t-SNE shows tighter fault clusters.

## Limitations
Single machine and single process stage dataset; only four fault types; not robust-tested for missing sensors (stated future work); limited physical priors / interpretability; data available on request only.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** TruLaser assist-gas pressure, flow and nozzle/extraction signals can be organised per process stage (pierce, cut, bevel) like gas-washing stages, with stage-wise feature selection.
- **Fusion:** Cost-aware source selection - choose which machine-database columns/sensors to feed the LLM context to limit token cost while keeping information gain.
- **Data ingestion:** Synchronous resampling of all channels to a common interval before fusion.
- **LLM reasoning:** The paper's documented fault-to-signal signatures (e.g., leak to oxygen rise) are the kind of rules to encode in a knowledge base/RAG so the LLM can cite signal evidence.
- **Evaluation:** Report macro-F1 per fault class plus runtime overhead for online feasibility; a WLRCNN-style classifier could serve as a non-LLM baseline.
