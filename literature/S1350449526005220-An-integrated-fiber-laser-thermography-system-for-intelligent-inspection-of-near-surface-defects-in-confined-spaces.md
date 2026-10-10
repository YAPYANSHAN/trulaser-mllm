# An integrated fiber-laser thermography system for intelligent inspection of near-surface defects in confined spaces

- **Citation (IEEE):** H. Li, J. Tao, D. Zhou, et al., "An integrated fiber-laser thermography system for intelligent inspection of near-surface defects in confined spaces," *Infrared Physics & Technology*, vol. 159, Art. no. 106887, 2026, doi: 10.1016/j.infrared.2026.106887.
- **Domain:** Non-destructive testing / laser active thermography, metal defect detection
- **Relevance to FYP (1-5):** 3 - metal defect imaging with Transformer restoration, YOLOv11 detection and quantitative sizing is a transferable vision stage. It is not laser cutting and uses no LLM.

## Problem
In-situ detection of near-surface defects (NSDs: micro-cracks, porosity, fatigue) in metallic components inside confined geometries, such as nuclear steam-turbine heat sinks. Conventional NDT lacks sensitivity to micro-defects and mechanical flexibility, and thermal images have low SNR.

## Data & modalities
- Active thermography image sequences of standard steel specimens and real nuclear heat sinks.
- 3D finite-element thermal simulations.
- The data are confidential.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Hardware:** a compact fibre-coupled semiconductor laser, decoupled from the inspection head for access to narrow gaps. Excitation of 90 W for 10 s, chosen by FE simulation to maximise thermal contrast without surface ablation.
- **Restoration:** a Transformer-based Restormer network denoises the thermal images.
- **Quantitative inversion:** Fuzzy C-Means clustering plus a back-propagation neural network estimate defect width and depth.
- **Detection:** an enhanced YOLOv11 with adaptive noise filtering and spatial attention.

## Results (key numbers and metrics)
- Restormer improves SNR by 8.9% over Gaussian filtering while preserving defect edges.
- Width estimation error is within 5%; depth error is mostly within 0.06 mm.
- YOLOv11 detection reaches mAP@50 of 97.9% on specimens and real heat sinks.

## Limitations
- Performance depends on stable imaging quality.
- Generalisation degrades under severe thermal disturbance (e.g., underwater nuclear environments).
- The data are confidential, so the results are not reproducible.
- No comparison across defect types beyond NSDs is reported.

## Transferable ideas for the FYP pipeline
- **Vision:** a three-stage image pipeline to reuse for cut-part images. (1) Learned restoration or denoising (Restormer) before detection, useful under shop-floor lighting, reflective stainless and spatter. (2) YOLOv11 with attention for defect localisation (dross, burrs, gouging, incomplete bevel). (3) A separate quantitative regressor to size defects (e.g., burr height, dross length), giving numeric evidence to the LLM.
- **Data ingestion:** use physics simulation (FE thermal models) to choose sensing parameters and to generate synthetic training data where real defects are scarce.
- **Evaluation:** report both detection (mAP@50) and sizing error (mm, %), so that LLM explanations can cite measured magnitudes.
