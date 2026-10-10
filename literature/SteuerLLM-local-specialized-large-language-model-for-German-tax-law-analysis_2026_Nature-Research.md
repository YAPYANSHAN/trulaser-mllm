# SteuerLLM: local specialized large language model for German tax law analysis

- **Citation (IEEE):** S. Wind, J. Sopa, L. Schmid, et al., "SteuerLLM: local specialized large language model for German tax law analysis," *Scientific Reports*, vol. 16, Art. no. 21640, 2026, doi: 10.1038/s41598-026-58485-z.
- **Domain:** Legal NLP / domain-adapted LLMs
- **Relevance to FYP (1-5):** 2 - text-only legal domain. Its transferable parts are the method for building a local domain-specialised LLM (synthetic data from RAG, block expansion vs. LoRA) and partial-credit, statement-level evaluation.

## Problem
General LLMs struggle in rule-bound domains that need exact citations, structured argument and numerical precision, such as German tax law. Existing benchmarks use binary or short answers and do not reflect graded, partial-credit exams.

## Data & modalities
Text only.
- **SteuerEx benchmark:** 115 expert-validated questions from real German university tax exams (2016-2024, bachelor and master level). It covers six domains (corporate, income, VAT, fiscal procedure, partnership, fundamentals). Reference solutions are decomposed into point-valued statements, 1,035 points in total.
- **Training data:** 6.3B tokens of German domain text for continued pre-training, plus about 1.5M tax instruction-response pairs. These were synthesised from exam material through a controlled retrieval-augmented pipeline grounded in statutes.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Base model Mistral Small 2409 (24B), expanded to 28B by inserting 8 identity-initialised Transformer blocks ("block expansion", LLaMA-Pro style). The original weights stay frozen. A Ministral 8B variant was also built.
- Two training stages: continued pre-training, then instruction tuning.
- Baseline: LoRA adapters on all linear projections (r = 32, α = 16) under a matched budget.
- **Evaluation:** an LLM-assisted, statement-level partial-credit grader, validated against three human graders. Bootstrap confidence intervals.
- Open release of data, weights and code, with a web demo.

## Results (key numbers and metrics)
- SteuerLLM 28B: 28% ± 2 of maximum points. That is the best result apart from DeepSeek-R1-671B (39% ± 3).
- It outperforms GPT-4o-mini (22%), Gemma-3-27B (23%), Qwen2.5-72B (19%), DeepSeek-R1-Distill-Llama-70B (20%) and its own base Mistral-Small (20%).
- The LoRA variant reaches only 20% ± 2. Block expansion beats LoRA under matched training.
- The automated grader agrees with the averaged human score (Kendall τ = 0.718).
- Average student scores beat every LLM.

## Limitations
- All exams come from a single institution, and that bias carries into the synthetic data.
- Some sparse subdomains are not improved.
- Absolute scores are low.
- Part of the training data is private.
- LLM-as-grader still differs from individual human graders.

## Transferable ideas for the FYP pipeline
- **Text/RAG / data:** generate synthetic Q&A pairs from TRUMPF manuals, fault-code tables and expert notes with a retrieval-grounded pipeline. This creates fine-tuning data for a local diagnostic LLM.
- **LLM fine-tuning:** domain data and adaptation strategy matter more than parameter count. Block expansion beat LoRA here, but at FYP scale LoRA on a small model is still the practical choice. Cite this as a known trade-off.
- **Evaluation:** decompose reference diagnoses into scorable statements (correct defect type, correct root cause, correct parameter and direction, cites correct manual section) for partial credit. Validate the LLM grader against human experts with rank correlation.
- **Deployment:** a local model keeps sensitive machine or company data on-premise.
