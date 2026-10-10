# Cross-lingual sentiment analysis via multimodal transformer fusion and lightweight deep ensemble learning framework

- **Citation (IEEE):** R. Yadav, D. K. Yadav, A. Jain, et al., "Cross-lingual sentiment analysis via multimodal transformer fusion and lightweight deep ensemble learning framework," *Knowledge and Information Systems*, vol. 68, art. 151, 2026, doi: 10.1007/s10115-026-02768-4.
- **Domain:** NLP / affective computing (multilingual text + speech sentiment classification).
- **Relevance to FYP (1-5):** 1 — unrelated domain; only the generic gated cross-attention fusion and missing-modality handling are loosely transferable.

## Problem
Sentiment models are mostly monolingual and text-only, generalising poorly across languages, code-switching and acoustic conditions. The paper proposes X-Sent-Fuse to combine text and audio for cross-lingual sentiment classification.

## Data & modalities
Text and speech audio. Benchmarks: Sentiment140-style Twitter (1.6M tweets), Amazon product reviews (80,000 samples, star ratings mapped to polarity), mTEDx, and CMU-MOSEAS (~40,000 sentences, continuous -3..+3 labels). Labels normalised to common polarity classes; audio framed and aligned to transcripts.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
DistilHuBERT (and MFCC features) for speech; TextCNN for text. Fusion via Multimodal Transformer Cross-Attentive Gated Fusion (MT-CAG2F): bidirectional cross-attention between modalities, then a sigmoid gate weighting each modality, then a fusion Transformer; degenerates gracefully to text-only when audio is absent (Twitter, Amazon). Classifier BiSRO-Net: BiLSTM-attention trained with Sharpness-Aware Minimization and a "Revolution Optimizer", with contrastive/adversarial alignment losses. In parallel, an ensemble of fine-tuned multilingual encoders labelled "LLMs" (mBERT, XLM-RoBERTa-Base, mT5-Base) with validation-weighted voting and knowledge distillation; final logits combined with a grid-searched coefficient. No generative LLM, RAG or prompting.

## Results (key numbers and metrics)
Accuracy 98.67% (Twitter), 97.89% (Amazon), 97.42% (mTEDx), 98.13% (CMU-MOSEAS); AUC up to 0.996; precision/recall above 97%. Fine-tuned mBERT Macro-F1 97.60-97.85%, XLM-R 97.88-98.12%, mT5 up to 98.45%. Ablations support MT-CAG2F and BiSRO-Net; MFCC outperformed mel spectrograms. 48.7M parameters, 195-417 MB storage, <3.1 GB RAM, 31 ms/sample inference.

## Limitations
No explanation component (weak transparency); needs further compression for edge devices; visual modality not included. (Note: very high accuracies on noisy benchmarks warrant caution.)

## Transferable ideas for the FYP pipeline
- **Fusion:** Bidirectional cross-attention + learned sigmoid gate between modalities (e.g., image embedding vs machine-parameter embedding) to let the model down-weight an unreliable modality.
- **Fusion (robustness):** Design the fusion so it degrades gracefully when a modality is missing (e.g., a fault record with no cut-part image), as MT-CAG2F does.
- **Evaluation:** Report latency/memory footprint alongside accuracy for shop-floor deployment feasibility.
- **Deployment:** Weighted-vote ensembling of several small classifiers as a fast pre-screen before invoking an expensive multimodal LLM.
