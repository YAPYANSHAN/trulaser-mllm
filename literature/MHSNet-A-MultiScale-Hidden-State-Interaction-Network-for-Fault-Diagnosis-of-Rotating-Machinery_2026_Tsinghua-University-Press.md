# MHSNet: A Multi-Scale Hidden State Interaction Network for Fault Diagnosis of Rotating Machinery

- **Citation (IEEE):** F. Zhang, Z. Li, Y. Cheng, et al., "MHSNet: A multi-scale hidden state interaction network for fault diagnosis of rotating machinery," *Tsinghua Science and Technology*, vol. 31, no. 6, pp. 2855-2876, Dec. 2026, doi: 10.26599/TST.2025.9010138.
- **Domain:** Multi-sensor time-series fault diagnosis for rotating machinery (bearings, gearboxes).
- **Relevance to FYP (1-5):** 3 - no LLM and not laser cutting, but its multi-sensor fusion and multi-task (fault type + operating condition) design transfers to the machine-log/sensor branch of the FYP.

## Problem
Bearing/gear fault diagnosis under heavy noise, data imbalance and heterogeneous sensors (vibration vs torque at different sampling rates). CNNs have limited receptive fields, Transformers are quadratic in sequence length, and early/late fusion ignores distribution differences between sensors and the differing importance of sensors per task.

## Data & modalities
1D time series only: vibration + torque.
- Paderborn University (PU) bearing set: real damage, 5 health states (healthy, outer ring levels 1-2, inner ring levels 1-2) x 3 operating conditions; 9000 samples; vibration 64 kHz (2048 points/sample), torque 4 kHz (128 points/sample).
- MCC5-THU gearbox set: 6 gear states (healthy, missing teeth, crack, wear, breakage, pitting) x 3 variable-speed ranges (500-1000, 1500-2000, 2500-3000 rpm); 4500 samples of 2048 points; 12.8 kHz.
- Gaussian noise at -1/-3/-5 dB SNR; imbalance splits such as 80/10/10.

## Method
- Mamba-based multi-scale (MMS) module: depthwise-separable multi-scale convolutions (local impulse features) + Mamba selective state-space blocks (long-range, periodic dependencies at linear cost).
- Dynamic state-space fusion (DSSF): two parallel Mamba blocks exchange hidden states between sensors, so sensors are aligned in the hidden space instead of concatenated.
- Multi-task heads: fault-type diagnosis (FTD) and operating-condition classification (OCC), with task-aware sensor weighting.
- Five-fold cross-validation; t-SNE visualisation; module, task and modality ablations. No LLM, RAG or images.

## Results
- PU, -5 dB: FTD accuracy 98.24% (described as almost unaffected by noise); OCC 90.89% vs M2FN 77.57%, MRCFN 85.32%, MICN 90.33%.
- MCC5-THU: FTD 95.96% / OCC 100% clean; -1 dB 79.64 / 99.84%; -3 dB 78.04 / 99.36%; -5 dB 74.40 / 98.67%, best among the 6 baselines (HCNN-1D, MTA, MT-ConvFormer, M2FN, MICN, MRCFN).
- Robust under imbalanced splits; ablations show vibration+torque beats either sensor alone, and removing the Mamba fusion (plain concatenation) degrades accuracy.

## Limitations
Laboratory test-rig data with synthetic Gaussian noise; class-label outputs only, with no explanation; the gearbox FTD accuracy drops sharply under noise (to about 74%); no compute or latency figures found in the text; future work is listed as deeper cross-modal interaction and other machine types.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** If the TruLaser database exposes time-stamped signals (laser power, gas pressure, feed rate, nozzle distance, bevel-head angle), encode each with a multi-scale conv + Mamba/SSM encoder rather than flat statistics.
- **Fusion:** Align heterogeneous sampling rates (e.g., 2048 vs 128 points) before fusion; hidden-state exchange is a better fusion strategy than simple concatenation.
- **Multi-task:** Predict fault class *and* operating regime (material/thickness/cut mode) jointly; the regime label can then condition the LLM's diagnosis prompt.
- **LLM reasoning:** Feed the classifier's fault label, confidence and dominant sensor as structured evidence to the LLM, which supplies the explanation this model lacks.
- **Evaluation:** Copy the protocol of noise-injection at several SNRs, imbalance splits and five-fold CV to test robustness of the FYP's sensor branch.
