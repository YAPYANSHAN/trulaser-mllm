# TeLL-me what you cannot see: a vision-language framework for forensic mugshot augmentation

- **Citation (IEEE):** S. Cavasin, M. Tamiazzo, P. Biasetton, et al., "TeLL-me what you cannot see: a vision-language framework for forensic mugshot augmentation," *Journal on Information Security*, vol. 2026, Art. no. 16, 2026, doi: 10.1186/s13635-026-00231-z.
- **Domain:** Digital forensics / VLM attribute extraction + generative augmentation
- **Relevance to FYP (1-5):** 2 - unrelated domain. Its useful parts are that image enhancement before VLM attribute extraction improves accuracy, that small VLMs can produce structured descriptors, and its generative-augmentation consistency checks.

## Problem
Law-enforcement agencies often have only a few low-quality, outdated mugshots of a person of interest. That limits poster-style descriptors (hair and eye colour, age, marks) and the material available for review. The paper builds a reproducible pipeline and evaluation protocol for VLM-based description and identity-consistent synthetic portraits.

## Data & modalities
Face images (mugshots) gathered via OSINT with poster-style attribute labels (age, colours, marks, etc.). Text descriptors are produced as an intermediate output.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Modular pipeline:
1. Optional image enhancement (three methods compared, including MAXIM in exposure-enhancement mode).
2. Structured attribute extraction with small VLMs: TinyLLaVA (ViT encoder + small LLM via a 2-layer MLP connector) and Qwen2-VL, both at low temperature.
3. Descriptor-conditioned portrait generation with an SDXL-based Stable Diffusion model, including ageing.
4. Identity-consistency checks with re-identification backends (Recognito similarity, DeepFace distance).

Prompt keywords were studied for their effect on generation.

## Results (key numbers and metrics)
- Attribute extraction on original images: TinyLLaVA 82.13%, Qwen2-VL 80.81%. Best is about 83.1% with enhanced input, +2.3 points.
- Qwen2-VL estimates numeric attributes (age) more precisely. TinyLLaVA rounds ages to decades.
- Re-ID (Recognito), same-subject vs. different-subject similarity:

| Pairs | Same subject | Different subject |
|---|---|---|
| Original | 0.719 | 0.499 |
| Original + generated | 0.693 | 0.499 |

## Limitations
- Limited dataset scope and no validation with human subjects.
- Appearance drift across generations and degradation propagating through augmentation levels.
- Demographic bias: some ethnic groups are rendered with lighter skin tones or altered features.
- Enhancement can oversmooth and remove fine details.

## Transferable ideas for the FYP pipeline
- **Vision preprocessing:** test whether enhancement (exposure correction, denoise) of shop-floor cut-part photos improves VLM defect description, while watching for oversmoothing that erases fine burr or striation detail.
- **Vision → structured text:** prompt a small VLM (Qwen2-VL, TinyLLaVA) at low temperature to produce a fixed schema of defect descriptors (type, location, severity, edge features). Pass that schema to the reasoning LLM, and score it per attribute against labels.
- **Data augmentation:** generate synthetic defect images conditioned on text descriptors with diffusion models. Add a consistency check (embedding similarity to the real class) so the synthetic data stays faithful.
- **Evaluation:** report per-attribute agreement and separation statistics (same vs. different class similarity distributions).
