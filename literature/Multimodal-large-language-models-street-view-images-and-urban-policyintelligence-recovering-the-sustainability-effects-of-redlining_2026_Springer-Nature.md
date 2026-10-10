# Multimodal large language models, street view images and urban policy-intelligence: recovering the sustainability effects of redlining

- **Citation (IEEE):** A. Howell, N. Wu, S. Bagchi-Sen, et al., "Multimodal large language models, street view images and urban policy-intelligence: recovering the sustainability effects of redlining," *npj Urban Sustainability*, vol. 6, art. 79, 2026, doi: 10.1038/s42949-026-00380-7.
- **Domain:** Urban analytics / GeoAI — MLLM-based image measurement for policy evaluation
- **Relevance to FYP (1-5):** 2 — unrelated domain, but its "reason-then-estimate" chained prompting with JSON outputs and self-consistency averaging is a transferable recipe for turning images into quantitative indicators.

## Problem
Cities need granular, low-latency indicators of social vulnerability (poverty) and green infrastructure (tree canopy). Can an MLLM reading Google Street View (GSV) images produce neighbourhood measures that match authoritative statistics and recover known policy effects (1930s HOLC redlining) as well as a conventional segmentation model?

## Data & modalities
>25,000 GSV images in Phoenix, Arizona, aggregated to 1,145 census block groups (CBGs); benchmarks: 2023 ACS poverty share and Google Environmental Insights Explorer tree canopy; HOLC redlining polygons (27 D-grade CBGs); demographic covariates.

## Method
- **GPT-4o** with a chained "reason-then-estimate" prompt: first elicit structured, auditable descriptions of visible street-view features, then map cues to probabilistic indicator values on [0,1]; calibration bands and JSON-only outputs; person-level inferences disallowed.
- **Self-consistency:** five independent runs per image, averaged; image predictions weighted-averaged to CBG level.
- Baseline: ResNet50dilated-PPM segmentation pretrained on ADE20K, pixel shares of aggregated feature classes.
- Evaluation: correlations, bootstrapped R² (500 resamples), ZIP fixed effects, spatial autoregressive models, stacked regression with bootstrap equivalence tests. No fine-tuning or RAG.

## Results
- Poverty: GPT-4o R² = 0.60 vs ResNet 0.29; demographics alone 0.56; GPT-4o + demographics 0.69.
- Tree canopy: GPT-4o R² = 0.40 vs ResNet 0.16. Sustainability index: GPT-4o 0.61 (~double ResNet), 0.66 with demographics.
- Both pipelines reproduce higher poverty / lower canopy in redlined areas; GPT-4o legacy-effect estimates statistically indistinguishable from benchmarks.

## Limitations
Single metropolitan area and year (chosen partly to manage token costs); API cost and time scale linearly with image volume and rate limits apply; MLLM inference partially opaque despite intermediate reasoning; generalisability across cities and imaging conditions untested.

## Transferable ideas for the FYP pipeline
- **LLM reasoning (vision):** two-step prompting — first make the MLLM describe observable cut-edge features (striation pattern, dross height, discolouration, burr) in structured form, then map them to defect probabilities/severity on a fixed scale. This produces an auditable evidence trail.
- **Output control:** JSON-only outputs with calibration bands to keep units consistent and suppress placeholder answers.
- **Robustness:** run N samples per image and average (self-consistency) to stabilise numeric estimates.
- **Evaluation:** benchmark MLLM-derived indicators against a conventional CNN baseline and against measured ground truth (e.g. profilometer roughness) using R² with bootstrap CIs; test incremental value when combined with tabular machine data (analogue of adding demographics).
