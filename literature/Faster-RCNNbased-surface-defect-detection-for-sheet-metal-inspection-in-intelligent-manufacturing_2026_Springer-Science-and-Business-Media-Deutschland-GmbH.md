# Faster R-CNN-based surface defect detection for sheet metal inspection in intelligent manufacturing

- **Citation (IEEE):** C.-H. Chen, S. N. Maurya, K.-Y. Li, et al., "Faster R-CNN-based surface defect detection for sheet metal inspection in intelligent manufacturing," *Int. J. Adv. Manuf. Technol.*, vol. 145, pp. 7021–7035, 2026, doi: 10.1007/s00170-026-18383-0.
- **Domain:** Industrial visual inspection — sheet-metal surface defect detection (AOI)
- **Relevance to FYP (1-5):** 4 — directly about sheet-metal defect detection on a real production line. It is a strong candidate for the vision front-end / non-LLM baseline in the FYP, though it covers coil surface defects rather than laser-cut edges and has no LLM.

## Problem
Manual inspection and rule-based machine vision of sheet-metal surfaces are inefficient, operator-dependent and fragile under industrial illumination, texture and noise. Many deep-learning studies use only laboratory datasets and are not validated on production lines.

## Data & modalities
Real production-line images of a steel coil surface. Two 4K line-scan cameras at 12k lines/s with bright-field lighting. Images range from 4096×512 to 4096×4096 px. Classes: block, strip, spot and hole defects plus normal surface, with bounding-box annotations. 1,547 annotated images: 1,437 for training/validation (7:3 split) and 110 for testing.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Preprocessing: Gaussian noise filtering, contrast enhancement (histogram equalisation / intensity stretching) and normalisation.
- Faster R-CNN with a ResNet-50 feature extractor and RPN for localisation and classification.
- Training: Adam, initial learning rate 0.01, momentum 0.9, weight decay 5e-4, reduce-on-plateau (factor 0.1, patience 15).
- No LLM or multimodal fusion.

## Results (key numbers and metrics)
- Confusion matrix: TP 238, TN 2,977, FP 15, FN 10. Accuracy 99.24%, precision 94.97%, recall 96.60%.
- Image-level: 108/110 test images correct (98%).
- Inference ~92 ms per image (~10.8 FPS) end to end.
- The authors' comparison table reports higher accuracy than prior CNN, VGG16, DenseNet121, DEENet and ID-MSNet studies, though these were evaluated on different datasets.

## Limitations
Fine or low-contrast defects and complex textures cause misclassifications. Moderate dataset size from a single line. No mAP/IoU reporting. The comparison with prior work is not on a common benchmark. Speed depends on resolution. Future work: real-time optimisation, more defect variants and edge deployment.

## Transferable ideas for the FYP pipeline
- **Vision:** use Faster R-CNN (ResNet-50) or YOLO as a defect localiser on cut-part photos (dross, burr, scorch marks, incomplete cuts, pitting). Crop the detected regions and pass them with labels to the MLLM for explanation and root-cause reasoning. This mirrors the detector-plus-VLM pattern.
- **Data ingestion:** controlled acquisition (fixed camera and bright-field lighting) and simple preprocessing (denoise, contrast stretch) noticeably help on metallic surfaces. Specify an image-capture protocol for TruLaser parts.
- **Evaluation:** report the confusion matrix with precision and recall, plus mAP for localisation, and latency. Explicitly analyse low-contrast failure cases.
- **Baseline:** use this CNN detector as the non-LLM vision baseline when arguing the added value of multimodal LLM reasoning.
