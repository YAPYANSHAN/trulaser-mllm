# Intelligent vineyard monitoring based on YOLOv8 with Gated-Swin and fine-tuned DeepSeek-VL2 vision–language model

- **Citation (IEEE):** D. Zhang, F. Xu, X. Gao, et al., "Intelligent vineyard monitoring based on YOLOv8 with Gated-Swin and fine-tuned DeepSeek-VL2 vision–language model," *Measurement*, vol. 292, Art. no. 123245, 2026, doi: 10.1016/j.measurement.2026.123245.
- **Domain:** Precision agriculture / AIoT visual defect (disease) detection with a VLM
- **Relevance to FYP (1-5):** 4 — different domain, but its sensor + image + detector + LoRA-tuned VLM producing schema-constrained reports is almost the same architecture the FYP needs for cut-part defect images.

## Problem
Vineyard disease monitoring needs to link environmental sensing, visible symptoms and actionable reports. The authors want accurate, repeatable lesion detection and structured (machine-parseable) VLM reporting within one modular system.

## Data & modalities
- Sensors: temperature, humidity, pH, NPK, illumination via a central gateway.
- Images: 5,000 image-label pairs, 18,205 boxes, three classes (Rotten holes 8,156; measles 4,605; wilt 5,444); hash-identical images grouped before a 3,500/1,000/500 split.
- VLM SFT records: 3,485 train / 498 val / 1,001 test.

## Method
- **Detector:** YOLOv8-S with a confidence-conditioned Gated-Swin refinement at the P5 level: two shifted-window Swin blocks (window 8), residual output F + g(F)⊙S(F) with sigmoid gate; 640×640, 100 epochs; 5-fold CV runner; calibrated variant uses conf 0.01 and NMS IoU 0.35.
- **VLM:** DeepSeek-VL2 (vision encoder + adaptor + MoE LLM) with Dynamic Tiling Strategy (DTS) for high-res tiles, LoRA (rank 8, alpha 32, dropout 0.05) via SWIFT; 2×2 factorial (DTS on/off × LoRA on/off).
- Structured evaluator scores schema validity, disease class, localization match and IoU (free-text description not scored).
- System: gateway, actuators (irrigation, fans, spraying), database backend, web platform.

## Results
- Gated-Swin vs YOLOv8-S: mAP50 0.93346 → 0.93881; mAP50-95 0.68694 → 0.72753; precision 0.92001 preserved.
- Three seeds: mAP50-95 0.718198 ± 0.001424 (CV 0.198%).
- LoRA raised schema validity 0.9800 → 0.9820 and cut invalid outputs 0.0200 → 0.0180; disease and localization metrics stable across configurations; DTS mainly affects latency/memory.

## Limitations
Small VLM gains; description text quality was not evaluated; sensor data not actually fused with images in the models; single frozen dataset; detector gains specific to YOLOv8-S; no causal reasoning or recommendations evaluated.

## Transferable ideas for the FYP pipeline
- **Vision:** two-tier design — a fast detector (YOLOv8) localizes cut defects (dross, burrs, burn marks, incomplete cuts) and passes crops/boxes to the VLM, rather than asking the VLM to find defects itself.
- **Fine-tuning:** LoRA SFT of an open VLM (DeepSeek-VL2 / Qwen-VL) on image→JSON report pairs; use DTS/tiling for high-res sheet images.
- **LLM output:** enforce a JSON schema (defect class, location, severity, probable cause) and measure schema validity / invalid-output rate as an evaluation metric.
- **Data ingestion:** deduplicate near-identical images by hash before splitting to avoid leakage.
- **Deployment:** database + web dashboard architecture mirrors an operator-facing TruLaser monitoring tool.
