# Foundation model-based federated learning for machine fault diagnosis

- **Citation (IEEE):** W. Sun, R. Yan, R. Jin, et al., "Foundation model-based federated learning for machine fault diagnosis," *Chinese Journal of Mechanical Engineering*, vol. 39, Art. no. 100233, 2026, doi: 10.1016/j.cjme.2026.100233.
- **Domain:** Industrial machinery fault diagnosis (bearings/gearboxes) / federated learning with foundation models
- **Relevance to FYP (1-5):** 3 - mechanical fault diagnosis that aligns sensor features with a foundation-model text space (CLIP prompts). The fault-prompt design is directly reusable; federated learning matters less for a single-machine FYP.

## Problem
Individual enterprises have too little fault data, and privacy prevents pooling it. Federated learning (FL) helps, but heterogeneous operating conditions, scarce local data and class imbalance across clients (non-IID) hurt the generalisation of the global model.

## Data & modalities
- **CWRU bearing dataset:** loads of 0-3 hp.
- **PU (Paderborn) bearing dataset:** 14 classes.
- **DDS planetary gearbox bearing dataset:** loads of 0, 3.66 and 10.98 N·m.
- Modalities are vibration signals plus text descriptions of the fault classes (fault prompts).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Fed-FM works as follows:
- Each client's local fault-diagnosis model (a signal encoder) is trained contrastively against the frozen, off-the-shelf **CLIP text encoder**. Signal features are aligned to text embeddings of fault prompts, extending the model's semantic knowledge.
- **Word-class fault prompting:** cryptic class codes (e.g., OR007, IR007, KA04) are renamed with intuitive fault-type words, followed by the class description. This avoids feature collapse in the text encoder.
- An **L2-norm regularisation** on local feature representations aligns marginal distributions and reduces domain shift within and across clients.
- The global model is aggregated FedAvg-style, with no extra communication cost.
- Baselines: Local, FedAvg, FedProx, Scaffold, FedGen, FedAlign and centralised learning.

## Results (key numbers and metrics)
- Highest test accuracy among the compared FL methods on all three datasets in the IID, non-IID-domain and non-IID-random (Dirichlet α = 0.1/0.3/0.6) settings.
- In the IID setting it even surpasses centralised training on CWRU and DDS.
- Gains over FedAlign are largest under high heterogeneity.
- Per-table accuracies are in the paper; CWRU values in the IID setting are close to 100% for all methods.

## Limitations
- Higher storage and compute on clients, which limits use on resource-constrained devices.
- Fixed, hand-written fault prompts cannot self-adjust to diverse, complex fault types.
- Future work: learnable continuous prompts.

## Transferable ideas for the FYP pipeline
- **Fusion/tabular:** align machine-data or image embeddings of TruLaser faults with text embeddings of fault descriptions (CLIP-style contrastive loss). This enables zero- or few-shot matching to fault classes described in the documentation.
- **Text/RAG:** replace cryptic alarm or fault codes with descriptive natural-language class names before embedding. This simple step improves semantic alignment.
- **Deployment:** if multiple TRUMPF machines or sites are involved, FL with a shared text anchor could combine data without sharing raw production logs.
- **Evaluation:** test under non-IID splits (different materials or thicknesses per "client").
