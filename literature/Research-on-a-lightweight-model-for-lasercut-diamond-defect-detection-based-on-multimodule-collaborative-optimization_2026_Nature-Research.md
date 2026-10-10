# Research on a lightweight model for laser-cut diamond defect detection based on multi-module collaborative optimization

- **Citation (IEEE):** A. Zhu, Q. Jiang, H. Guo, et al., "Research on a lightweight model for laser-cut diamond defect detection based on multi-module collaborative optimization," *Scientific Reports*, vol. 16, art. 21233, 2026, doi: 10.1038/s41598-026-51745-y.
- **Domain:** Industrial visual inspection — laser-cutting defect detection (lightweight object detection)
- **Relevance to FYP (1-5):** 4 — directly about defects produced by laser cutting (cracks, ablation) with a fibre laser and a deployable lightweight detector; however, the material is diamond rather than sheet metal and no LLM is used.

## Problem
Laser cutting of diamond causes defects (cracks, ablation, bursts) through thermal stress; manual/microscope inspection is slow and operator-dependent, and standard deep detectors are too heavy for resource-limited (e.g. handheld) inspection devices.

## Data & modalities
RGB microscope images (AO-HD208C electron microscope, SN-60R camera, 1920×1080) of one batch cut on a fibre laser (1064 nm, 300 W, 2000 mm/min, 0.2 ms pulse, 180 Hz). Four classes with 7:2:1 split: ablation (435/125/63), burst (140/40/20), adulterant (225/64/32), crack (1075/307/156). Images resized to 640×640; augmentation by flipping, cropping, noise.

## Method
FAS-YOLO built on YOLOv11n:
- **FDConv** (frequency-domain dynamic convolution) rebuilds the C3k2 block to emphasise high-frequency crack/fracture details;
- **ADown** adaptive downsampling to cut parameter redundancy;
- **SEAM** attention in the detection head to focus on defect regions and suppress metal-reflection background.
Ablation study per module; comparison with YOLO variants. No LLM/multimodal fusion.

## Results
- Precision 92%, recall 80.4%, mAP50 82.6%.
- Versus YOLOv11n: parameters −37.4%, GFLOPs −40%, model size −34.6% with competitive accuracy.
- Crack and burst classes recognised with few false positives/negatives; adulterant class weaker (AP reported ~0.715 for "AD" due to microscope texture).

## Limitations
Only four defect types; small, single-batch dataset (privacy-restricted, not public); trained only under conventional cutting conditions, robustness to illumination changes unverified; edge deployment not yet demonstrated.

## Transferable ideas for the FYP pipeline
- **Vision:** a lightweight YOLO detector (with frequency-aware convolutions and attention against reflections) is a good first-stage defect localiser for shiny metal cut edges before passing crops/labels to the MLLM.
- **Data ingestion:** record laser parameters (power, speed, pulse width, frequency) with each image — the paper reports them per dataset; the FYP should store them per sample to enable parameter–defect reasoning.
- **Class imbalance:** expect long-tail defect classes; report per-class AP.
- **Future fusion:** the authors propose visible + infrared fusion and pruning/quantisation/distillation for edge deployment — both applicable to an on-machine TruLaser inspection station.
- **Evaluation:** report P/R/mAP50 plus parameters, GFLOPs and model size for deployment trade-offs.
