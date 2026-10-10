# Class Prototype Rectification and Multi-Scale Feature Measurement for Few-Shot Classification of Bearing Surface Defects

- **Citation (IEEE):** Y. Cang, C. Li, X. Zhang, et al., "Class prototype rectification and multi-scale feature measurement for few-shot classification of bearing surface defects," *Scientific Reports*, vol. 16, art. 24444, 2026, doi: 10.1038/s41598-026-51829-9.
- **Domain:** Industrial visual inspection / few-shot defect classification (metal bearings)
- **Relevance to FYP (1-5):** 3 - real production-line metal-surface defect classification with very few labelled samples and edge deployment; no LLM, but directly usable for the cut-part defect image branch.

## Problem
Industrial defect classifiers generalise poorly when labels are scarce. Metric-based few-shot methods (ProtoNets) use fixed embeddings, mean prototypes sensitive to outliers, and single-scale features that miss micro-cracks and low-contrast defects.

## Data & modalities
RGB images. mini-ImageNet (100 classes x 600 images; 64/16/20 split) for meta-training. Bearing surface-defect dataset from the Harbin Bearing Group production line (130 mm eight-ball steel bearing): two lateral 5 MP cameras and one circumferential 2 MP camera with fixed lighting; 7 fine-grained defect categories, 50 images each, cropped to 200x200, held out entirely for cross-domain testing.

## Method
Metric-based meta-learning with Conv-4 or ResNet-12 backbone: (1) adaptive weighted pooling - normalised learnable spatial weights with a local sliding operation, preserving fine detail; (2) Class Prototype Rectification - Sum-of-Absolute-Differences weighting in embedding space down-weights outlier support samples; (3) Multi-Scale Feature Measurement - per-block features, parallel local-global fusion with similarity attention, per-scale predictions ensembled with layer-wise supervision. Focal loss in meta-training. Episodic 5-way 1-shot/5-shot training; Grad-CAM and t-SNE for interpretation.

## Results
mini-ImageNet: +1.97% / +2.77% (1-/5-shot, Conv-4) over the best multi-scale baseline FMAF; +3.22% / +2.19% over PCIC on ResNet-12. Bearing dataset, 5-way 5-shot: 90.12 ± 0.29% (Conv-4) and 91.34 ± 0.53% (ResNet-12) vs best baselines 87.99% (MATANet) and 88.94% (RENet). Jetson Xavier NX with FP16/TensorRT: 200-400 FPS; six images per bearing in 0.015-0.03 s against a 4 s cycle requirement.

## Limitations
Needs controlled lighting (lens hood, supplementary light); poor accuracy on unseen (zero-shot) defect classes; confusion among highly similar defects (light rust, mill scale, shallow scratches); no explicit domain-adaptation mechanism across operating conditions; slightly higher parameters/FLOPs than simple baselines.

## Transferable ideas for the FYP pipeline
- **Vision:** with few labelled TruLaser defect photos per class (dross, burr, striation, incomplete cut, bevel-angle error), prototype-based few-shot classification is a practical starting point; rectified prototypes help when operator photos vary in lighting and viewpoint.
- **Vision:** multi-scale measurement suits defects ranging from fine edge roughness to large burn-outs.
- **Data ingestion:** fixed camera rig and lighting for cut parts substantially improves reliability on reflective metal.
- **Fusion / LLM reasoning:** feed the classifier's label + confidence + Grad-CAM region to the LLM as evidence; route low-confidence or unseen-defect cases to the VLM/human, since zero-shot classes fail here.
- **Deployment:** precomputed prototypes + FP16 TensorRT enables edge inference beside the machine.
