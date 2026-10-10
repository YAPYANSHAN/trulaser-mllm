# Adaptive Multimodal Large Language Model with Hierarchical Cross Modal Grounding for Real Time Industrial Visual Anomaly Detection on Edge Devices

- **Citation (IEEE):** P. Sundaravadivel, U. Kumaran, E. S. Vinoth Kumar, et al., "Adaptive multimodal large language model with hierarchical cross modal grounding for real time industrial visual anomaly detection on edge devices," *Discover Artificial Intelligence*, vol. 6, art. 1044, 2026, doi: 10.1007/s44163-026-02008-2.
- **Domain:** Industrial visual anomaly / surface-defect detection (manufacturing QC, edge AI)
- **Relevance to FYP (1-5):** 4 - lightweight vision-language defect detection with text-prompt grounding and explainability on industrial images; directly informs the image/defect branch, though not laser cutting and no generative reasoning.

## Problem
Industrial surface anomaly detection suffers from scarce defect data, heavy compute, and poor interpretability. Earlier MLLM-based detectors (incl. the authors' Light-MLLMAD) use a single-scale encoder, a fixed prompt granularity, and a static normal prototype that cannot follow production-line drift.

## Data & modalities
RGB images paired with operator text prompts (defect vocabularies). Benchmarks: MVTec-AD, VisA, BTAD, PCB-Defect, plus a cross-domain evaluation on six datasets. One-shot supervision. Images CLAHE-normalised and resized to 256x256.

## Method
HCG-MLLMAD, six modules: (i) dual-branch visual encoder - ViT-Tiny (global, with bottleneck adapters, rank r=64, <2% extra params) + MobileNet-V4 feature pyramid (local, 3 scales), concatenated after global average pooling; (ii) Hierarchical Prompt Router choosing coarse/moderate/fine prompts based on visual entropy; (iii) hierarchical cross-attention fusion of text-encoder embeddings and visual features; (iv) Adaptive Contrastive Prototype Memory (momentum/EMA update of normal-class prototypes at inference, no retraining); (v) anomaly scoring head (score, label, optional heatmap); (vi) edge optimiser (INT8 quantisation). Contrastive embedding regularisation (CER) inherited from Light-MLLMAD. Explainability via SHAP and Grad-CAM++. Trained with AdamW, lr 3e-4.

## Results
99.1% accuracy and 0.993 AUC (one-shot), above Light-MLLMAD (98.3%, 14.5M params, 92 ms). 18.3M parameters, 3.9 GFLOPs, 78 ms on Jetson Orin Nano (~12.8 FPS); INT8 variant 61 ms (16.4 FPS). AUC 0.991 on PCB-Defect, 0.989 on VisA. Ablation: +6.5 pp from CER+adapters, +0.3 pp dual-branch, +0.3 pp HPR, +0.2 pp ACPM. No-prompt fallback still +2.0% AUC over baseline.

## Limitations
RGB only (no depth/thermal/hyperspectral). ACPM assumes fairly stable production statistics; untested under abrupt process changes. Failure analysis: ~63% of false negatives are low-contrast defects, ~24% partially occluded defects, ~13% illumination/reflection/clutter - metallic reflective surfaces are explicitly a weak point. Global average pooling suppresses small defects. "MLLM" here is a compact vision-text model, not a generative LLM producing explanations.

## Transferable ideas for the FYP pipeline
- **Vision:** dual global/local encoder for cut-edge images (dross, burr, striations need fine texture); CLAHE preprocessing for reflective sheet metal.
- **Vision / fusion:** prompt-grounded defect scoring using a TRUMPF-specific defect vocabulary (e.g. "burr on bevel edge", "dross", "incomplete cut") at multiple granularities.
- **Data ingestion / deployment:** online prototype memory of "good cut" embeddings per material/thickness to absorb drift without retraining; one-shot setting suits scarce defect photos.
- **Evaluation:** report latency, params, per-class failure analysis (low contrast, occlusion, illumination) and SHAP/Grad-CAM++ heatmaps as evidence passed to the LLM reasoning stage.
