# A robust natural language text-to-SQL generation framework with dynamic strategies based on LLMs (TriSQL)

- **Citation (IEEE):** X. Su, Y. Gu, P. Wang, et al., "A robust natural language text-to-SQL generation framework with dynamic strategies based on LLMs," *Scientific Reports*, vol. 16, art. 7892, 2026, doi: 10.1038/s41598-026-39128-9.
- **Domain:** NLP / Text-to-SQL (database question answering)
- **Relevance to FYP (1-5):** 4 - the FYP must query structured TruLaser machine-database tables; schema selection + skeleton generation + complexity-aware LLM refinement is a direct recipe for the LLM's tabular-evidence retrieval tool.

## Problem
LLM-based Text2SQL degrades sharply as question complexity grows (large schemas, nested queries, multi-joins) because methods apply a uniform generation strategy; post-hoc fixes are applied uniformly and rarely correct deeper semantic errors.

## Data & modalities
Natural-language questions + relational database schemas. Benchmarks: Spider (dev/test), Spider-DK, Spider-Syn and other variants; PowerSQL, a power-utility benchmark of 3,427 SQL statements covering INSERT/UPDATE/DELETE/CREATE TABLE. Pilot tests on Cypher (Neo4j) and MongoDB pipelines.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Stage 1 - Question-Guided Schema Selector: pretrained encoder embeds question and tables/columns; cross-attention relevance scoring; focal loss for sparse relevant elements; keeps only the most relevant schema.
- Stage 2 - Structure-Aware SQL Generator: hierarchical, skeleton-first decoding for syntactically valid initial SQL.
- Stage 3 - Complexity-Aware SQL Refiner (LLM): estimates complexity of question and initial SQL and selects refinement strategies dynamically, including execution-based correction (execution reward).
- Modules pre-trained separately then jointly fine-tuned with complexity-aware data augmentation. The specific LLM backbone was not identified in the sections reviewed.

## Results (key numbers and metrics)
- Spider test: execution accuracy (EX) 82.2%, exact match (EM) 76.4%; 180 ms inference, 4.0 pp better than RESDSQL and 6.7x faster.
- Spider-DK: EX 62.42 (EM 51.02); Spider-Syn: EX 77.16 (EM 72.24).
- Robustness across complexity levels: average EX 80.5% with 6.0 pp degradation per level (RESDSQL 70.8%, 10.7 pp).
- PowerSQL: 90.8% execution accuracy. Ablation: removing the correction module drops EX to 0.583.

## Limitations
Highly ambiguous questions need disambiguation; adaptation to unseen schemas with few examples; optimises correctness, not query performance; single-turn only.

## Transferable ideas for the FYP pipeline
- **Tabular / text-RAG:** expose the machine database (jobs, alarms, parameter sets, quality results) to the LLM through a Text2SQL tool: first select relevant tables/columns, then generate a SQL skeleton, then refine with execution feedback.
- **LLM reasoning:** run the generated SQL and use errors/empty results as feedback for self-correction before evidence is passed to the diagnosis step.
- **Evaluation:** build a small domain benchmark (like PowerSQL) of operator questions with gold SQL; measure execution accuracy by complexity level.
- **Deployment:** schema pruning keeps prompts short and latency low on large plant databases.
