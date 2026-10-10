# Boosting Large-Language Models for Fact-Checking: Leveraging Verbalized Tabular Data as Evidence

- **Citation (IEEE):** S. T. Luu, T. Vo, V. Tran, et al., "Boosting large-language models for fact-checking: leveraging verbalized tabular data as evidence," *International Journal of Data Science and Analytics*, vol. 22, art. 109, 2026, doi: 10.1007/s41060-025-00998-3.
- **Domain:** NLP / table reasoning / automated fact-checking
- **Relevance to FYP (1-5):** 3 - not industrial, but directly addresses how to feed structured tables to LLMs (table-to-text verbalisation + raw table in prompt), which is a core problem for the machine-database branch of the FYP.

## Problem
LLMs reason well over text but struggle with tabular evidence (numeric reasoning, row/column comparisons). Fact-checking claims against tables should work with little or no training data.

## Data & modalities
Tables + textual claims. Table-to-text training data: QTSUM and SCIGEN. Fact-checking evaluation: TabFACT (Wikipedia), SCITAB (scientific) and PubHealthTAB (health); labels such as support / refute / not enough information.

## Method
TabV4FC: (1) fine-tune TAPEX (BART-based table pre-training via neural SQL execution) for table-to-text generation to produce a natural-language description of the table; (2) zero-shot prompt an LLM with the claim, the table rendered as text (grid format) and the generated description to output a veracity label. LLMs: Qwen2.5-14B/32B/72B-Instruct, Llama-3.3-70B and DeepSeek-R1-Distill (Llama-70B, Qwen-32B). Ablations remove the table or the description. Compared with TART and ProTrix.

## Results
Fine-tuned TAPEX: BERTScore 90.57 (QTSUM) and 84.56 (SCIGEN). Qwen2.5-72B with TabV4FC was best overall, F1-macro 45.20% (SCITAB), 57.35% (TabFact) and 58.60% (PubHealthTab); competitive with TART and ProTrix in zero-shot. For Llama-3.3-70B and Qwen2.5 models, removing the description hurt more than removing the table on SCITAB and TabFact - the verbalised summary contributed more than the raw table. DeepSeek-distilled models showed large F1-micro/macro gaps and depended more on the raw table for PubHealthTab. Inference about 4 s per question (TAPEX + Qwen2.5-72B).

## Limitations
The table-to-text module misses latent information, especially numerical values and computed comparisons across rows/columns; only zero-shot prompting; advanced prompting (self-prompting, plan-then-reason) left to future work; absolute scores remain moderate.

## Transferable ideas for the FYP pipeline
- **Tabular ingestion:** for each machine-database record (job parameters, alarms, sensor summaries), generate a short natural-language verbalisation (template-based or a table-to-text model) and pass both the compact table and its description to the LLM.
- **Tabular reasoning:** because verbalisers miss numeric comparisons, precompute derived facts in code (e.g. "laser power 12% below recipe value", "alarm X occurred 5 times in last 2 h") instead of asking the LLM to compute them.
- **Evaluation:** replicate the ablation (table only / description only / both) on TruLaser data to justify the chosen serialisation.
- **LLM reasoning:** frame diagnosis hypotheses as claims verified against tabular evidence (support / refute / not enough info) for evidence-based outputs.
