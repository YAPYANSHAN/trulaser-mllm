# Hybrid framework for lesion-aware, clinically coherent chest X-ray report generation using contrastive learning and large language models

- **Citation (IEEE):** W.-J. Noh, S.-W. Pi, and B.-D. Lee, "Hybrid framework for lesion-aware, clinically coherent chest X-ray report generation using contrastive learning and large language models," *Scientific Reports*, vol. 16, art. 4645, 2026, doi: 10.1038/s41598-025-34799-2.
- **Domain:** Medical imaging / vision-language report generation
- **Relevance to FYP (1-5):** 3 - medical domain, but the "region-level findings -> LLM aggregator -> coherent report" pattern and LLM-based label extraction map directly onto defect-image-to-diagnosis-report generation.

## Problem
Automated chest X-ray (CXR) report generation suffers from a trade-off: full-image methods miss localized lesions, while region-based methods produce redundant or contradictory narratives (e.g., "no consolidation" and "patchy opacities" in the same zone).

## Data & modalities
Chest-Imagenome dataset (CXR images with anatomical ROIs and radiology reports). Modalities: images + free-text reports. Fine-grained lesion labels with anatomical location were produced by an LLM label-extraction pipeline and validated against CheXbert labels and a radiologist-annotated test subset.

## Method
CLALA-Net: ViT-B (ImageNet-pretrained) image encoder and a BERT-based text encoder. Three modules: (1) Lesion Cross-Attention (LCA) injects full-image lesion-classification cues into each ROI embedding; (2) Lesion-Level Contrastive Learning (LLCL) pulls together ROI embeddings with the same lesion status/location across images; (3) Image-Text Contrastive Learning (ITCL) aligns visual and textual features. ROI descriptions are decoded with GPT-2, redundancy removed with BERTScore, and GPT-4o mini consolidates ROI-level sentences into a final report via designed prompts. Labels were extracted with chain-of-thought prompting (lesion list + example expressions; LLM states presence, location and rationale). No LoRA/fine-tuning of the LLM reported.

## Results
Mean lesion-level F1 0.40 (best among baselines such as RGRG, R2Gen, CvT-DistilGPT2, XrayGPT, LLaVA-Rad, MAIRA-2). LLM-judged report consistency total 14.32/20 (clinical accuracy, findings completeness, linguistic quality ~4.36, structure ~3.83). Ablation: neither LCA nor LLCL 14.02, LCA alone 14.29; both best. Training on LLM-derived labels outperformed CheXbert-derived labels, showing sensitivity to label quality.

## Limitations
Requires fine-grained anatomically localized annotations; single dataset; does not exploit native high-resolution MLLM encoders; hybrid pipeline (region extraction + cross-attention + LLM) is computationally heavier than end-to-end models; not all SOTA baselines reproduced.

## Transferable ideas for the FYP pipeline
- **Vision:** treat each cut-part image as global + regional crops (edge, kerf, bevel face, dross zone); inject global defect-class predictions into region features (LCA analogue).
- **Data ingestion / labelling:** use an LLM with chain-of-thought prompting to extract structured defect labels (type, location, rationale) from free-text operator logs or QA notes, then validate on a small expert-labelled subset.
- **LLM reasoning:** two-stage generation - per-region findings first, then an LLM aggregator that merges them into a non-contradictory diagnosis report.
- **Evaluation:** combine lexical metrics (ROUGE-L, METEOR) with an LLM-as-judge rubric (accuracy, completeness, structure, language) for generated fault reports.
