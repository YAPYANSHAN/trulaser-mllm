# Fourier-Taylor progressive knowledge distillation for RGB+IR object detection in complex environments

- **Citation (IEEE):** C. Li and J. Liu, "Fourier-Taylor progressive knowledge distillation for RGB+IR object detection in complex environments," *Expert Systems With Applications*, vol. 331, Art. no. 133451, 2026, doi: n/a.
- **Domain:** Computer vision / multimodal (RGB + thermal IR) object detection, knowledge distillation
- **Relevance to FYP (1-5):** 2 - autonomous-driving detection, but cross-modal distillation into a tiny edge detector is a usable vision/deployment pattern (e.g., RGB + thermal imaging of cut parts).

## Problem
Multimodal RGB+IR detectors are robust but too heavy for edge devices, while unimodal lightweight detectors lack accuracy in low-light or complex scenes. Spatial-only feature imitation in knowledge distillation (KD) transfers cross-modal knowledge poorly.

## Data & modalities
Three RGB-infrared object detection benchmarks: M3FD, FLIR and LLVIP. The modalities are paired visible and thermal images.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Teacher and student:** the teacher is a multimodal YOLOv11x (RGB+IR fusion, 114.8M parameters). The student is a unimodal YOLOv11n (RGB-only or IR-only).
- **FSAM (Frequency Spectrum Alignment Module):** aligns the Fourier amplitude and phase of teacher and student features to capture global, modality-invariant structure.
- **TRRM (Taylor-inspired Residual Refinement Module):** approximates the non-linear teacher-student discrepancies via zero-order identity plus trainable residual terms. This makes the student emulate the teacher's local response sensitivity (edges, texture gradients).
- **Progressive distillation:** a coarse-to-fine schedule alternates the two losses (L_Fourier + L_Taylor). There is no LLM.

## Results (key numbers and metrics)
- **M3FD, RGB student:** AP is 55.3% vs. 47.7% for the baseline (+7.6), which is 1.2 points above the teacher, with 2.86M parameters (about 97.5% fewer than the teacher).
- **M3FD, IR student:** AP rises from 41.6% to 45.0%.
- **Ablation:** the full FTPKD reaches 82.8% mAP50, +8.8 points over the baseline.
- **Jetson Nano:** latency is 14.2 ms vs. 120.4 ms for the teacher (23.7 vs. 398.1 GFLOPs).

## Limitations
- Confusion between small or distant objects and the background (person→background 0.37, bus→background 0.42 on M3FD), caused by IR thermal blurring and scale variation.
- Future work: scale-adaptive attention and stronger cross-modal integration.

## Transferable ideas for the FYP pipeline
- **Vision:** if defect images come from several sensors (e.g., RGB camera plus a thermal or coaxial process camera on the TruLaser), train a heavy multimodal detector offline, then distil it into a lightweight single-camera YOLO for shop-floor deployment.
- **Vision/fusion:** frequency-domain feature alignment may suit periodic surface textures such as cut striations, burr and dross patterns, where FFT signatures are informative.
- **Deployment:** benchmark latency, GFLOPs and parameters on edge hardware alongside mAP.
- **Evaluation:** use per-class confusion matrices to expose small-defect-vs-background errors.
