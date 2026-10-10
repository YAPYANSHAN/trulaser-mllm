# Acoustic-based fault diagnosis of electric motors using Mel spectrograms and convolutional neural networks

- **Citation (IEEE):** H. Uzel, Y. Ozupak, F. Alpsalaz, et al., "Acoustic-based fault diagnosis of electric motors using Mel spectrograms and convolutional neural networks," *Scientific Reports*, vol. 16, art. 3379, 2026, doi: 10.1038/s41598-025-33269-z.
- **Domain:** Industrial fault diagnosis / acoustic condition monitoring
- **Relevance to FYP (1-5):** 3 - industrial machine fault diagnosis with careful leakage-free evaluation, noise robustness and embedded deployment; acoustic/spectrogram branch could be an extra sensing modality for the laser cutter, but no LLM or multimodal reasoning.

## Problem
Diagnosing electric-motor faults from sound is hindered by limited data, background noise and subtle acoustic differences between operating states; needs an accurate, interpretable, real-time method.

## Data & modalities
Audio: IDMT-ISA-ELECTRIC-ENGINE dataset, three classes (engine_good, engine_broken, engine_heavyload). Converted to Mel spectrograms; acoustic descriptors THD, spectral entropy and SNR computed to characterise states. External-domain test set for generalisation.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Raw audio -> Mel spectrogram -> lightweight CNN (convolution, pooling, batch normalisation, dropout, dense layers).
- Leakage control: file-level splitting, session separation, 5-fold cross-validation, repeated trials.
- Baselines: MFCC-based classical ML, ResNet-18, CRNN, lightweight Transformer classifiers.
- Analyses: noise-robustness across SNR levels, preprocessing sensitivity, feature-importance maps, latency and parameter count on embedded hardware. No LLM.

## Results (key numbers and metrics)
- Test accuracy 99.7%, matching or exceeding ResNet-18, CRNN, Transformer and MFCC baselines at lower computational cost; convergence within about two epochs.
- Stable performance under varying SNR; low-frequency region (Mel bins 0-40) most discriminative, linked to bearing defects, rotor imbalance and load effects.
- Real-time feasible on embedded hardware with low latency and modest parameter count; promising external-domain results.

## Limitations
Validated mainly on one motor type and three coarse classes; data available only on request; transfer learning and multimodal fusion left as future work.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series (new modality):** if microphones or high-rate sensor logs are available on the TruLaser (cutting sound, gas flow noise), convert to Mel spectrograms and classify with a small CNN; outputs become additional evidence for the LLM.
- **Evaluation:** adopt file/job-level splits and session separation to avoid leakage between near-identical cuts; repeat trials and report variance; test under added noise.
- **LLM reasoning:** pass physically interpretable descriptors (spectral entropy, dominant bands) and feature-importance findings to the LLM so explanations reference physical mechanisms.
- **Deployment:** prefer compact CNNs for edge inference next to the machine; measure latency on target hardware.
