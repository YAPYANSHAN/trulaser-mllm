# Lightweight multimodal large language model enabling efficient one shot industrial visual anomaly detection

- **Citation (IEEE):** P. Sundaravadivel, R. Augustian Isaac, U. Kumaran, et al., "Lightweight multimodal large language model enabling efficient one shot industrial visual anomaly detection," *Discover Artificial Intelligence*, vol. 6, Art. no. 483, 2026, doi: 10.1007/s44163-026-01252-w.
- **Domain:** Industrial visual anomaly detection (surface cracks, metallic scratches, PCB defects) with lightweight vision-language models on edge hardware.
- **Relevance to FYP (1-5):** 4 - one-shot, prompt-guided defect detection on metal surfaces with edge deployment fits the image stage, but the "LLM" is only a compact text encoder and the reported results are internally inconsistent.

## Problem
Deep anomaly detectors need many defect images and heavy GPUs. Existing MLLM approaches are computationally expensive, are not real-time on edge devices and lose accuracy when only one defective example exists. Many detectors also cannot explain *why* a region is anomalous.

## Data & modalities
Images + short natural-language defect prompts ("surface crack", "colour deviation", "texture inconsistency"). Benchmarks: MVTec-AD, VisA, PCB-Defect (over 20 defect categories). One-shot protocol: one normal + one defective sample per class. Images resized to 256x256 with contrast normalisation. A cross-domain crack test also lists CRACK500, DeepCrack, ADE20K, COCO, Ego4D and fMoW.

## Method
- Vision: ViT-Tiny or Mobile-Swin encoder with bottleneck adapter modules (fewer than 10% of parameters trainable).
- Text: compact text encoder "distilled from CLIP or MiniGPT-4", prompt-tuned; prompts act as linguistic priors.
- Fusion: projection to a shared space and cross-attention; prompt-grounded attention weights image patches by text relevance.
- Losses: CLIP-style contrastive loss, an auxiliary reconstruction loss and L2 regularisation (contrastive embedding regularisation, CER).
- Scoring: anomaly score = 1 - cosine(fused embedding, mean normal prototype). There is also a normal-only mode that uses generic prompts.
- Explainability: Grad-CAM/attention maps and SHAP (linear and kernel explainers, 1000 background samples).
- Deployment: INT8 mixed-precision quantisation and structured pruning bring the model under 100 MB. Hardware: Jetson Nano 4 GB and RTX A5000.
- No generative LLM, no RAG and no chain-of-thought. The paper says outright that it does not produce explicit reasoning.

## Results
- Reported: accuracy 98.3%, precision 97.6%, recall 96.9%, F1 0.972, AUC 0.986; 14.5 M parameters; 92 ms inference; about 25 FPS on Jetson Nano.
- Reported gains: about 60% fewer parameters and about 45% lower latency than baselines (Swin-UNet, PatchCore++, CLIP-AD, ProtoAD); +2.2% accuracy and +3.8% F1 vs ProtoAD.
- Ablation: +2.9 pp from CER, +2.1 pp from prompt conditioning, +1.5 pp from adapters.
- Wilcoxon p < 0.01 over 15 categories; run-to-run standard deviation ±0.42%.
- The paper also claims prompt wording (synonyms or generic prompts) caused only a small drop in performance.

## Limitations
- The authors' own figures conflict. The ROC figure is quoted as AUC = 0.926, and the confusion matrix (414 TN, 427 TP, 85 FP, 74 FN) works out to about 84% accuracy, not 98.3%. Treat the headline numbers with caution.
- Architecture details are vague ("ViT-Tiny or Mobile-Swin", "CLIP or MiniGPT-4").
- No proprietary industrial data; the authors list this as future work.
- Image-only detection. The "MLLM" produces no free-form diagnosis.

## Transferable ideas for the FYP pipeline
- **Vision:** Score defects as distance from a normal-part prototype. This works when only one or two images of bad TruLaser bevel cuts exist, and the normal-only mode suits early data collection.
- **Vision / text:** Write a small set of prompts in laser-cutting terms ("dross on bottom edge", "burn-out", "excessive striation") to steer patch attention. Test the system with prompts worded in different ways.
- **Fusion:** Pass only the anomaly score and heatmap from a small edge model to a larger reasoning LLM. This splits a fast detector from a slow explainer.
- **Deployment:** INT8 quantisation and pruning give a model under 100 MB for a camera at the machine. Leave LLM reasoning on a server.
- **Evaluation:** Report a confusion matrix together with AUC, and check that they agree. This paper shows why that check matters.
