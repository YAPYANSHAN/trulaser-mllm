# Integrating Large Language Models into Dynamic Network Reconfiguration: A Systematic Review for Sustainable Telecommunication Systems

- **Citation (IEEE):** M. Singh, A. Bindle, P. Singla, et al., "Integrating large language models into dynamic network reconfiguration: a systematic review for sustainable telecommunication systems," *International Journal of Networked and Distributed Computing*, vol. 14, art. 28, 2026, doi: 10.1007/s44227-026-00106-2.
- **Domain:** Telecommunications / network management - systematic review of LLM + RAG
- **Relevance to FYP (1-5):** 2 - different domain and no experiments, but its LLM log-based anomaly detection, root-cause explanation and self-healing loop is a conceptual template for machine-log fault diagnosis.

## Problem
How LLMs, especially within Retrieval-Augmented Generation (RAG) frameworks, can support dynamic reconfiguration of SDN/NFV/6G networks - intent translation, anomaly detection, self-healing, policy optimisation and knowledge-driven automation - and what the trade-offs are versus traditional AI.

## Data & modalities
Literature review (2014-2025) following PRISMA: 716 records from IEEE Xplore, ScienceDirect, SpringerLink and Scopus; 26 duplicates removed; 690 screened; 202 full-text reviewed; 74 studies included. Data types discussed: telemetry logs, alerts, configuration files, policy documents, incident reports.

## Method
Systematic review with quality-assessment criteria. Organises the field into: (1) configuration management and intent translation; (2) anomaly detection and self-healing (LLM ingests real-time telemetry/logs, detects anomalies, explains root cause, generates remediation such as configuration changes, with a feedback loop for continuous learning); (3) reinforcement learning and policy optimisation; (4) knowledge-driven network automation via RAG. Compares LLM vs traditional AI on flexibility, latency, interpretability and scalability, and analyses recurring challenges.

## Results
Qualitative synthesis. Reported examples from reviewed works: LLM-based anomaly classification with corrective suggestions reduced mean-time-to-repair by over 35% in simulated testbeds; fine-tuned BERT log parsers outperformed conventional ML classifiers on noisy/fragmented logs; GPT-3 + Codex prototypes generated CLI patches. Key challenge categories: data scarcity and generalisation, real-time latency, explainability/trust, legacy integration, and inference energy cost.

## Limitations
Narrative synthesis with few quantitative comparisons; many cited results are simulations; telecom-specific; sustainability benefits are rarely quantified (acknowledged by the authors).

## Transferable ideas for the FYP pipeline
- **Data ingestion / text:** treat TruLaser alarm logs, error codes and event histories as semi-structured text that an LLM can parse and correlate with retrieved manual sections.
- **LLM reasoning:** adopt the "detect -> explain root cause -> propose remediation -> human approval -> feedback" loop; capture whether the fix worked to grow a case base for RAG.
- **Text/RAG:** retrieve historical incident reports similar to the current fault as few-shot evidence.
- **Evaluation:** track operational KPIs like MTTR reduction and false-alarm rate, not just accuracy.
- **Deployment:** note latency and energy trade-offs; consider smaller/edge models for real-time alerting and a larger model for offline root-cause reports.
