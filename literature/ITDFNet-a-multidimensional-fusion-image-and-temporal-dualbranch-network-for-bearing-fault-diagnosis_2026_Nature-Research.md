# ITDFNet: a multi-dimensional fusion image and temporal dual-branch network for bearing fault diagnosis

- **Citation (IEEE):** S. Cai and Y. Zhang, "ITDFNet: a multi-dimensional fusion image and temporal dual-branch network for bearing fault diagnosis," *Scientific Reports*, vol. 16, art. 16596, 2026, doi: 10.1038/s41598-026-47235-w.
- **Domain:** Industrial fault diagnosis (rotating machinery, vibration signals)
- **Relevance to FYP (1-5):** 3 - industrial fault diagnosis with signal-to-image plus temporal dual-branch fusion; no LLM, but directly reusable for machine time-series channels.

## Problem
1D vibration-feature methods have limited representational power, while 1D-to-2D image conversions (e.g., GAF) suffer information loss, heavy computation and poor feature separability; models also degrade under strong noise.

## Data & modalities
CWRU bearing dataset (ten fault classes) and UCONN gear dataset (public, IEEE DataPort / Figshare). Single physical modality (vibration) represented in two views: a fused 2D image and the 1D time sequence. Noise robustness tested by adding white Gaussian noise at SNR -8, -6, -4, -2, 0 dB.

## Method
Dual-branch network. **Image branch:** the original signal matrix, a Time Gramian Matrix (TGM, emphasising periodic impacts) and a newly proposed Structural Gramian Matrix (SGM = X X^T after phase-space reconstruction, encoding impact strength, resonance decay and fault period as block textures) are stacked into a multi-channel image and processed by a CNN with a dual fusion attention (DFA) block. **Temporal branch:** models the Gram-denoised original sequence to keep time-varying information. Features from both branches are fused for classification. Ablations remove DFA, structured Gram images and each branch. No LLM/VLM.

## Results
100% accuracy and F1 on CWRU and UCONN (clean). Only 0.33 M parameters and 3.88 ms inference, lower than ResNet18/VGG19/AlexNet. Under noise (Table 5), accuracy at -8 dB was 97.56% (about 14.92 points above the next-best MRCFN); from 0 dB to -8 dB the model dropped only 2.44 points vs 16.64 (ECA-Net), 22.80 (Swin-FFRN) and 13.94 (MRCFN). Versus Swin-FFRN: +8.44% accuracy under strong noise with 29 M fewer parameters. t-SNE shows clearer class separation.

## Limitations
Validated only on benchmark lab datasets with balanced classes; authors note imbalanced/minority-fault data and edge-device resource limits as open issues; synthetic Gaussian noise only.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** if the TruLaser logs contain sensor traces (laser power, gas pressure, axis drives, cutting-head distance), encode windows as Gramian images (TGM/SGM) plus a raw temporal branch to produce a compact fault embedding or class for the LLM.
- **Fusion:** dual-view (image-like + sequence) fusion with attention is a lightweight alternative to sending raw signals to an MLLM; the classifier output and confidence can be passed as evidence text to the LLM reasoning stage.
- **Evaluation:** adopt SNR-sweep robustness testing and parameter/latency reporting for any tabular or signal model.
- **Deployment:** 0.33 M-parameter scale shows such encoders can run on edge hardware next to the machine.
