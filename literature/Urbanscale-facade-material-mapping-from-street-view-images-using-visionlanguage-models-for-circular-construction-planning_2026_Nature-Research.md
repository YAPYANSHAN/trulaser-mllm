# Urban-scale facade material mapping from street view images using vision–language models for circular construction planning

- **Citation (IEEE):** D. Raghu, I. Armeni, and C. De Wolf, "Urban-scale facade material mapping from street view images using vision–language models for circular construction planning," *Scientific Reports*, vol. 16, art. 20691, 2026, doi: 10.1038/s41598-026-51028-6.
- **Domain:** Built environment and circular economy; VLM-based material classification from street-view images.
- **Relevance to FYP (1-5):** 3 - a different domain, but it is a clean template for a "segment, then VLM-classify with a constrained prompt, then expert-verify" vision pipeline with cost accounting. That pattern maps directly onto classifying cut-part defects.

## Problem
Circular-economy planning and retrofit decisions are blocked by a lack of reliable building-level data on facade material, condition and style. This is especially true in low-income, data-scarce cities. Manual surveys and supervised, city-specific models are costly and hard to scale.

## Data & modalities
- Street-view images from public sources such as Google Street View, covering six cities: Zurich, San Francisco, Melbourne, Mumbai, Cape Town and Rio de Janeiro.
- Grounded-SAM was run over 57,918 images.
- 9,254 high-confidence facade images went to GPT-4V, and 9,056 outputs were manually validated for scoring.
- Category vocabularies come from a literature review and are specific to each city.
- The authors release the Global Building Facade Dataset.

## Method
1. **Facade isolation.** Grounded-SAM (Grounding DINO with the text prompt "building facade", then SAM masks) selects the dominant facade by confidence and area. Only images with logit > 0.8 are kept; about 15% were excluded.
2. **Attribute inference.** The masked facade goes to GPT-4V through the API with a structured prompt that has three parts:
   - "specific" prompts that force an answer from a predefined category list (material; condition Poor/Fair/Good; style; proxy score Low/Medium/High), with an explicit "other" option;
   - "flexible" prompts that ask for explanatory observations;
   - instruction prompts that help human verifiers.
3. **Verification.** Domain experts check every output against a rubric. Grounded-SAM output is scored with a point system for identification and coverage.
4. **Outputs.** City-specific visual proxies (seismic, energy retrofit, flood, greening, heritage), mapped in QGIS.

There is no fine-tuning and no RAG.

## Results
- Grounded-SAM accuracy: 91.32-98.60% across cities.
- GPT-4V attribute accuracy: 72% (Melbourne) to 89% (Mumbai).
- Composite accuracy (mean of Grounded-SAM and GPT-4V): 84.66% (San Francisco) to 90.30% (Cape Town); mean 87.70%.
- Condition assessment was near-perfect in Rio de Janeiro and Cape Town, where wear is clearly visible. It was weaker in Melbourne, where variations are subtle and modern composite materials are common.
- Of 386 upstream-misidentified images, GPT-4V returned no response for 267. This limited the spread of upstream errors.
- Cost: about $337.40 and just over 3 hours per 1,000 images, including $100 of GPT-4V API, $100 of expert QA and a one-time $1,000 of hardware.

## Limitations
- Accuracy depends on expert annotation and subjective categories; there is no inter-annotator agreement.
- Street-view images are often outdated, low-resolution or occluded.
- Materials that look alike (composites) are hard to tell apart.
- The workflow is a screening tool, not a replacement for domain models.
- It relies on a proprietary GPT-4V API.

## Transferable ideas for the FYP pipeline
- **Vision:** crop or segment the part or cut edge first (an open-vocabulary detector plus SAM, prompted with "cut edge" or "burr"), then send only the masked region to the VLM. This cuts background confusion, and upstream confidence thresholds filter out bad images.
- **LLM reasoning (prompting):** use a hybrid prompt. A constrained categorical field (defect type from a fixed taxonomy, severity Low/Medium/High, "other") gives parseable output. A free-text "explanation" field gives the evidence trail for human verification.
- **Evaluation:** score each stage separately (segmentation vs VLM classification) and combine them. Use a points-based verification rubric. Report accuracy per condition class, since subtle defects will score lower, as Melbourne did.
- **Deployment:** report cost and time per 1,000 images (API, GPU, expert QA) to justify feasibility in the FYP report.
