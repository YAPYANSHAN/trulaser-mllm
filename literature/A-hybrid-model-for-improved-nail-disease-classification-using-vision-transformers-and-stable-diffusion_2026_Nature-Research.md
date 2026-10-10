# A hybrid model for improved nail disease classification using vision transformers and stable diffusion

- **Citation (IEEE):** R. Nijhawan, A. Gupta, M. Diwakar, et al., "A hybrid model for improved nail disease classification using vision transformers and stable diffusion," *Scientific Reports*, vol. 16, art. 1544, 2026, doi: 10.1038/s41598-025-04538-8.
- **Domain:** Medical imaging (dermatology) / generative data augmentation
- **Relevance to FYP (1-5):** 2 - medical domain; transferable only as a recipe for diffusion-based synthetic augmentation of rare defect images.

## Problem
Nail-disease classification is limited by small, imbalanced, privacy-constrained datasets. The study tests whether few-shot fine-tuned Stable Diffusion can generate realistic synthetic images that improve classifier accuracy.

## Data & modalities
RGB nail images. Training source: open Kaggle nail_dataset_disease with 4 classes (clubbing, blue finger, eczema, onycholysis); a custom real-world test set compiled from datasets and clinical repositories. 5,466 images used to tune the generative model; images resized to 512x512 for generation.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Text-to-image Stable Diffusion fine-tuned with DreamBooth and LoRA in a few-shot setting; generation volume weighted toward under-represented classes (e.g., clubbing, blue finger) to balance the dataset.
- Hybrid dataset (reported as roughly 80% synthetic / 20% real for the ViT configuration).
- Classifiers: ViT (google/vit-base-patch16-224-in21k) and MobileNetV2 (ImageNet-pretrained), fine-tuned on hybrid data and evaluated on real unseen data.
- No LLM reasoning, RAG or KG.

## Results (key numbers and metrics)
- Synthetic data increased accuracy by 3.26% for MobileNetV2 and 3.02% for ViT.
- Reported accuracies on the comparison table: MobileNetV2 (proposed) 75.69%, ViT (proposed) 72.79%, vs prior works between 67.8% and 71.5%.
- Confusion matrices provided for both datasets.

## Limitations
Overfitting to synthetic data (noted for MobileNetV2); high computational cost of ViT and diffusion training; only four classes; modest absolute accuracy; generalisation to broader real-world data and statistical significance testing are left as future work.

## Transferable ideas for the FYP pipeline
- **Data ingestion / vision:** use DreamBooth+LoRA fine-tuned Stable Diffusion on a handful of real images per rare cut defect (e.g., bevel-angle deviation, incomplete cut, heavy dross) to synthesise extra samples; allocate generation in inverse proportion to class frequency.
- **Evaluation:** always test on held-out real images only and report the real-vs-hybrid accuracy delta; watch for synthetic overfitting by limiting the synthetic ratio.
- **Vision:** MobileNetV2 provides a lightweight edge-deployable baseline against which to judge VLM classification.
