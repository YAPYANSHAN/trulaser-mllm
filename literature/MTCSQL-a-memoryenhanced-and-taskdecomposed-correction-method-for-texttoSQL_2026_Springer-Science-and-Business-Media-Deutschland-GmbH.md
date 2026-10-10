# MTC-SQL: a memory-enhanced and task-decomposed correction method for text-to-SQL

- **Citation (IEEE):** T. Zhao, H. Zhang, Y. Jiang, et al., "MTC-SQL: a memory-enhanced and task-decomposed correction method for text-to-SQL," *International Journal of Data Science and Analytics*, vol. 22, Art. no. 101, 2026, doi: 10.1007/s41060-025-00995-6.
- **Domain:** NLP / databases: LLM-based text-to-SQL with retrieval augmentation and self-correction.
- **Relevance to FYP (1-5):** 4 - not industrial, but the FYP must let an LLM query structured TruLaser machine-database tables; this gives a concrete, validated text-to-SQL + hybrid-RAG + execution-feedback recipe.

## Problem
LLMs generating SQL for complex, multi-table, ambiguous queries suffer from limited schema/context understanding, weak structural control and no error correction, giving syntax errors, wrong joins or hallucinated columns.

## Data & modalities
Text (natural-language questions) + relational database schemas and content. Spider (10,181 questions, 5,693 SQL, 200 databases, 138 domains; 8659 train / 1034 dev / 2147 test) and BIRD (12,751 question-SQL pairs, 95 databases, >33 GB, 37+ domains, external-knowledge hints).

## Method
Four stages, prompting only (no fine-tuning), with GPT-4 or Codex Davinci as the generator:
1. **Multi-source memory:** historical validated (question, SQL, valid flag, timestamp) pairs + schema information; only SQL that passes validation is written back, so memory grows over time.
2. **Hybrid retrieval:** dense vector search (inner product with locally quantised vectors) + BM25 keyword search (k1 = 1.5, b = 0.75) over history and schema, merged by Reciprocal Rank Fusion (k = 60).
3. **Dynamic task decomposition:** complexity score = weighted sum of #tables, #predicates, #columns and token-field alignment entropy; thresholds pick 1, 2 or more sub-tasks; schema elements become roles (main entity, join, filter, aggregation, ordering) in a DAG, topologically ordered.
4. **Recursive generation and correction:** each sub-SQL is checked for syntax (parser), logic (schema consistency + intent alignment) and execution (run against the DB); failures trigger correction loops before assembly.

## Results
- Spider dev: EM 80.6%, BLEU 76.7 (RESDSQL 80.5 / 72.0). Spider test: EM 75.0%, EX 80.2%, BLEU 77.0 (Codex variant has higher EM 78.7%, which the authors attribute to EM's string-matching bias).
- BIRD dev EX 64.13% / VES 60.45%; BIRD test EX 65.05% / VES 61.74%.
- Ablation (Spider dev, EM/EX/BLEU): full 80.6/82.1/76.7; w/o decomposition 75.4/77.0/72.3; w/o memory retrieval 77.6/79.1/73.8; w/o correction 78.9/76.2/75.0.
- Retrieval: Top-10 recall 94.88% (schema) and 95.05% (history).
- CREATE-statement schema formats outperform Table(Column) format.
- Latency: 2.06 s average (3.02 s for complex queries) vs 1.59 s without decomposition.

## Limitations
Depends on quality and coverage of historical query logs and schema annotations (weak in new/low-resource domains); correction loops add latency; no multi-turn dialogue or schema evolution handling; relies on proprietary GPT-4.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** Expose the TruLaser tables (jobs, alarms, parameters, maintenance) to the LLM as CREATE TABLE statements with column comments (units, alarm-code meanings).
- **Text/RAG:** Use hybrid BM25 + vector retrieval with RRF. BM25 catches exact alarm codes, part numbers and parameter names that embeddings miss; apply this to both schema and manuals.
- **LLM reasoning:** Decompose a diagnosis question ("why did dross increase on 15 mm steel last week?") into sub-queries (filter jobs -> join alarms -> aggregate parameters) and validate each by executing it before the LLM reasons over results.
- **Memory:** Store validated question-SQL pairs as few-shot examples so the system improves with engineer use.
- **Evaluation:** Use execution accuracy (not string match) for the SQL tool, plus a small hand-built set of FYP questions with gold SQL.
