# Context-aligned representation editing and tuning with procedural priors for truthfulness improvement in large language models

- **Citation (IEEE):** X. Peng, G. Rao, J. Zhang, et al., "Context-aligned representation editing and tuning with procedural priors for truthfulness improvement in large language models," *Expert Systems With Applications*, vol. 331, Art. no. 133433, 2026, doi: n/a.
- **Domain:** NLP / LLM hallucination mitigation (representation engineering)
- **Relevance to FYP (1-5):** 2 - generic LLM truthfulness method. Hallucination control is important for evidence-based diagnosis, but the method needs white-box access to model activations.

## Problem
LLMs hallucinate even when they internally "know" the correct answer. Existing truthfulness interventions either need probes or full fine-tuning, or they make the model overly conservative (more refusals).

## Data & modalities
Text only. TruthfulQA is the main benchmark, plus seven out-of-distribution QA benchmarks (factuality, hallucination and reasoning, e.g., ARC-Challenge). The method is evaluated across 13 LLMs, including Llama-2-7B-Chat.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **CARE:** run an offline forward pass with many-shot, label-consistent in-context-learning demonstrations. Collect the intermediate activations and compress them into stable steering directions within each attention head's subspace ("procedural priors").
- **CARE-TF:** training-free, feature-adaptive representation editing at inference. No demonstration tokens are needed at run time.
- **CARE-PO:** learns only two non-negative scalars per head using Direct Preference Optimization (DPO), acting as soft head selection. This adds less than 0.00003% parameters.

## Results (key numbers and metrics)
- CARE-TF raises Llama-2-7B-Chat's TruthfulQA truthfulness from 67% to 92% without changing weights.
- CARE-PO reaches 82.3% True×Info.
- The refusal rate does not increase.
- Per-token latency overhead for CARE-PO is 4.4%.
- Largely transfers across architectures and OOD benchmarks, with small drops on some reasoning tasks (e.g., ARC-Challenge).

## Limitations
- Does not mechanistically explain why the directions work.
- The truthfulness vs. helpfulness/informativeness trade-off is application-dependent.
- Small degradation on reasoning-heavy tasks.
- Needs access to internal activations, so it is unusable with closed API models.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** if the FYP uses an open-weight local LLM/VLM (e.g., Llama or Qwen), CARE-style steering directions could be derived from many-shot, correctly labelled TruLaser diagnosis examples. This would bias the model toward evidence-faithful answers without adding long few-shot prompts at inference (lower latency).
- **Fine-tuning:** DPO on a tiny parameter set is a cheap alternative to LoRA when the labelled preference data (good vs. hallucinated diagnoses) is small.
- **Evaluation:** track both a truthfulness/faithfulness score and a refusal rate. Check that hallucination control does not degrade reasoning on process-optimisation questions.
