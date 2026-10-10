# Interactive text-guided image segmentation via vision Mamba and large language models

- **Citation (IEEE):** Y. Meng, H. Sun, and W. Jiang, "Interactive text-guided image segmentation via vision Mamba and large language models," *Scientific Reports*, vol. 16, art. 14061, 2026, doi: 10.1038/s41598-026-43841-w.
- **Domain:** Computer vision / vision-language referring segmentation
- **Relevance to FYP (1-5):** 2 - general-domain referring segmentation; useful as a design pattern for operator-queried defect localisation ("segment the dross on the lower bevel edge") and partial LLM fine-tuning, but no industrial data.

## Problem
Text-guided (referring) image segmentation requires grounding complex linguistic references (attributes, spatial relations) to pixel-precise masks; static text encoders underfit task-specific cues and dense prediction training is unstable.

## Data & modalities
Natural images + referring expressions: RefCOCO, RefCOCO+, RefCOCOg (standard val/testA/testB splits). Interactive click feedback for iterative refinement.

## Method
"H-type Bidirectional Alignment Network". Visual encoder: 12-layer, four-stage Vision Mamba (selective state-space model) with local convolution and residual blocks for boundary detail at lower cost on high-resolution images. Text encoder: encoder-only variant of Qwen2-0.5B with bottom layers frozen and the top 2 transformer layers fine-tuned. Cross-modal alignment: Q-Former learnable queries (CLIP-based alignment); forward path does text-to-image segmentation, backward path reconstructs image-over-text attention, with a bidirectional consistency constraint between a segmentation head and a text-attention head. Multi-scale decoder fuses visual and aligned features; interactive iterative refinement via user clicks.

## Results
RefCOCO val IoU: full model 67.69%, RefCOCO+ 61.64%, RefCOCOg 55.96%. Ablations: ResNet50 instead of Vision Mamba 64.19%; BERT-base instead of Qwen 64.69% (2-3% drop); concatenation instead of Q-Former cross-attention 65.47%. Text-encoder tuning: frozen 66.12%, full fine-tuning (>500M params) 66.85% (overfits), top-2 tuning (28.5M trainable) 67.69%. Vision Mamba cuts FLOPs by about 35% vs ResNet with ~30% faster inference. Overall IoU gains of 2.4-3.2% over SOTA and 43% user-efficiency gain in interaction.

## Limitations
Long text descriptions degrade performance; very high-resolution images need hierarchical processing; click-only interaction; generalisation to specialised domains (e.g., medical, satellite) untested; needs compression for real-time/edge use; code only on request.

## Transferable ideas for the FYP pipeline
- **Vision:** text-promptable segmentation lets an LLM agent ask the vision module for a specific region (e.g., "burr along the bottom edge") and get a mask to measure.
- **Fine-tuning:** partial fine-tuning of only the top layers of a small LLM/text encoder beat both frozen and full fine-tuning on limited data - relevant when adapting to a small laser-cutting corpus (alternative/complement to LoRA).
- **Fusion:** Q-Former query-based alignment between image features and text as a lightweight fusion module.
- **Deployment/HITL:** interactive click refinement lets an operator correct masks before the LLM report is generated.
