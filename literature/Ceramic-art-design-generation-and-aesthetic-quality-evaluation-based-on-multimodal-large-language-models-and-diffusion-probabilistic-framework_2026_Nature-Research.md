# Ceramic Art Design Generation and Aesthetic Quality Evaluation Based on Multimodal Large Language Models and Diffusion Probabilistic Framework

- **Citation (IEEE):** W. Zhao, "Ceramic art design generation and aesthetic quality evaluation based on multimodal large language models and diffusion probabilistic framework," *Scientific Reports*, vol. 16, art. 26758, 2026, doi: 10.1038/s41598-026-55502-z.
- **Domain:** Generative AI for design / computational aesthetics (ceramics)
- **Relevance to FYP (1-5):** 2 - creative-design domain; transferable pieces are KG-augmented MLLM parsing into structured attributes and a multi-dimensional, expert-calibrated quality scorer, not the diffusion generation.

## Problem
Ceramic surface-decoration design depends on subjective artisan expertise with long cycles and homogenisation; there is no domain-specific pipeline that parses design intent, generates styled designs and evaluates their visual quality.

## Data & modalities
Purpose-built dataset of over 21,000 annotated 2D ceramic images across five traditions (about 86% Chinese: celadon, blue-and-white, polychrome enamel, monochrome glaze), with text briefs, reference images and expert aesthetic ratings.

## Method
Three coupled modules. (1) Multimodal semantic parsing: LLaVA-1.5-13B instruction-tuned (15 epochs) on ceramic prompt-response pairs, augmented with a ceramic-domain knowledge graph that resolves vague terms (e.g. linking to specific ware nodes), outputs structured design attributes. (2) Style-conditioned diffusion network: semantic cross-attention injection plus adaptive layer normalisation (AdaLN) for categorical style embedding. (3) Multi-dimensional aesthetic evaluator: separate branches for composition, colour harmony (HSV), texture fineness (GLCM/LBP) and style consistency, combined by attention-weighted adaptive fusion calibrated against expert scores.

## Results
FID 28.35 and IS 10.46, outperforming baselines including Stable Diffusion, DALL-E 3 and ControlNet. Aesthetic evaluator SRCC 0.891 and PLCC 0.903 against expert ground truth. Ablation: removing the semantic parsing module raised FID by 37.3% (largest contributor); multi-dimensional adaptive scoring beat monolithic scorers.

## Limitations
Operates only on 2D imagery; no 3D form, clay-body, glaze chemistry or firing dynamics, so outputs are ideation aids, not manufacturing specifications; dataset dominated by Chinese traditions; aesthetic scores are computational proxies, not holistic judgement.

## Transferable ideas for the FYP pipeline
- **Text/RAG + KG:** use a small domain KG to resolve vague operator language ("rough edge", "bad bevel") to precise defect classes and machine parameters before LLM reasoning.
- **LLM reasoning:** instruction-tune a VLM to output structured attributes (defect type, location, severity, material) from images or text - structured intermediate representations were the most important component here.
- **Evaluation / vision:** decompose cut-quality assessment into separate interpretable dimensions (edge roughness, dross, burr, dimensional/bevel-angle accuracy, discolouration) with dedicated features, fuse with learned weights, and calibrate against expert ratings using SRCC/PLCC.
- **Scope note:** like the paper's material/firing gap, image-only analysis cannot capture process physics - combine with machine-parameter tables.
