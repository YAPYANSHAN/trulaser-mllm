# RepoCBench: A benchmark for C-oriented repository-level code generation with large language models and agents

- **Citation (IEEE):** Y. Zhang, K. Yao, L. Zhang, et al., "RepoCBench: A benchmark for C-oriented repository-level code generation with large language models and agents," *Expert Systems With Applications*, vol. 331, Art. no. 133242, 2026, doi: 10.1016/j.eswa.2026.133242.
- **Domain:** Software engineering; LLM/agent code-generation benchmarking (C language, embedded/IoT/industrial control repositories).
- **Relevance to FYP (1-5):** 1 - Code generation benchmark with no fault-diagnosis, vision or manufacturing content; only generic lessons on context selection and agent self-correction transfer.

## Problem
Code benchmarks (HumanEval, MBPP, ClassEval, SWE-bench, etc.) focus on Python/Java and function-level tasks. C - central to OS and embedded systems, with pointers, manual memory, structs - lacks a repository-level benchmark for LLMs and agents.

## Data & modalities
Text/code. 10 GitHub C repositories (embedded scripting, IoT protocol stacks, industrial control protocols, RTOS kernels) chosen for recency, stars and documentation quality; 200 tasks after pruning trivial functions; every task needs cross-file context (often 3-4 dependency snippets); projects mostly 1,000-2,500 LOC. Skeletons with TODO function bodies, docstrings, and basic/edge/large-scale tests. Near-duplicate decontamination on normalised code.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Evaluated 11 LLMs (GPT-3.5-turbo, GPT-4o, GPT-4.5, Claude-3.5, Gemini-2.5, Grok3, Qwen2.5-Coder, Qwen2.5-72B, QwQ-32B, DeepSeek-V3, DeepSeek-R1) and 4 agents (AutoGPT, SWE-agent, Bailian, Coze). Greedy decoding (T=0), 1,024-token max output. Three context settings: none, relevant context, maximum (full window, e.g., 128K). System + instruction prompt templates. Agents limited to the same context to isolate planning/self-debugging. Metrics: Completion@1, Compilation@1, Pass@1, Reuse@1 (key function reuse), Relative Execution Time, Cyclomatic Complexity deviation.

## Results (key numbers and metrics)
- No context: GPT-4o 100% completion but 0% compilation on Repo 1 ("surface-level correct" code); with relevant context, 45.45% compilation / 25% Pass@1.
- Relevant context beats maximum context for most models (Repo 2: GPT-4.5/Claude-3.5 71.43% drops to 50% / 64.29% with max context); max context occasionally helps in very complex repos (Repo 3 compile 82.50% vs. 75.50%).
- GPT-4o Pass@1 falls from 80% (Repo 1) to 44.4% (Repo 10); agents form the outer envelope.
- SWE-agent backbones (relevant context): DeepSeek-R1 90.0% compile / 76.2% Pass@1; Claude-3.5 86.8/71.5; Qwen2.5-Coder 85.9/71.2; Gemini-2.5 85.5/70.8.
- GPT-4.5 RET 1.02, DeepSeek-R1 1.03; agents produce higher complexity (+1.4 SWE-agent).

## Limitations
Only 10 repositories / 200 tasks; agents constrained from autonomous retrieval; data on request; C-specific.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** Curated relevant context beats dumping the full manual or full database into the window - supports targeted retrieval of TruLaser documentation sections and only the relevant table rows.
- **LLM reasoning:** Agentic loops with tool feedback (here compiler errors) outperform one-shot generation; analogously, let the diagnosis agent query the machine database/SQL and retry on errors.
- **Evaluation:** Separate "looks complete" from "actually correct" metrics (cf. Completion vs. Pass@1) - e.g., a diagnosis that is well-formatted vs. one matching technician ground truth.
