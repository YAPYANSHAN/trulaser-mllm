# Multimodal content generation and enhancement for smart imaging

- **Citation (IEEE):** K. Zhang, D. Wu, Y. Song, et al., "Multimodal content generation and enhancement for smart imaging," *Discover Artificial Intelligence*, vol. 6, Art. no. 1175, 2026, doi: 10.1007/s44163-026-02108-z.
- **Domain:** Multimodal-conditioned image enhancement/generation (medical, natural scenes, industrial inspection).
- **Relevance to FYP (1-5):** 2 - generates enhanced images rather than diagnosing faults; uses no LLM. Only its image-text-label fusion modules and the MVTec subset are loosely relevant.

## Problem
Image enhancement conditioned jointly on a reference image, a text description and pixel-level semantic labels. Existing methods use one or two of these, suffer a cross-modal semantic gap, and trade detail fidelity against semantic consistency.

## Data & modalities
Image + text + semantic label maps. MIID-50K (introduced by the authors): 50,000 triplets at 1024x1024, about 16,667 each from NIH ChestX-ray14 (medical), MS-COCO 2017 (natural) and MVTec AD (industrial, 15 categories). Medical and industrial texts were written by experts (Cohen's kappa = 0.87). Labels come from Mask R-CNN with manual correction. Blur (Laplacian variance < 100) and duplicate (pHash) filtering; 8:1:1 split. Also MS-COCO 2017 val (5000 pairs).

## Method
MCGE-Net (not an LLM):
- Encoders: ResNet-50 (stage-4 features -> 256 tokens, 768-D), BERT-base text (128 tokens), label embedding plus an MLP.
- HCMA (hierarchical cross-modal attention): fine-grained token-level and coarse globally pooled cross-attention, with a learnable per-sample gate between the two.
- DFA (dynamic feature alignment): instance-adaptive modality weights to narrow the semantic gap.
- MSEN (multi-scale enhancement network): pyramid with channel attention, followed by a decoder.
- Loss: reconstruction, perceptual, adversarial (PatchGAN 70x70) and multimodal-consistency terms. Two-stage training, 200 epochs, 4x A100, input 512x512.

## Results
- MIID-50K: PSNR 32.1 dB, SSIM 0.903, FID 24.8, Semantic Consistency 89.5%.
- MS-COCO: FID 20.4, CLIP-Score 33.8.
- Beats ControlNet, Stable Diffusion, Imagen, DALL-E 2, GLIDE and VQGAN (p < 0.001, Bonferroni-corrected). Most baselines were not fine-tuned on MIID-50K; the authors acknowledge this and give a fine-tuned comparison in the supplement.
- Cost: 1.23 s/sample (Stable Diffusion 2.34 s, Imagen 2.67 s); 110.3M parameters and 187.6 GFLOPs.
- Industrial-subset IoU 0.857; medical Dice 0.912; inter-scenario PSNR standard deviation 0.38 dB.
- 50-participant user study.

## Limitations
- Failure modes: semantic drift on long-tail categories (8.3% of test samples), scale-boundary artifacts (5.1%) and label-boundary blur (4.7%).
- Too large for edge devices; static images only.
- No attribution of which modality drove the output, so the system is not explainable.
- Weaker in data-scarce domains.
- Validation is on curated data only; the authors say safety-critical use needs domain validation.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** Copy the dataset-building QA steps: Laplacian-variance blur filter, pHash de-duplication, a split at source-image level to avoid leakage, and two annotators with kappa reported. All apply directly to collecting cut-part photos.
- **Fusion:** Gated fine-grained + global cross-attention (HCMA) is a reusable pattern for fusing image tokens with text (operator notes, manual excerpts) before a reasoning head.
- **Vision / data augmentation:** Use label-plus-text-conditioned generation to synthesise rare defect images (e.g., severe dross on thick plate) for training the vision stage. Validate the synthetic images against real ones before relying on them.
- **Evaluation:** Use CLIP-based image-text semantic consistency as a cheap automatic check that a generated defect description matches the image.
