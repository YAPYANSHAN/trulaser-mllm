# MG-CRAG: fusion of multi-granular retrieval evaluators in corrective RAG with weakly supervised fine-tuning

- **Citation (IEEE):** N. Masoumi, O. Davar, and M. Eftekhari, "MG-CRAG: fusion of multi-granular retrieval evaluators in corrective RAG with weakly supervised fine-tuning," *Knowledge and Information Systems*, vol. 68, Art. no. 149, 2026, doi: 10.1007/s10115-026-02778-2.
- **Domain:** NLP: retrieval-augmented generation (RAG), corrective RAG, hallucination mitigation.
- **Relevance to FYP (1-5):** 3 - general-domain QA, but its passage/sentence-level relevance filtering is a direct, cheap upgrade for the FYP's technical-documentation RAG stage.

## Problem
Corrective RAG (CRAG) uses a retrieval evaluator trained on noisy heuristic binary labels, needs hand-set upper/lower thresholds, refines documents at only one granularity ("strips"), and relies heavily on costly web search when retrieval is judged poor.

## Data & modalities
Text only. Short-answer QA benchmarks: ARC-Challenge, PubHealth, PopQA. Retrieval via Contriever (MS MARCO); a small human-labelled guide set plus a manually labelled validation set of question-context pairs (High/Medium/Low relevance).

## Method
- **Weakly supervised labelling (4 stages):** retrieve and pair queries with documents -> embed with T5-GTR (768-D) -> autoencoder with joint reconstruction + classification loss (on the labelled subset) maps to a small latent space -> K-Means (3 clusters) assigns pseudo-labels, validated against human labels.
- **Evaluators:** frozen T5-GTR embeddings + trained residual classification head, giving a 3-class output (no thresholds). Passage-Level Retrieval Evaluator (PLRE) then Sentence-Level Retrieval Evaluator (SLRE) applied sequentially.
- **Inference modes:** strict (High from both), moderate (High from either), lenient (drop only Low); web search is triggered only if fewer than `wsc` High sentences remain; web results filtered by SLRE.
- Dataset-specific re-rankers (MPNet, RoBERTa, Self-RAG scores); generator SelfRAG-LLaMA2-7B with CRAG prompts; ChatGPT-3.5-turbo as query rewriter.

## Results
- ARC-Challenge accuracy 68.85% (reported state of the art); PopQA 59.89% (61.54% with higher web-search rate); PubHealth 75.58% (equal to CRAG; 74.97% when SLRE was applied to web results).
- Lower web-search rate than CRAG on all datasets (about 8.7% on ARC-Challenge).
- Evaluator size 352M + 100M vs CRAG's 738M, with faster inference.
- Combining PLRE+SLRE beats either alone (ablation); best context size is 2-3 sentences for short answers.
- Best mode differs by dataset (moderate for ARC, strict for PubHealth, lenient for PopQA).

## Limitations
Only short-answer benchmarks (no long-form generation); best re-ranker and inference mode must be chosen per dataset; SLRE degrades under domain shift (web text); on PopQA the PLRE underperformed and SLRE was reused for both roles; still needs some manual labels.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** After retrieving TruLaser manual/alarm-handbook chunks, pass them through a small relevance classifier at section level then sentence level so the LLM receives only the 2-3 sentences that matter (e.g., the exact remedy for a nozzle-collision alarm).
- **Data ingestion / labelling:** Label about 100 query-chunk pairs by hand (High/Medium/Low) and pseudo-label the rest with embedding + autoencoder + K-Means. This is a realistic labelling budget for an FYP.
- **LLM reasoning:** Use a 3-class relevance gate in place of a fallback; if no "High" evidence exists, the system should say "insufficient documentation" or query the machine database instead of guessing (replace web search with a DB/SQL fallback).
- **Evaluation:** Report accuracy alongside the fallback rate, tuning a `wsc`-like knob for the accuracy-cost trade-off; measure how context sentence count affects answer quality.
