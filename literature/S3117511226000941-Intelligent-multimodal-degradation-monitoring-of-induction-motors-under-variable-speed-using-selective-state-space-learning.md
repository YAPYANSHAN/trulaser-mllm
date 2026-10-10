# Intelligent multimodal degradation monitoring of induction motors under variable speed using selective state space learning

- **Citation (IEEE):** N. Lakshmaiya, "Intelligent multimodal degradation monitoring of induction motors under variable speed using selective state space learning," *e-Prime - Nexus of Electrical, Electronic, and Intelligent Engineering*, vol. 18, Art. no. 201243, 2026, doi: 10.1016/j.eprime.2026.201243.
- **Domain:** Industrial fault diagnosis / condition monitoring (rotating machinery, multi-sensor time series)
- **Relevance to FYP (1-5):** 3 - industrial multimodal sensor fusion for fault diagnosis under changing operating regimes. It uses no LLM or images, but its time-series and fusion methods transfer.

## Problem
Induction-motor degradation is hard to assess when speed varies, because the signals are non-stationary. Handcrafted features and CNN/RNN/Transformer models either assume stationarity, fail to capture long-range temporal dependencies, or cost too much to run in real time. Few methods explicitly model the cross-domain electrical-mechanical interaction.

## Data & modalities
Public Mendeley dataset "Vibration and Motor Current Dataset of Rolling Element Bearings under Varying Speed Conditions." It has synchronised motor current, vibration and rotational speed. Classes are healthy plus inner-race, outer-race and rolling-element faults, each at three severity levels. Frames are 2048 samples with 50% overlap. Band-pass filtering is 10-5000 Hz for vibration and 10-2000 Hz for current. Splits are run-block based (70/15/15), so windows from the same run never appear in both train and test.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Speed-adaptive preprocessing:** resampling/interpolation normalises the signals to speed.
- **Multimodal signal fusion:** current, vibration and speed features are fused, including cross-domain correlation features.
- **Selective state-space temporal model (Mamba):** speed-conditioned temporal gating, linear complexity and streaming (causal) inference. The latent state is read as a progression of health state, and a smoothed health indicator is checked for monotonicity.
- Implemented in PyTorch. No LLM is used.

## Results (key numbers and metrics)
- Accuracy 98.8%, with high precision, recall, F1 and AUC and a low false-alarm rate.
- Literature comparison: MLP 97.96, 1D dilated CNN 97.4, CNN-LSTM 97.8, TCN+Attention 97.6, proposed 98.8.
- Latent dimension 64/128/256 gives 97.3/98.8/98.7.
- Removing current-magnitude features lowers F1 by 2.1%, and removing vibration-envelope features lowers it by 1.8%.
- Health-indicator monotonicity is 0.87-0.94 depending on the smoothing factor.
- The ablation shows that every module (speed adaptation, fusion, Mamba) contributes.

## Limitations
- Single laboratory bearing dataset.
- The gain over baselines is about 1 point.
- Not validated on run-to-failure data or for RUL.
- Large-scale industrial validation is left to future work.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** condition features on operating regime, as this paper conditions on speed. For the laser this means power, feed rate, gas pressure, material and thickness, so that fault signatures are not confused with recipe changes.
- **Evaluation:** split by run or job (no leakage between windows from the same job). This applies directly to the TRUMPF machine logs.
- **Tabular/time-series:** a lightweight Mamba/SSM or TCN encoder can compress long sensor or log sequences into embeddings or a health index. The LLM then receives that index as evidence instead of raw streams.
- **Fusion:** cross-modal correlation features (e.g., current vs. vibration) carry the most information. The laser analogue is correlating laser power, cutting speed and gas pressure against defect occurrence.
