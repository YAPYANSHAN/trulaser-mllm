# Self-Prompt: Gradient-guided discrete prompt optimization for code generation

- **Citation (IEEE):** L. Zhu, W. Zong, Y. Tong, et al., "Self-Prompt: Gradient-guided discrete prompt optimization for code generation," *Neurocomputing*, vol. 706, Art. no. 134963, 2026, doi: 10.1016/j.neucom.2026.134963.
- **Domain:** NLP / automated prompt engineering for LLM code generation
- **Relevance to FYP (1-5):** 1 — code-generation prompt optimization requiring white-box gradients; only a marginal idea for tuning system prompts of an open LLM.

## Problem
LLM code-generation reliability is highly sensitive to prompt wording. Automated prompt engineering (e.g., APE) searches discrete text heuristically and is limited by linguistic priors; soft prompts are not deployable as text. The paper seeks gradient-driven optimization that still yields a discrete, human-readable prompt artifact.

## Data & modalities
Text/code only. Benchmarks: HumanEval, MBPP and their EvalPlus versions (HumanEval+, MBPP+). Optimization uses a held-out evaluation subset, not the test set.

## Method
- Decouples the prompt into (1) self-generated natural-language contextual scaffolding and (2) gradient-guided discrete trigger tokens.
- Parameter-frozen "pseudo-training": only a virtual embedding layer is updated by gradient descent, then the learned continuous vectors are projected to the nearest vocabulary tokens.
- Eleven open-weight LLMs (3B-30B): Qwen3-4B, Qwen3-8B, Qwen3-30B-A3B-Instruct (MoE), Llama-3.2-3B-Instruct, Phi-4-mini-instruct, ChatGLM3-6B, Qwen2-7B, Llama-3-8B, Gemma-2-9B, Yi-1.5-9B, among others.
- Baselines: default prompt, manual prompt, APE. Metric: pass@1 under greedy decoding; multi-seed robustness in appendix.

## Results
- Qwen3-4B: HumanEval 0.793 (APE 0.750, manual 0.756); MBPP 0.704 → 0.743; HumanEval+ 0.707 → 0.738.
- Qwen3-30B-A3B-Instruct: HumanEval 0.921, MBPP 0.910, exceeding APE.
- ChatGLM3-6B HumanEval 0.262 (APE) → 0.518; Llama-3-8B 0.573 → 0.610.
- Best or second-best in most configurations; a few cases (Llama-3-8B MBPP/MBPP+, Qwen2-7B MBPP+, Yi-1.5-9B MBPP) fall short.

## Limitations
Requires white-box gradient access — not usable with API-only closed models; extracted trigger tokens are semantically opaque (low interpretability); validated only on 3B-30B models; code-generation tasks only.

## Transferable ideas for the FYP pipeline
- **LLM reasoning / prompting:** if the FYP uses a local open model (e.g., Qwen3-8B) for diagnosis, prompts can be optimized automatically against a small validation set of labelled fault cases rather than by hand; at minimum, compare default vs manual vs automatically searched (APE-style) system prompts.
- **Evaluation:** optimize prompts on a held-out dev split and report on a separate test split to avoid prompt overfitting.
- Caution: opaque trigger tokens conflict with the FYP's goal of auditable, explainable reasoning, so human-readable prompts are preferable.
