# Comparative Performance of Recent and Prior Large Language Models and Pediatric Residents on Pediatric In-Training Examination Questions

- **Citation (IEEE):** M. J. Kim, J. S. Park, and S. H. Kang, "Comparative performance of recent and prior large language models and pediatric residents on pediatric in-training examination questions," *Scientific Reports*, vol. 16, art. 15849, 2026, doi: 10.1038/s41598-026-44333-7.
- **Domain:** Medical education / benchmarking multimodal LLMs vs humans
- **Relevance to FYP (1-5):** 2 - medical exam benchmark; relevant only as evidence that frontier multimodal LLMs remain weaker on image-based than text-only questions, plus a repeatability-testing protocol.

## Problem
Vision-enabled LLMs perform well on medical exams, but their ability on pediatric image-based questions, their year-over-year progress, and generalisation to non-English (mixed Korean-English) exams are unclear.

## Data & modalities
498 unique questions from 10 pediatric in-training examinations (2016-2023) of a single department; about 22% include medical images; mixed Korean-English terminology; mostly multiple choice (6 short-answer items). Resident scores by training year (R1-R4) as human comparison.

## Method
Six vendor-hosted LLMs via API: recent GPT-4.1, Gemini-2.5-Pro, Claude-4.1-Opus and prior GPT-4o, Gemini-1.5-Pro, Claude-3.5-Sonnet. Standardised prompt template (context, choices, images, question-type instructions, decision/output rules) refined on a held-out exam in August 2025. Each model run in five repeated sessions; repeatability measured with intraclass correlation. Proportion correct (PC) compared with residents, split by text-only vs image-included items. No fine-tuning or RAG.

## Results
Recent LLMs 77.7-78.9% PC vs fourth-year residents 70.1% (all P<0.008); prior models comparable to R4. Text-only items: recent LLMs 80.1-81.0% vs R4 69.6%. On image-included items no LLM surpassed R4, and all models scored lower on image items than on text-only items. Repeatability high (ICC > 0.98) for most models.

## Limitations
Single centre; snapshot of 2025 model versions; possible language-recognition errors with mixed Korean-English items; no error-pattern or reasoning analysis (hallucination, calibration not assessed); only six short-answer items; open-source models not evaluated.

## Transferable ideas for the FYP pipeline
- **Vision / LLM reasoning:** do not rely on a general multimodal LLM alone to read cut-part or defect images - image understanding lags text reasoning even in frontier models; supply image evidence pre-processed by dedicated vision models or converted to text descriptors.
- **Evaluation:** split benchmark results by input type (text/table-only vs image-included questions), run each case multiple times and report repeatability (ICC or agreement) - useful for a fault-diagnosis test set.
- **Evaluation:** compare the system against human operators/technicians of different experience levels as a meaningful baseline, and track performance across model versions.
- **Deployment:** standardised prompt templates refined on a held-out set before final evaluation avoid test-set leakage.
