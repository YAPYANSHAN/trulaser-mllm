# D-ProtoCoT: Prototype-based path selection for chain-of-thought reasoning

- **Citation (IEEE):** Z. Zhang and A. Feng, "D-ProtoCoT: Prototype-based path selection for chain-of-thought reasoning," *Neurocomputing*, vol. 705, Art. no. 134976, 2026, doi: 10.1016/j.neucom.2026.134976.
- **Domain:** NLP / LLM reasoning (inference-time chain-of-thought selection)
- **Relevance to FYP (1-5):** 2 — general reasoning method; transferable as a way to pick the most coherent of several sampled diagnostic reasoning chains.

## Problem
Self-consistency aggregates sampled chain-of-thought (CoT) paths by majority vote on final answers, assuming all paths that reach an answer are equally good. Outcome Reward Models ignore flawed steps; Process Reward Models need expensive step-level annotation.

## Data & modalities
Text. Benchmarks: CommonsenseQA, GSM8K, StrategyQA (question-grouped held-out splits where official test labels unavailable). Generators: LLaMA-3.1-8B-Instruct and Qwen3-8B; scaling check on Qwen3-14B.

## Method
- Sample multiple CoT paths from a frozen LLM.
- Lightweight auxiliary encoder (BERT-base-uncased) fine-tuned with a step-level InfoNCE contrastive objective: each reasoning step is an alignment target; labels derived only from gold final answers (no step annotation).
- At inference, a dynamic prototype is built by similarity-weighted aggregation of path embeddings; the path best aligned with the prototype is selected (no gold answer needed at inference).
- Baselines: standard CoT, self-consistency, ORM, static frozen-BERT centroid prototype, C-CoT.

## Results
- Consistently beats self-consistency in most settings; largest gain up to 8.5 percentage points on GSM8K with LLaMA-3.1-8B-Instruct.
- StrategyQA (LLaMA-3.1-8B): 66.67% vs 52.38% for static centroid prototype.
- Qwen3-14B GSM8K: 97.50% vs self-consistency 97.00%, ORM 96.50%.
- Representation AUC of 0.78 for separating path quality; ablations show both step-level contrastive training and prototype selection contribute.

## Limitations
Needs gold answers to train the encoder; outcome-derived labels broadcast to steps (correct answer via flawed step still labelled positive); gains shrink when sampled paths lack diversity; extra latency from encoder; benchmark scale limited; inherits encoder biases.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** for each fault case, sample several diagnostic reasoning chains (e.g., "dross → low gas pressure → check nozzle"), then select the chain most consistent with the others in an embedding space rather than simply voting on the final fault label.
- **Evaluation:** labelled historical fault cases (fault label = gold answer) could train a small encoder that scores reasoning quality, at low annotation cost.
- **Trust:** keep the selected chain as the auditable explanation shown to the engineer; flag low-agreement cases for human review.
