# A comprehensive system for detecting and verifying counterfeit images using deep neural networks

- **Citation (IEEE):** P. Ajit Pai, R. Ur Rahman, and D. S. Tomar, "A comprehensive system for detecting and verifying counterfeit images using deep neural networks," *Journal of Computer Virology and Hacking Techniques*, vol. 22, art. 2, 2026, doi: 10.1007/s11416-025-00584-y.
- **Domain:** Digital forensics / image manipulation (morph, deepfake) detection
- **Relevance to FYP (1-5):** 1 - forensic face-morph detection; only generic CNN benchmarking and ensemble-voting ideas transfer.

## Problem
Morphed and deepfake images (enabled by tools such as MidJourney) are used for identity fraud, extortion and misinformation; forensic practitioners lack an integrated system to detect and document such manipulation, and the legal framework (India's IT Act 2000) does not explicitly cover morphing.

## Data & modalities
RGB images (authentic vs morphed/deepfake faces) assembled from diverse real-world sources, with preprocessing and augmentation; image metadata (EXIF-type) is also analysed. Exact dataset sizes are not summarised here.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Six-phase forensic workflow: Identification, Preservation, Collection (metadata, context), Analysis (AI/ML), Documentation, Presentation.
- Metadata analysis plus deep CNN classifiers: EfficientNet, DenseNet121, ResNet50, VGG-16 (transfer learning), with attention/refinement modules (CBAM, Context Refinement Module).
- Final verdict combines predictions of the four models into an averaged confidence score.
- No LLM/VLM is used for detection; LLMs are discussed only as a threat source.

## Results (key numbers and metrics)
- EfficientNet best: train 99.47%, validation 95.96%, test 95.42% accuracy.
- Another model (reported in the text): 91.74% / 91.22% validation/test; VGG-16: train 78.02%, validation 84.64%, test 83.74%.
- Case example: ensemble labelled an image "fake" with average confidence 86.43%.

## Limitations
Relies on established architectures (limited novelty); dataset availability, adversarial evolution of manipulation methods, computational demands and legal gaps are acknowledged; generalisation to unseen generators not fully demonstrated.

## Transferable ideas for the FYP pipeline
- **Vision:** quick baseline benchmark of standard CNN backbones (EfficientNet, DenseNet, ResNet, VGG) with transfer learning for cut-defect image classification before adopting a VLM; EfficientNet is a strong, efficient default.
- **Fusion / LLM reasoning:** average multiple model confidences into a single score and present it as structured evidence to the LLM (e.g., "defect: dross, ensemble confidence 0.86").
- **Deployment / evaluation:** borrow the forensic-style documented workflow (collect, preserve, analyse, document, present) as a template for traceable, audit-ready fault reports, including metadata (timestamp, machine program, sheet ID) attached to each image.
