# Concise thoughts: Impact of output length on LLM reasoning and cost

- **Citation (IEEE):** S. Nayab, G. Rossolini, M. Simoni, et al., "Concise thoughts: Impact of output length on LLM reasoning and cost," *Information Sciences*, vol. 757, art. 123939, 2026, doi: 10.1016/j.ins.2026.123939.
- **Domain:** NLP — prompt engineering and evaluation of LLM reasoning efficiency
- **Relevance to FYP (1-5):** 2 — text-only arithmetic reasoning benchmarks; transferable as a cheap prompting trick (length-constrained CoT) and metrics for balancing explanation length, latency and correctness in diagnostic outputs.

## Problem
Chain-of-thought (CoT) improves accuracy but produces long, variable-length outputs; because decoding is autoregressive, generation time grows with length, which hurts interactive use. Standard accuracy ignores conciseness.

## Data & modalities
Text only. Arithmetic reasoning datasets: GSM8K test (~1.3k problems), SVAMP (300), ASDiv (1.22k). Preliminary analysis on 100/50 GSM8K questions.

## Method
- **Constrained-CoT (CCoT):** CoT prompt plus explicit word limit (e.g. "limit the answer length to k words"), k ∈ {15, 30, 40, 45, 60, 100}.
- Three correctness-with-conciseness metrics: **HCA(k)** (hard-k concise accuracy — fraction correct within k words), **SCA(k, α)** (soft penalty for exceeding k), **CCA(k, α, β)** (also penalises length variability).
- Structural analysis: number of reasoning steps, **redundancy** and **information flow** between reasoning steps in embedding space.
- Models: Llama2-70b-chat-hf and Falcon-40b-instruct (plus smaller models in appendix) on TGI with 8×A100. No fine-tuning.

## Results
- Llama2-70b on GSM8K: accuracy rises from 36% (CoT) to 37% (CCoT-30) and 41.77% (CCoT-100); generation time falls from 30.1 s (CoT) to 23.86 s (CCoT-100).
- Falcon-40b: better accuracy/time trade-off on SVAMP and ASDiv, not on GSM8K.
- Information flow between steps reduced by 26–41% with CCoT-15 vs CoT on GSM8K (4–20% for CCoT-100).
- Models often fail to respect very tight limits (15–40 words); smaller models lose accuracy under constraints.

## Limitations
Only arithmetic reasoning; older open models (Llama2, Falcon); small models struggle; metric parameters (k, α, β) are user-defined; open-domain/multi-hop tasks untested.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** constrain diagnosis rationales (e.g. "≤80 words of reasoning, then JSON verdict") to cut latency and token cost on the shop floor; tune k empirically per model.
- **Evaluation:** report a concise-accuracy metric (HCA/SCA) alongside diagnostic accuracy, plus mean/variance of generation time, to choose prompts for deployment.
- **Model choice:** verify that the chosen (possibly smaller, locally hosted) model still reasons correctly under length limits before adopting CCoT.
