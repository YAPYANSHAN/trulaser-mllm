# Fine-grained alignment in medical pathology vision-language models via variational distillation

- **Citation (IEEE):** R. Huang, H. Lin, W. Zhuo, et al., "Fine-grained alignment in medical pathology vision-language models via variational distillation," *Pattern Recognition*, vol. 180, Art. no. 114283, 2026, doi: 10.1016/j.patcog.2026.114283.
- **Domain:** Medical imaging / computational pathology; vision-language prompt learning (CLIP-style).
- **Relevance to FYP (1-5):** 2 - Medical domain, but the problem (fine-grained discrimination of visually similar classes with few labels using a CLIP-style VLM + LLM-generated class descriptions) maps onto distinguishing similar cut-edge defects.

## Problem
General VLMs (CLIP) and prompt-learning variants (CoOp, MaPLe, PromptSRC, CoPrompt, ATPrompt) fail on pathology images where classes (e.g., adipose, debris, mucus, stroma) differ only subtly. LLM-generated descriptions can inject redundant/ambiguous text, while strong cross-modal coupling amplifies modality-specific visual noise.

## Data & modalities
Histopathology image + text prompts/descriptions. Five public benchmarks: Kather, Colorectal Histology, BloodMNIST, KIMIA Path960 (class generalization, few-shot), PanNuke (cross-organ transfer). Metrics: accuracy and (macro-)F1.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
PromptDVD: CLIP ViT-B/16 initialised from PLIP (pathology CLIP), template "a photo of a {class}", learnable multimodal prompts (prompt depth ~9). Components: (1) Cross-granular Variational Distillation - coarse class prompts and fine-grained LLM descriptions are mapped to variational latent distributions and aligned with a KL loss so only robust semantics survive; (2) Information Bottleneck to amplify modality-shared and suppress modality-specific features; (3) Dual-Loop Feature Modulation - inner loop records gradients and stores image/text features in a memory bank; outer loop uses gradient-based saliency to modulate image features. No full fine-tuning of backbone; parameter-efficient prompt learning. Descriptions compared from Claude Sonnet 4.6, Gemini 2.5 Pro, GPT-5.2, Kimi K2.5, Qwen 3.5 Plus.

## Results (key numbers and metrics)
- Ablation on Kather: baseline 76.80% acc / 70.45% F1; +VD 79.29%; +IB 81.64%; full (with DLM) 85.75% acc / 80.52% F1; best loss weight w=1.75 gives 87.14%.
- Class-generalization case study: DEB 86.1%, TUM 87.8% (best among compared).
- Description source matters: Kimi K2.5 85.84% vs Qwen 3.5 Plus 80.79% (generalization acc).
- Claimed best results across all five datasets and cross-organ transfer vs. MaPLe/CoPrompt/PromptSRC.

## Limitations
Weak on heterogeneous malignant cases (HeadNeck, Kidney) because generic LLM descriptions lack expert knowledge; dual-loop training increases training time (inference comparable); classification only, no generative reasoning.

## Transferable ideas for the FYP pipeline
- **Vision:** Use a CLIP-style backbone with learnable prompts for few-shot classification of cut defects (dross, burr, striations, bevel angle error) when labelled images are scarce.
- **Text/RAG:** Generate fine-grained defect descriptions from TRUMPF documentation (not generic LLM knowledge) as class text anchors; paper shows description quality/source changes accuracy by ~5 points.
- **Fusion:** KL-based alignment between coarse labels and detailed descriptions to filter noisy text - useful when manuals contain verbose, partly irrelevant wording.
- **Evaluation:** Report accuracy plus macro-F1, and test "unseen class" generalization (new defect types / new materials) as separate split.
