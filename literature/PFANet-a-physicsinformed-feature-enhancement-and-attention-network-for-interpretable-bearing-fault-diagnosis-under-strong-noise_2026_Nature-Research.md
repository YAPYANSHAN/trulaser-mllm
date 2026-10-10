# PFA-Net: a physics-informed feature enhancement and attention network for interpretable bearing fault diagnosis under strong noise

- **Citation (IEEE):** C. Wang, Y. Li, R. Li, et al., "PFA-Net: a physics-informed feature enhancement and attention network for interpretable bearing fault diagnosis under strong noise," *Scientific Reports*, vol. 16, art. 28095, 2026, doi: 10.1038/s41598-026-61244-9.
- **Domain:** Industrial fault diagnosis — rolling-bearing vibration analysis (physics-informed deep learning)
- **Relevance to FYP (1-5):** 3 — industrial fault diagnosis with physics-based interpretability, but single-modality vibration data, no LLM, and rotating machinery rather than laser cutting.

## Problem
Strong background noise, coupled vibrations and transmission paths mask incipient bearing faults. Signal-processing methods are interpretable but brittle under non-stationary, high-noise conditions; deep networks are accurate but black-box, label-hungry and poorly generalising.

## Data & modalities
Vibration signals from the CWRU (ten-class) and Paderborn University PU (six-class, incl. compound faults) bearing datasets, converted to three-channel time–frequency images via continuous wavelet transform (complex Morlet). Robustness test: Gaussian noise at 6, 3, 0, −3, −6 dB SNR.

## Method
- **Feature Decoupling Enhancement Module (FDEM):** Quadratic Convolution Feature Enhancement Submodule (learnable quadratic convolution to amplify nonlinear transient features) + Physical Feature Decoupling Submodule (Fourier and Hilbert transforms extract impulse/envelope information as interpretable physical indices).
- **Feature Aggregation Module (FAM):** improved residual block with CBAM (local channel–spatial attention) + Swin Transformer shifted-window self-attention (global dependencies).
- **Dynamic joint loss** balancing physics-informed losses and classification loss (multi-task).
- No LLM, RAG or multimodal fusion.

## Results
- CWRU ten-class test accuracy 98.75% vs DenseNet 96.88% and MobileViT 94.79%.
- PU six-class average accuracy 98.68%.
- PU under noise: clean 98.96%; 0 dB 95.69% (DenseNet121 92.42%); −6 dB 88.13% vs ResNet50 81.63%, DenseNet121 83.30%, MobileViT 78.04%. Margin over best baseline grows from 2.15 pp (6 dB) to 4.83 pp (−6 dB).
- Confusion matrices/t-SNE show better class separation; some residual confusion between ball-fault severities and normal vs inner-race.

## Limitations
Laboratory benchmark datasets only; same working conditions within each dataset; cross-domain adaptation under variable conditions and few-shot learning left for future work; physical operators specific to impulsive bearing faults.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** if TruLaser logs include high-rate signals (e.g. drive currents, gas pressure, sensor traces), convert them to CWT scalograms and process with a CNN/Swin encoder; physics operators (FFT/envelope) yield interpretable indices that can be passed to the LLM as textual evidence.
- **Fusion/LLM reasoning:** expose physically meaningful intermediate metrics rather than raw embeddings so the LLM's explanation can cite them.
- **Evaluation:** test diagnostic robustness by injecting controlled noise at multiple SNRs and report degradation curves against baselines.
