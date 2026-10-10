# Reinforcement learning-powered co-optimization: Bridging critic model and multimodal LLM reasoning abilities

- **Citation (IEEE):** Q. Wang, S. Liu, Z. Zhang, et al., "Reinforcement learning-powered co-optimization: Bridging critic model and multimodal LLM reasoning abilities," *Pattern Recognition*, vol. 180, art. 113955, 2026, doi: 10.1016/j.patcog.2026.113955.
- **Domain:** Multimodal LLM reasoning — RL fine-tuning (actor–critic "slow thinking")
- **Relevance to FYP (1-5):** 3 — general MLLM reasoning on math/chart VQA benchmarks, not industrial; but the external critic/self-refinement and critic-as-reward-model ideas are applicable to verifying fault diagnoses, albeit training-heavy.

## Problem
"Slow thinking" (reflection) boosts MLLM reasoning. Internal methods (reflection tokens in the chain, e.g. o1/DeepSeek-R1 style) cause long, redundant outputs and unstable RL; external critic methods produce unreliable critiques and poorly aligned actor–critic interaction.

## Data & modalities
Image + text VQA. Critic cold-start dataset (MMC) built with Qwen2.5-VL-7B on queries from MathV360k, ChartQA and M3CoT: ~2,100k critique triplets filtered to 1,020k (48.6% retained), 8:1 train/val. Evaluation on MathVista, MathVerse, MathVision, MMStar, MMMU, etc.

## Method
- **COCA (Co-Optimization of Critic and Actor):** a critic MLLM evaluates the actor MLLM's answer; the actor refines using the critique history; iterate.
- Critic cold-start via SFT on MCTS-generated reasoning paths and critiques (multitask objective, λ = 0.1).
- Both critic and actor trained iteratively with **GRPO**, reward = rule-based correctness of the final answer (no human annotation); critic rewarded when its feedback leads the actor to correct answers.
- Sampling strategy: use highest-reward critique for actor training.
- Optimised critic reused as a **generative reward model (GRM)** for best-of-N selection (COCA*).
- Backbones: Qwen2-VL-7B and Qwen2.5-VL-7B.

## Results
- COCA*-7B: MathVerse 59.8%, MathVista 78.7% vs GPT-4o (50.2%, 63.8%) and Qwen2.5-VL-72B (57.6%, 74.8%); MMStar 71.1% (best of compared); MathVision on par with Claude-3.5-Sonnet.
- COCA-7B (no GRM): MathVista 77.0% vs Vision-R1 73.5%, matching Shuffle-R1.
- Ablations confirm the highest-reward critique sampling beats random critique at one-third the cost of alternatives.

## Limitations
Two separate models (actor and critic) increase deployment complexity and resource overhead; heavy training (million-scale data, RL); evaluated on general/math benchmarks, not domain tasks.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** implement a lightweight "critic pass" — a second MLLM call (or same model with a critic prompt) that checks the diagnosis against image evidence, machine-data values and retrieved manual text, then asks for a refinement if inconsistent.
- **Evaluation / selection:** use a critic as a reward model to pick the best of N candidate diagnoses.
- **Fine-tuning (stretch goal):** if labelled fault cases exist, GRPO with rule-based correctness rewards (correct fault class/parameter recommendation) avoids human-written rationales; realistic only at small scale with a 7B VLM.
- **Deployment:** account for the latency/compute of two-model loops.
