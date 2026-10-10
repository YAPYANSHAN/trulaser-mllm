# A data-efficient 3D medical vision-language model using only a 2D encoder

- **Citation (IEEE):** Y. Lian, Y. Xie, Y. Jiang, et al., "A data-efficient 3D medical vision-language model using only a 2D encoder," *Scientific Reports*, vol. 16, art. 8809, 2026, doi: 10.1038/s41598-026-39526-z.
- **Domain:** Medical imaging / 3D vision-language models (report generation, VQA)
- **Relevance to FYP (1-5):** 3 - medical domain, but its recipe (frozen 2D CLIP encoder, token pruning, frequency-domain fusion, LoRA-tuned LLaMA) is a data-efficient VLM design suited to a small industrial image set.

## Problem
3D medical VLMs depend on specialised 3D vision encoders that need large annotated 3D datasets, which are scarce; they also suffer from slice redundancy and spatial-only features that miss texture/heterogeneity cues.

## Data & modalities
3D CT volumes (processed as 2D slices) + text. Training/evaluation: M3D-Data (M3D-Cap report generation, M3D-VQA). Cross-modal adaptability tested on BraTS 2023 (MRI) and AutoPET (PET).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Pre-trained 2D biomedical CLIP vision encoder (BiomedCLIP-style) extracts slice-wise features.
- Cosine-similarity slice selection prunes redundant slices.
- Spatial-Frequency Cross-domain Fusion module models inter-slice correlations using spatial and frequency-domain information.
- Fine-grained feature injection (downsampling factor 2) re-introduces high-resolution details into compressed visual tokens.
- LLM: LLaMA-2-7B. Two-stage training: (1) freeze encoder and LLM, train the intermediate modules on image-text pairs; (2) instruction tuning with LoRA (r=16, alpha=32, dropout 0.1, context 512), LR 2e-5, warm-up + cosine decay.
- Compared with RadFM, M3D-LaMed, Med3DVLM.

## Results (key numbers and metrics)
- M3D-Cap report generation: METEOR 50.13, a 37.6% improvement over the previous best (Med3DVLM).
- M3D-VQA closed-ended: 82.90% average accuracy, +3.15 percentage points over prior best.
- Adaptability demonstrated on MRI and PET data.

## Limitations
English-only data; not evaluated on ultrasound/OCT; public 3D image-caption data remains small relative to 2D generic datasets.

## Transferable ideas for the FYP pipeline
- **Vision:** reuse a frozen pre-trained 2D encoder (CLIP/SigLIP) rather than training a domain encoder; for multi-view or sequential images of a cut part (or frames from in-process camera), treat them as "slices".
- **Fusion:** prune redundant views/frames by cosine similarity of embeddings to cut tokens and cost; frequency-domain features may capture striation periodicity on laser-cut edges.
- **LLM reasoning / fine-tuning:** two-stage training (projector alignment, then LoRA instruction tuning) with the LoRA hyperparameters given is a concrete, low-cost starting recipe.
- **Evaluation:** report both closed-ended (accuracy on defect-type questions) and open-ended (METEOR/BLEU on diagnostic reports) metrics.
