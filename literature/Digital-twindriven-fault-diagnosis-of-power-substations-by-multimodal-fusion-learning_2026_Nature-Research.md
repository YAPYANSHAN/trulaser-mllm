# Digital twin-driven fault diagnosis of power substations by multi-modal fusion learning

- **Citation (IEEE):** Y. Wu, Y. Chen, T. Xiao, et al., "Digital twin-driven fault diagnosis of power substations by multi-modal fusion learning," *Nat. Commun.*, vol. 17, art. 6628, 2026, doi: 10.1038/s41467-026-73483-5.
- **Domain:** Industrial / power-system fault diagnosis, multimodal fusion, digital twins
- **Relevance to FYP (1-5):** 4 — industrial multimodal fault diagnosis fusing heterogeneous logs, alarms, waveforms and SCADA tables, with a deployed system. No LLM and not laser cutting, but the fusion, robustness and synthetic-data ideas transfer directly.

## Problem
Substation faults generate large amounts of heterogeneous data (alarms, fault waveforms, SCADA). Rule-based methods (Petri nets, expert systems) are brittle under relay/breaker malfunctions and missing data. Data-driven methods rarely fuse modalities, generalise poorly across topologies, and lack fault samples.

## Data & modalities
A real 110 kV substation modelled in the CloudPSS digital-twin platform: 11,597 training and 3,890 test fault scenarios (single-point faults). Modalities: system topology (graph), alarm messages, fault waveform recordings and SCADA measurements. Augmentation emulates noise, sampling loss, sensor failure and up to 30% data loss. Data and code are on Code Ocean.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Graph-structured inputs follow the primary topology. Three modality-specific multi-layer **GAT** branches encode alarms, waveforms and SCADA. They are concatenated into a fused latent matrix, then passed through **self-attention** fusion.
- **Denoising autoencoder (DAE)** pre-training with a GAT encoder/decoder (MSE reconstruction) on corrupted samples. The encoder is then frozen.
- **Supervised contrastive learning (SCL)** trains the self-attention layers. Classification heads (cross-entropy) handle fault location, fault type and protection-failure detection.
- No LLM, RAG or KG.
- Deployed as a digital-twin system over IEC 61850 communication.

## Results (key numbers and metrics)
- Over 95% accuracy in fault location and 97% in fault-type identification, plus 90% in protection-failure detection under 30% data loss.
- Outperforms 7 baselines (rule-based TCFPN, MPNN, and MLP/ResNet/LSTM/GCN/Transformer variants) on 10 degraded test sets, with 5 seeds reported as mean ± SD.
- End-to-end latency ~1 min for data communication. Inference 0.5 s on an RTX 3090.

## Limitations
Trained on simulated scenarios. Single-point faults only. Moderate extra compute vs. baselines. Moving to a new substation requires rebuilding the simulation model and retraining. No visual modality yet (future: inspection-robot images).

## Transferable ideas for the FYP pipeline
- **Fusion:** one encoder per modality (machine table, alarm/error log, sensor time-series, image), then attention fusion. This is a non-LLM baseline to compare against the MLLM pipeline.
- **Data ingestion/robustness:** train on deliberately corrupted inputs (missing columns, noisy sensors) and report accuracy vs. % data loss. TruLaser databases will have gaps.
- **Synthetic data:** use simulation or a digital twin to generate rare fault scenarios and balance the classes. For laser cutting, this could be parameter sweeps or a physics model of dross/kerf.
- **Structured outputs:** split diagnosis into sub-tasks (fault location/component, fault type, protection/system failure). This maps to component, defect type and root cause in the FYP.
- **Evaluation:** test robustness under graded degradation, use multiple seeds, and report latency for deployment feasibility.
