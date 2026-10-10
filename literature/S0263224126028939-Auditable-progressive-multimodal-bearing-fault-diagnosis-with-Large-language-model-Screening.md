# Auditable progressive multimodal bearing fault diagnosis with Large language model Screening

- **Citation (IEEE):** J. Wang, G. Peng, Y. Chen, et al., "Auditable progressive multimodal bearing fault diagnosis with Large language model Screening," *Measurement*, vol. 292, Art. no. 123183, 2026, doi: 10.1016/j.measurement.2026.123183.
- **Domain:** Industrial fault diagnosis (rotating machinery, vibration) with LLMs
- **Relevance to FYP (1-5):** 4 — industrial fault diagnosis using an LoRA-fine-tuned LLM on textualized measurement features plus multimodal fusion and explicit expert knowledge; not laser cutting or images.

## Problem
Data-driven bearing diagnosis mixes global descriptors, local transients, model capacity and prior knowledge so contributions cannot be verified. Also, prior LLM fault-diagnosis work varies representation, pretraining and parameter count simultaneously, so the benefit of language pretraining is unclear. Windows from the same recording leak between train/test.

## Data & modalities
Four public bearing datasets: CWRU, JNU, MFPT, Paderborn (PU). 2048-sample vibration windows. Modalities: (1) global 24-D canonical time/spectral statistics expanded to an 81-D descriptor and rendered as text; (2) raw local waveform patches; (3) fixed expert-prototype token derived from mechanical sign rules.

## Method
- **Stage 1:** label-free, deterministic measurement-to-language template (blocks B/Q/I/R, values at two decimals) classified by ChatGLM2-6B with LoRA (rank 8, alpha 32, dropout 0.10 on QKV); produces recording-grouped out-of-fold hypothesis.
- **Stage 2:** hypothesis gates mean-one shaft-synchronous modulation (from inner-race load-zone kinematics) on local patches.
- **Fusion:** re-encodes global descriptor and modulated patches; expert-prototype token used only during training (removed at inference).
- Audit tools: sample-level transition analysis (corrections vs regressions), physical/shuffled/zero-content prototype controls, factorial evaluation (pretrained vs random LM x numeric vs textual input) with parameter-matched MLP controls.

## Results
- Fusion corrected more than 60% of Stage 1 errors across the four datasets.
- On MFPT, a 17.84 percentage-point interaction between language pretraining and textualization.
- MFPT: 94.22% accuracy, 93.66% macro-F1; CWRU 100% (saturated); JNU best macro-F1 84.18%; best overall on PU under the common recording-grouped protocol.
- Stage 1 cost: ~6,245.57M total / 1.96M trainable parameters, ~5,494.8 GFLOPs per window.

## Limitations
Hypothesis-conditioning gains are dataset-dependent (MFPT showed a reversal); semantic prototype effect is dataset-dependent; LLM stage is heavy versus small numeric models that perform comparably on some datasets; vibration-only, classification (no generated explanations).

## Transferable ideas for the FYP pipeline
- **Tabular → text:** a fixed, label-free template to serialize machine-database rows (laser power, speed, gas pressure, focus) into LLM-readable text; include no labels to avoid leakage.
- **Fine-tuning:** LoRA on a ~6B open LLM for classification over serialized features is feasible and cheap in trainable parameters.
- **Fusion:** progressive design — tabular screening hypothesis conditions the image/defect analysis, and a final fusion stage may overturn it; log correction vs regression rates.
- **Knowledge:** encode TRUMPF documentation rules (e.g., "dross ↑ when gas pressure low") as fixed prototype tokens/rules and test with shuffled controls.
- **Evaluation:** group splits by job/sheet; ablate pretrained vs random LM and text vs numeric input to justify using an LLM at all.
