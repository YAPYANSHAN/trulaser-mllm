# TriUTest: Internalizing execution feedback for defect-exposing python unit test generation

- **Citation (IEEE):** Z. Li, Z. Wang, and C. Cui, "TriUTest: Internalizing execution feedback for defect-exposing python unit test generation," *Neurocomputing*, vol. 706, Art. no. 135014, 2026, doi: 10.1016/j.neucom.2026.135014.
- **Domain:** Software engineering / LLM post-training (unit test generation)
- **Relevance to FYP (1-5):** 1 — software testing domain; only the general SFT → distillation → RL-from-execution-feedback recipe for small models is loosely transferable.

## Problem
LLM-generated Python unit tests often achieve high coverage but low defect exposure: weak assertions, collapse of candidate diversity, and no mechanism to turn execution feedback (e.g., mutation kills) into learnable training signals.

## Data & modalities
Text/code with execution feedback. Benchmarks: HumanEval, QuixBugs-Python (real defects), codetiming (3 modules) and apimd (25 files) open-source projects.

## Method
Three-stage post-training of a small LLM:
1. **SFT** on real executable focal-method/test pairs to learn test structure and basic assertions.
2. **DQ-GKD**: guided knowledge distillation from teacher Qwen2.5-14B-Instruct to student Qwen2.5-3B-Instruct on student-sampled candidates, with quality-weighted distribution calibration on test-sensitive spans (input construction, invocation, assertions) plus a multi-candidate likelihood regularizer to curb collapse.
3. **SM-GRPO**: GRPO reinforcement learning with stateful mutant-coverage tracking and a marginal incremental kill reward, converting suite-level Mutation Kill Rate (MKR) into per-test rewards and encouraging complementary tests.
Evaluation under equal budgets, five seeds, cluster-robust significance tests; baselines include Pynguin, MuTAP, pytLMtester and SFT-only models.

## Results
- TriUTest (3B): macro-averaged 77.11% statement / 52.55% branch coverage.
- Best macro-averaged MKR 48.75%.
- Highest Fail Trigger Rate 78.50% on QuixBugs.
- Beats same-scale and larger SFT-only baselines on defect-oriented metrics; authors do not claim superiority on some raw-coverage comparisons (e.g., vs MuTAP/pytLMtester on QuixBugs, Pynguin on codetiming).

## Limitations
Fails on defects requiring complex program-state construction (e.g., linked-node graph inputs in BFS/DFS); limited, small benchmarks not representative of large industrial systems; tied to Qwen2.5-3B/14B; dual-environment evaluation introduces validity threats.

## Transferable ideas for the FYP pipeline
- **Fine-tuning:** the SFT → teacher distillation → reward-based RL pipeline shows how a small (3B) local model can be pushed toward a task-specific objective; for the FYP, a large teacher LLM could generate diagnosis rationales for distillation into a small deployable model.
- **Evaluation:** "high fluency ≠ correct diagnosis" parallels "high coverage ≠ defect exposure"; define metrics that measure whether the diagnosis actually identifies the true root cause, not just whether it looks complete.
- Marginal-reward idea: reward each additional diagnostic hypothesis only if it covers a fault not already covered (diversity in candidate causes).
