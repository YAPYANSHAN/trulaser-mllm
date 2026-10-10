# Starmate: A Lightweight AI Assistant for Autism Caregivers Developed and Evaluated Through a User-Centered Mixed-Methods Framework

- **Citation (IEEE):** Z. Li, X. Liu, T. Chen, et al., "Starmate: A lightweight AI assistant for autism caregivers developed and evaluated through a user-centered mixed-methods framework," *Journal of Medical Systems*, vol. 50, Art. no. 106, 2026, doi: 10.1007/s10916-026-02433-x.
- **Domain:** Healthcare NLP / domain-specific conversational LLM
- **Relevance to FYP (1-5):** 3 - unrelated domain, but it is a complete small-LLM system (LoRA fine-tune of Qwen2.5-1.5B + knowledge-graph RAG via LightRAG + query router) evaluated with LLM-as-judge and human experts. Its architecture is a template for a local, privacy-preserving technical assistant.

## Problem
Caregivers of children with autism face unreliable online advice. General LLMs hallucinate, give generic answers that are hard to act on, and lack empathy. The authors want a lightweight, privacy-conscious assistant that gives accurate, empathetic, hands-on guidance.

## Data & modalities
Text only.
- Requirements from interviews (n = 13) and a Kano survey (n = 60). "Hands-on guidance" came out as a must-have.
- Fine-tuning corpus from parent forums (Tieba, QQ groups) plus model-distilled expert-style answers.
- An expert-vetted clinical knowledge base turned into a knowledge graph.
- ASDP-120 test set of 120 real parent questions, 5 of them with typos.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
"P-REG" modular architecture:
- **Text-correction module** for input errors.
- **Sentiment classifier** (fine-tuned Chinese ELECTRA-small) that selects emotion-adaptive response templates.
- **Routing model** that outputs a binary decision to call RAG or not.
- **LightRAG** graph-based retrieval over the expert knowledge graph, accessed through an asynchronous HTTP API.
- **Qwen2.5-1.5B** fine-tuned with LoRA (PEFT, AdamW).

Evaluation: LLM-as-judge (three referee models, six dimensions) plus double-blind expert human ratings against commercial LLMs.

## Results (key numbers and metrics)
- Human blinded comparison: 86.76 vs. 78.43-83.84 for commercial LLMs (p < 0.001), with advantages in Empathy, Hands-on guidance and Logical clarity (p < 0.05).
- Automated benchmark: Professional accuracy 86.18, Empathy 86.79, Hands-on guidance 82.58.
- Ablation: the router invoked RAG for only 20.1% of queries. This cut response time by 20.3% (6.5 s to 5.18 s) for a marginal score loss compared with always using RAG.
- LightRAG drives professional accuracy and the sentiment module drives empathy. The fine-tuned LLM alone scored lowest.

## Limitations
- Chinese cultural and linguistic context only.
- Possible data contamination: training and test data share origins (distilled data, forums).
- LLM-as-judge has positional, verbosity and self-enhancement biases.
- No real-world clinical or usability trial yet. Some comparisons with Grok 3 and o3-mini were not significant.

## Transferable ideas for the FYP pipeline
- **Deployment / LLM reasoning:** a 1.5B-class model with LoRA fine-tuning plus RAG can match larger commercial LLMs in a narrow domain. This supports running a local model on factory hardware so machine data stays private.
- **Text/RAG:** build a knowledge graph from TRUMPF manuals and fault codes (fault → cause → parameter → remedy). Use graph RAG (LightRAG) to ground answers.
- **LLM reasoning:** a router decides when retrieval is needed, which saves latency. A requirement analysis with operators and engineers (Kano-style) defines output qualities such as "actionable parameter adjustments".
- **Evaluation:** combine LLM-as-judge (several judges, multi-dimension rubric) with blinded expert ratings, and watch for train/test contamination.
