# Bias and Fairness in Vision-Language Models and Large Language Models: A Survey on South Asian Festival Representations

- **Citation (IEEE):** N. Sarmah and R. Bhattacharyya, "Bias and fairness in vision-language models and large language models: a survey on South Asian festival representations," *International Journal of Data Science and Analytics*, vol. 22, art. 187, 2026, doi: 10.1007/s41060-026-01162-1.
- **Domain:** Responsible AI / cultural informatics / bias in LLMs and VLMs (survey)
- **Relevance to FYP (1-5):** 1 - cultural-bias survey with no industrial content; only general lessons on VLM "semantic averaging" toward common knowledge and on evaluation metrics apply.

## Problem
AI question-answering and visual-QA systems may misrepresent or stereotype cultural practices; there is no consolidated survey of bias/fairness detection for both LLMs and VLMs with a focus on South Asian festivals.

## Data & modalities
Literature survey (no new dataset). A statistical objective survey (SoS) of publications 2021-2025 retrieved with keyword sets (QA, VQA, culturally-aware LLMs/VLMs, South Asian festivals, cultural informatics), plus a subjective review of models, metrics and benchmark datasets. Covers text (QA) and image+text (VQA) settings.

## Method
Survey methodology: keyword-driven search and article-database analysis showing publication trends; subjective analysis along three axes - (a) models (e.g. GPT-family LLMs; CLIP-ViT, LLaVA, BLIP-2, mCLIP, CultureCLIP among VLMs), (b) metrics (e.g. LAVE accuracy, VLStereoSet score, embedding-based scores) and (c) benchmark QA/VQA datasets. Includes an illustrative probe of GPT-5.2 Instant with an image of festival leaves.

## Results
Robust upward trend in bias/fairness research on VLMs and LLMs over 2021-2025. No QA or VQA dataset is dedicated to South Asian festivals. Cited findings: GPT-3.5 shows high bias rates for South Asian cultural stereotypes; CLIP-ViT shows an accuracy gap of over 10% for Indian cultural elements versus Western ones. The GPT-5.2 probe confused a specific local ceremony (Goru Bihu) with a more common practice - "semantic averaging" driven by geographic bias.

## Limitations
Narrow cultural scope; mostly descriptive survey with no experiments beyond an anecdotal example; dependent on keyword search coverage; no quantitative meta-analysis.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** general VLMs default to "popular" knowledge; for a niche machine (TruLaser 3000 Bevel Cut), they will likely generalise to generic laser-cutting advice. Ground answers in the machine's own documentation and data (RAG / knowledge injection) rather than relying on pre-training - the paper's "culturally grounded" argument maps to "domain-grounded".
- **Evaluation:** include test cases where the specific TRUMPF behaviour differs from common laser-cutting wisdom to detect such semantic averaging.
- **Data ingestion:** build a small domain-specific QA/VQA benchmark with expert collaboration, mirroring the gap the paper identifies.
