# Research on intelligent evaluation system of film and television script integrating InternVL 2 and GCSE algorithm

- **Citation (IEEE):** L. Yu, "Research on intelligent evaluation system of film and television script integrating InternVL 2 and GCSE algorithm," *Systems and Soft Computing*, vol. 9, Art. no. 200618, 2026, doi: 10.1016/j.sasc.2026.200618.
- **Domain:** Creative industries / NLP + multimodal evaluation (film script review)
- **Relevance to FYP (1-5):** 2 - unrelated domain, but shows an InternVL 2 multimodal backbone plus expert-aligned, multi-metric scoring with an auto-generated diagnostic report.

## Problem
Reviewing film/TV scripts is manual, slow and subjective. Existing automated tools mostly do surface text analysis and miss narrative structure, plot logic and character-relationship semantics. The author wants a quantitative, multi-dimensional script-quality assessment that agrees with experts.

## Data & modalities
500 film and TV scripts (drama, suspense, comedy, 90-120 min), each with its script text and storyboard images. Five domain experts annotated character-relationship strength, conflict-event positions and plot turning points; each script was labelled three times and the majority label was kept. Split 6:2:2 with 5-fold cross-validation, and 5 repeated runs.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **InternVL 2** (ViT-MLP-LLM architecture) parses scene text and produces latent visual representations. These are fused with the text features.
- A narrative-structure module computes the cosine similarity between adjacent fused scene features (coherence), conflict density and character-relationship features.
- **GCSE** (Gaussian-decayed, gradient-assisted contrastive sentence embedding) strengthens the sentence embeddings. A population-based, gradient-assisted search then sets the metric weights by maximising the Spearman correlation between system scores and expert scores.
- Output: a report with 12 core metrics and revision suggestions.
- Baselines: BERT text classifier, InternVL 2 alone, and TF-IDF with linear regression.

## Results (key numbers and metrics)
- Overall evaluation accuracy 86.7%, 7.2 points above the baseline.
- Plot-hole detection F1 82.3%. Character-relationship consistency correlation 0.79.
- Full model mAP 78.4% / F1 0.82. Without GCSE: 73.8% / 0.77. Without InternVL 2: 65.8% / 0.69.
- 2.8 min per script on average.

## Limitations
- Single author, single (proprietary/domestic) dataset, and no public code.
- The paper says little about how the "latent visual representations" are produced from text.
- Expert labels are subjective. The model is not compared with modern general LLMs used as judges.
- The paper does not include an explicit limitations section.

## Transferable ideas for the FYP pipeline
- **Evaluation / fusion:** learn metric weights by maximising rank correlation (Spearman) with expert ratings. This could set the weights of sub-scores such as dross, burr, kerf or bevel-angle deviation in a cut-quality index so the index matches TRUMPF operator judgment.
- **LLM reasoning / output:** a structured report with a fixed set of core metrics plus actionable "revision suggestions" is a template for the FYP's fault diagnosis plus process-optimisation report.
- **Evaluation:** ablations that remove one modality (VLM vs. text-only) and repeated runs reported as mean ± SD. Use the same protocol to show what images add on top of the machine tables.
- **Vision:** InternVL 2 is an open VLM backbone candidate for local deployment.
