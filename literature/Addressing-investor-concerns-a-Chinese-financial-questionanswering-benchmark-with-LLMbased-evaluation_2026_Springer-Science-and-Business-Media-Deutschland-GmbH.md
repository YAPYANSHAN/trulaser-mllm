# Addressing Investor Concerns: A Chinese Financial Question-Answering Benchmark with LLM-Based Evaluation

- **Citation (IEEE):** Y. Gan, Y. Tao, J. Mo, et al., "Addressing investor concerns: a Chinese financial question-answering benchmark with LLM-based evaluation," *EPJ Data Science*, vol. 15, art. 6, 2026, doi: 10.1140/epjds/s13688-025-00601-6.
- **Domain:** Financial NLP / document QA / retrieval-augmented generation
- **Relevance to FYP (1-5):** 3 - different domain, but a careful study of RAG over long, table-heavy PDFs and of LLM-as-judge reliability, both directly applicable to querying TRUMPF manuals.

## Problem
Chinese financial QA lacks high-quality datasets. Answering investor questions requires locating evidence in long annual-report PDFs with complex tables and repetitive content.

## Data & modalities
CFQA: >13,000 real investor questions with human-annotated answers and the PDF page number containing the answer, from 516 annual reports of Chinese listed companies. Text + tables in PDF. Two splits: Year-Based Split (train 2019-2021, test later; 9183/1327/3065) and Company-Based Split (unseen companies). Two tasks: Financial Report QA and Page Retrieval.

## Method
Retrievers at page level: sparse BM25, dense BGE-M3, hybrid BM25+dense, and BGE-Reranker-v2-m3 cross-encoder (pages split into up to six 480/80-character snippets, max-score aggregation). Retrieval metrics: NDCG, Hit@K, Recall@K. QA: BM25 top-5 pages fed to LLMs (DeepSeek 3.2, GPT-5-mini, Qwen2.5-7B/14B, Qwen3-30B-A3B, Qwen3-235B-A22B) and ChatPDF. Answers graded by LLM-as-judge (GPT-4o, DeepSeek-V3) with a step-by-step correctness prompt; judge validated against human labels. Prompts provided in appendix.

## Results
BM25 beat dense, hybrid and reranked pipelines on all retrieval metrics (e.g. NDCG@20 0.516 YBS / 0.533 CBS), yet absolute retrieval remains moderate. Reranking BM25 candidates hurt ordering. LLM judges: Cohen's kappa 0.8495/0.8433 (GPT-4o, CBS/YBS) and 0.8199/0.8417 (DeepSeek-V3), macro F1 >0.91. DeepSeek 3.2 and GPT-5-mini best (auto content score ~0.64); Qwen models of all sizes scored similarly lower because of "lazy" answers lacking units/context.

## Limitations
Retrieval is the main bottleneck; no query rewriting or expansion; vague temporal references in questions unresolved; Chinese-only financial domain; text-only (no image modality).

## Transferable ideas for the FYP pipeline
- **Text/RAG:** do not assume dense embeddings win - for technical manuals with repetitive tables and exact codes (alarm numbers, parameter names, nozzle types), benchmark BM25 vs dense vs hybrid; page-level indexing with page citations gives evidence traceability.
- **Evaluation:** build a small gold QA set from TRUMPF documentation with page labels; report Hit@K/Recall@K/NDCG for retrieval separately from answer quality.
- **LLM reasoning / evaluation:** LLM-as-judge validated with Cohen's kappa against a human-labelled subset is a cheap, defensible way to score diagnosis outputs.
- **LLM reasoning:** enforce answer templates (units, parameter names, evidence) to avoid terse "lazy" answers from smaller open models.
