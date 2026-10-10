# Exploring the integration of large language models in industrial test maintenance processes

- **Citation (IEEE):** J. Liu, L. Lemner, L. Wahlgren, et al., "Exploring the integration of large language models in industrial test maintenance processes," *The Journal of Systems and Software*, vol. 242, Art. no. 113049, 2026, doi: 10.1016/j.jss.2026.113049.
- **Domain:** Software engineering / software test maintenance; industrial case study (Ericsson AB).
- **Relevance to FYP (1-5):** 2 - Software rather than machine domain, but it is an industrial deployment study of a RAG + multi-agent (ReAct) LLM system with an on-premise open model, recall-oriented evaluation and practitioner validation, all of which carry over.

## Problem
Test maintenance (adding/modifying/removing tests as code evolves) is costly and under-automated. The study asks (RQ1) what triggers maintenance, (RQ2) what actions LLMs/agents can take and what must be considered when deploying LLMs in industry, and (RQ3) whether a multi-agent LLM can predict which tests need maintenance after a code change.

## Data & modalities
Text/code only. Exploratory part: literature reviews, 5 interviews (8 participants), survey (29 respondents) at Ericsson. Tool study: confidential Java microservice repository, 54 commits (32 with test updates, 22 without), 634 code changes as git diffs (context extended from 3 to 9 lines).

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
LangChain multi-agent architecture with ReAct (Thought-Action-Observation, max 3 iterations, 300 s/prompt, format-reminder retries). Planning agent coordinates: test maintenance agent (calls a code summarizer agent, then an LLM instance decides if maintenance is needed) and test localization agent (RAG over test code via bge-m3 embeddings + FAISS). Two variants: RAG over raw test code vs. over LLM-generated natural-language test summaries. LLM: Qwen2.5-32B-Instruct, chosen under company approval constraints; no fine-tuning. Agent memory printed for explainability.

## Results (key numbers and metrics)
- 44 maintenance triggers identified (37 low-level changes + 7 high-level process decisions).
- Commits with updates: summary-based prototype recall 0.676, precision 0.275, accuracy 0.911, F1 0.391, F2 0.523; raw-code prototype recall 0.412, precision 0.213, accuracy 0.908, F1 0.281, F2 0.347.
- Commits with no updates: summary prototype averaged 5.5 FPs/commit; raw-code prototype did better here.
- Developer review: of 38 FPs, 14 were actually correct (missed by developer or dataset), 10 more were useful suggestions. Typical commit: ~5 TP, ~3 FN out of ~8 updated tests; responses in <30 s.

## Limitations
Single repository, single language, small dataset; no baseline comparison; ground truth assumes co-change within commit (labeling errors found); low precision; authors judge it not trustworthy for sole reliance; data confidential.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** Index LLM-written natural-language summaries of documents/records, not raw content - summaries improved recall from 0.41 to 0.68. Analogous: summarise TruLaser alarm logs or parameter tables into text before embedding.
- **LLM reasoning:** Planner + specialist agents (e.g., a tabular-query agent, image-defect agent, manual-retrieval agent) under ReAct with iteration/time limits.
- **Evaluation:** Use F2 when missed faults are costlier than false alarms; have a domain expert re-adjudicate false positives, since ground truth may be incomplete.
- **Deployment:** Consider on-prem open models (Qwen2.5) for confidential machine data; position output as advisory with human oversight ("pair technician").
