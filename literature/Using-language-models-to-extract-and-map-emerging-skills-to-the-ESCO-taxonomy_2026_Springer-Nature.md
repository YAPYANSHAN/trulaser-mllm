# Using language models to extract and map emerging skills to the ESCO taxonomy

- **Citation (IEEE):** A. De Santo, N. Nobani, L. Malandri, et al., "Using language models to extract and map emerging skills to the ESCO taxonomy," *Discover Artificial Intelligence*, vol. 6, art. 1150, 2026, doi: 10.1007/s44163-026-01609-1.
- **Domain:** Labour-market intelligence; NLP entity linking and taxonomy enrichment from online job ads.
- **Relevance to FYP (1-5):** 2 - unrelated domain, but its "embedding retrieval top-k, then constrained LLM re-ranking" pattern for mapping free text onto a fixed taxonomy transfers to mapping operator or alarm text onto a fault-code taxonomy.

## Problem
ESCO lists about 14,000 skills but is static. New skills appear first in online job ads (OJAs). The authors need to (i) extract skills that are new relative to ESCO from multilingual OJAs and (ii) normalise and map them back onto ESCO entries.

## Data & modalities
Text only:
- Eurostat WIH-OJA job ads, over 18 million ads across the 27 EU countries plus the UK in 22-23 languages. Access is subject to an NDA.
- ESCO preferred and alternative labels.
- A multilingual benchmark of 300 sampled ESCO skills with their alternative labels.
- The English "tech" and "house" datasets from prior work.

## Method
- **Extraction:**
  - Country-specific FastText embeddings, chosen by grid search over 160 configurations using a Hierarchical Semantic Similarity metric. The best is SG, dim 100.
  - Top-5 cosine neighbours of each ESCO label become candidates.
  - A lexical-novelty filter (rapidfuzz ratio ≤ 70) keeps only candidates that differ in wording from existing labels.
  - A relevance score S = 0.85·cos + 0.15·freq, plus a 95% cumulative-frequency filter.
- **Validation:**
  - GPT-4 classifies each candidate with contextual framing (a skill definition plus an example ad), few-shot examples, and a forced leading "yes/no" with an explanation. The prompt is deliberately conservative to keep recall high.
  - National experts then review the survivors.
- **Mapping:**
  - Texts are translated to English with DeepSeek v3. This was more stable than multilingual embeddings.
  - Open sentence-embedding models are compared (gte, Qwen3-Embedding, inf-retriever, MiniLM and others) across 13 similarity metrics, including Spearman.
  - The top-3 ESCO candidates with their descriptions go to an LLM, which must choose one of the three.

## Results
- About 70% of extracted candidates were judged valid by experts. Random checks on Italy and the UK found that over 98% of valid skills survived the LLM filter.
- SkiLLink beats prior methods on RP@1, RP@5, RP@10 and MRR on the tech and house datasets.
- Adding LLM re-ranking raised P@1 above the embedding-only baseline:

| P@1 | Tech | House |
|---|---|---|
| Embedding only (baseline) | 60.8 | 66.2 |
| DeepSeek | 62.1 | 69.1 |
| Qwen3-235B | 62.8 | 69.1 |
| Claude 3.5 Sonnet | 64.7 | 70.6 |
| GPT-5-Mini | 67.6 (best) | 69.3 |
| Claude Opus 4.5 | 64.7 | 69.9 |

- Cost and latency per model are reported. The open models give a cost-effective baseline.

## Limitations
- Novelty has no ground truth, so extraction is judged qualitatively.
- There is a single expert per country.
- Performance varies across languages, and low-resource languages do worse.
- The deterministic top-1 mapping has no confidence estimate.
- Access to the data is restricted.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** map free-text machine messages, operator notes or TRUMPF manual passages onto a controlled fault taxonomy in two steps: dense-embedding retrieval of the top-k candidate fault codes, then constrained LLM selection among only those k, with their descriptions. This keeps recall high and limits hallucinated labels.
- **Data ingestion:** add a lexical-novelty plus frequency filter to surface new fault phrases that are missing from the taxonomy, so it can be extended.
- **LLM reasoning:** force a machine-readable leading token ("yes/no", or a code) and add a short justification. Bias the prompt towards recall when a human reviews the output afterwards.
- **Evaluation:** benchmark several embedding models and similarity metrics instead of assuming cosine. Report P@1, Recall@k and MRR, and give cost and latency per LLM to justify choosing an open versus a proprietary model.
- **Deployment:** translating text to one language before embedding can stabilise retrieval over German/English TRUMPF documentation.
