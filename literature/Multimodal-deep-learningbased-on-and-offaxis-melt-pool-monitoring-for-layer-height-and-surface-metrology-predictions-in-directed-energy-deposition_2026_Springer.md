# Multimodal deep learning-based on and off-axis melt pool monitoring for layer height and surface metrology predictions in directed energy deposition

- **Citation (IEEE):** R. Asadi, A. Ylä-Autio, O. H. Wiikinkoski, et al., "Multimodal deep learning-based on and off-axis melt pool monitoring for layer height and surface metrology predictions in directed energy deposition," *Journal of Intelligent Manufacturing*, vol. 37, pp. 3995–4022, 2026, doi: 10.1007/s10845-025-02714-1.
- **Domain:** Laser-based additive manufacturing (DED-LB/M with wire) process monitoring; computer vision + process-parameter fusion
- **Relevance to FYP (1-5):** 4 — laser materials processing with vision + machine-parameter fusion (FiLM) to predict quality; directly analogous to fusing TruLaser parameter tables with cut-part images, though no LLM.

## Problem
Wire-fed laser DED is sensitive to head-to-workpiece height deviations, thermal accumulation and defects (wire wobbling, stubbing, dripping, porosity) in multilayer builds. The authors want real-time melt-pool monitoring that also predicts bead geometry (layer height) and surface waviness.

## Data & modalities
- 21 multilayer wall depositions (10 layers each) with a 3 kW fibre laser, Inconel 625 wire on S355 substrate, designed at constant linear energy density with three wire-feed-rate/travel-speed ratios.
- 4,775 annotated frames from **on-axis and off-axis cameras** (classes: melt pool, wire, contact tip).
- Tabular metadata: laser power (LP), travel speed (TS), wire feed rate (WFR), layer index; ground truth from surface scans.

## Method
- Modified **YOLOv11** instance-segmentation model for melt-pool detection/segmentation.
- A lightweight multimodal CNN head where **Feature-wise Linear Modulation (FiLM)** injects process parameters (compact MLP produces per-sample scale/shift vectors) into dual-view image feature maps; compared against plain late concatenation and single/stacked-view variants.
- No LLM, RAG or fine-tuning of foundation models.

## Results
- Segmentation mAP50–95: 91.4% (box), 86.3% (mask); mask mAP +3.3% over vanilla YOLOv11.
- Inference: 7.2 ms/frame (138.9 fps) on Tesla P100; 16.25 ms (61.5 fps) on RTX A2000.
- Test RMSE: surface waviness 21.37 µm; layer height 7.34 µm (abstract) — note the highlights state 0.073 mm, an internal inconsistency in the text.
- FiLM-modulated dual-view model had the lowest test errors; on-axis frames outperformed off-axis.

## Limitations
Single material/feedstock and simple wall geometries; generalisability across materials, process variants and complex geometries untested; open-loop (no closed-loop control yet); purely data-driven (authors suggest physics integration).

## Transferable ideas for the FYP pipeline
- **Fusion:** use FiLM conditioning so TruLaser parameters (power, feed rate, gas pressure, focus position, bevel angle, sheet thickness) modulate image-encoder features of cut edges, instead of naive concatenation — then expose fused predictions (e.g. predicted roughness/dross) as evidence for the LLM.
- **Vision:** YOLO-style segmentation of kerf/edge/dross regions as a fast pre-processor feeding region crops or measurements to the MLLM.
- **Evaluation:** ablate fusion type (FiLM vs concat) and view count; report RMSE on physical quality metrics and fps/latency on edge GPU.
- **Data ingestion:** design-of-experiments dataset at controlled energy density is a template for collecting labelled laser-cut samples.
