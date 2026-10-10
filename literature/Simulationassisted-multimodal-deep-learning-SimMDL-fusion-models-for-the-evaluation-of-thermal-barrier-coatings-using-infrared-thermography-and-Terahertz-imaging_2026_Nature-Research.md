# Simulation-assisted multimodal deep learning (Sim-MDL) fusion models for the evaluation of thermal barrier coatings using infrared thermography and Terahertz imaging

- **Citation (IEEE):** S. K. Kunji Purayil, S. Aroliveetil, A. Chaturvedi, et al., "Simulation-assisted multimodal deep learning (Sim-MDL) fusion models for the evaluation of thermal barrier coatings using infrared thermography and Terahertz imaging," *Scientific Reports*, vol. 16, Art. no. 1540, 2026, doi: 10.1038/s41598-025-31783-8.
- **Domain:** Industrial non-destructive evaluation (NDE) / materials characterisation, multimodal deep learning
- **Relevance to FYP (1-5):** 3 - industrial multimodal sensor fusion and simulation-augmented training for quality evaluation of manufactured parts. It has no LLM, but the data-augmentation and fusion ideas transfer.

## Problem
Thermal barrier coatings (TBCs) on turbine and aerospace parts need accurate NDE. Infrared thermography (IRT) is sensitive to surface emissivity and has limited depth. Terahertz (THz) imaging is noisy and has poor spatial resolution. There is little experimental data covering varied coating properties. The goal is to predict several topcoat properties at once from fused IRT and THz data.

## Data & modalities
- Pulsed IRT temporal thermal profiles and THz reflection time-domain signals, both 1D temporal signals.
- Experimental data from 4 newly coated samples (topcoat 24-120 µm).
- About 3,000 physics-based simulations: thermal conductivity and heat capacity varied by ±5% and thickness by 20-200 µm. THz propagation was simulated in COMSOL Multiphysics.
- Targets: thermal conductivity k, heat capacity ρCp, topcoat thickness and refractive index n.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Two fusion networks: (1) a 1D-CNN and (2) an LSTM with attention. Each fuses IRT and THz feature streams for multi-output regression.
- Training sets compared: simulation-only vs. simulation + experimental data.
- Compared against single-modality models and conventional parameter estimation.
- No LLM or VLM is used.

## Results (key numbers and metrics)
LSTM+Attention trained on simulation + experimental data gives these MAPE values across the four samples:

| Property | MAPE |
|---|---|
| Thermal conductivity | 2.06-4.43% |
| Heat capacity | 2.05-3.57% |
| Thickness | 1.75-11.53% |
| Refractive index | 0.27-1.05% |

- LSTM+Attention beats the 1D-CNN on all properties.
- Adding experimental data to simulation data clearly improves accuracy.
- Fusion beats single-modality models and conventional estimation.

## Limitations
- Only 4 experimental samples, so this is a proof of concept.
- Simulation approximations add error.
- Service conditions and material compositions are limited.
- Degraded and aged coatings and varied bond-coat thickness are left to future work.

## Transferable ideas for the FYP pipeline
- **Data ingestion / augmentation:** when real TRUMPF defect data is scarce, generate synthetic or simulated samples and mix them with the few real samples. Here the mix gave much better accuracy than simulation alone. For laser cutting this could be physics-based kerf, heat-input or bevel-geometry models, or synthetic defect images.
- **Fusion:** complementary sensors cover each other's blind spots, as IRT (surface) and THz (depth) do here. Similarly, cut-part images show surface defects while machine tables show process causes. Use a late-fusion multi-output model to predict several quality attributes at once (e.g., roughness, dross height, bevel-angle error).
- **Tabular/time-series:** LSTM+attention works for temporal signals. Attention weights can be passed to the LLM as interpretable evidence.
- **Evaluation:** report per-sample MAPE for regression targets, and ablate single-modality against fused models.
