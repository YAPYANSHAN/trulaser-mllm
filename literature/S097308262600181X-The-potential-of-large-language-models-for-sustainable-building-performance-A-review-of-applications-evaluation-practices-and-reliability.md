# The potential of large language models for sustainable building performance: A review of applications, evaluation practices, and reliability

- **Citation (IEEE):** A. Ibrahim, M. Alsukkar, Y. Xu, et al., "The potential of large language models for sustainable building performance: A review of applications, evaluation practices, and reliability," *Energy for Sustainable Development*, vol. 95, Art. no. 102104, 2026, doi: 10.1016/j.esd.2026.102104.
- **Domain:** Building energy / HVAC; review of LLM applications (including fault diagnosis)
- **Relevance to FYP (1-5):** 3 - a different domain, but a useful taxonomy of LLM methods (prompting, grounding/RAG, fine-tuning, agents). It also gives evidence that general LLMs fail at fault diagnosis without domain grounding, and offers evaluation/reliability guidance.

## Problem
Building performance simulation, energy audits and assessments are slow, expensive and expert-dependent. The review asks how LLMs can automate these tasks and, unusually, focuses on accuracy, evaluation practice and reliability risks.

## Data & modalities
- A literature review of Scopus, Web of Science and Google Scholar publications from 2022 to 2026.
- Search terms combine LLM/ChatGPT/GPT/Gemini/Llama with building energy modelling, BIM, EnergyPlus, HVAC, fault diagnosis, retrofit and indoor environmental quality (IEQ).
- The reviewed works use text, BIM models, sensor and time-series data, audit reports and code.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Taxonomy dimensions:** (1) prompt engineering and inference-time reasoning (CoT, self-correction, Bayesian-optimised prompts); (2) domain-knowledge integration and grounding (RAG, knowledge bases, BIM/Brick grounding); (3) specialisation via fine-tuning; (4) agentic tool-using architectures (e.g., AutoControl, with two LLM agents generating PI controller code tuned by PSO); (5) applications.
- **Application areas:** BIM querying, energy modelling, retrofit decision support, HVAC fault diagnosis, control and IEQ.
- Links each methodological choice to the accuracy outcomes reported in the studies.

## Results (key numbers and metrics)
Selected results reported from the reviewed studies:
- **HVAC fault diagnosis:** a customised system reached 96.30% accuracy (F1 0.96), vs. 18.4% for GLM-4-9B, 29.40% for ChatGPT-3.5 and 38% for ChatGPT-4o (all untuned).
- **Another fault-detection study:** GPT-4 95.53% vs. GPT-3.5 66.45% accuracy.
- **Agentic RAG (thermal-comfort chatbot):** 94% vs. 82% for standard RAG with Llama 3.1.
- **GPT-3.5 code generation with knowledge-base-augmented prompts:** average R² of 0.95.
- **Overall:** accuracy is highest when outputs are grounded, tool-validated and checked by experts.

## Limitations
- The underlying studies have heterogeneous metrics and test conditions, which limits comparability.
- Many evaluations are single case studies, measuring agreement with experts or exams rather than real-world physical outcomes.
- Reliability risks include hallucination and the need for human-in-the-loop oversight.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** expect weak zero-shot fault diagnosis from general LLMs. Plan domain grounding (RAG over TruLaser manuals and alarm lists), structured prompts and/or fine-tuning, and report the vanilla-vs-grounded gap.
- **Fusion/deployment:** an agentic RAG design with tool calls (SQL over machine tables, an image classifier, a physics calculator) outperformed plain RAG in the reviewed work.
- **Evaluation:** use the review's accuracy taxonomy to justify the choice of metrics. State clearly what each metric does and does not show (e.g., text similarity is not the same as correct root cause). Include expert review as a human-in-the-loop check.
