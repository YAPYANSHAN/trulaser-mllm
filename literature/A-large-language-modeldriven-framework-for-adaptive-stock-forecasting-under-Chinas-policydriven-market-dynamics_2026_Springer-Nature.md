# A large language model-driven framework for adaptive stock forecasting under China's policy-driven market dynamics (DPAD-Net)

- **Citation (IEEE):** S. Zhang and Z. Li, "A large language model-driven framework for adaptive stock forecasting under China's policy-driven market dynamics," *Discover Artificial Intelligence*, vol. 6, art. 1100, 2026, doi: 10.1007/s44163-026-01837-5.
- **Domain:** Financial time-series forecasting with LLM-derived priors
- **Relevance to FYP (1-5):** 3 - finance domain, but its "LLM as regime classifier producing structured priors that gate a numeric model" is a strong template for fusing text/doc reasoning with machine time-series.

## Problem
In China's A-share market, policy announcements cause abrupt regime shifts that break stationarity assumptions of time-series models; existing LLM fusion treats text insights as static concatenated features rather than changing the model's behaviour.

## Data & modalities
Daily OHLCV for the CSI 300 index and 10 A-share stocks (AkShare, forward-adjusted) plus multi-source text streams (policy, macro news, sentiment) cleaned by de-duplication, HTML stripping and summarisation.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- MRP-LLM (macro-regime perception): Qwen1.5-72B-Chat instruction-tuned with LoRA (r=16, LR 2e-5, 3 epochs, 4x A100 80GB) on A-share financial corpora ("Qwen-72B-FinA").
- Chain-of-Thought prompt (observe, analyse, conclude) returns JSON: one of five discrete regimes (bullish momentum, bearish panic, range-bound, policy-driven rally, event-driven volatility), confidence score and volatility encoding, turned into a dynamic prior vector.
- RAND-Net: regime-adaptive non-linear decomposition with learnable gates that change the decomposition formula, splitting price into a stable value anchor and volatile sentiment component; dual-track prediction for each component.
- Grounded in regime-switching and Bayesian inference ideas.

## Results (key numbers and metrics)
- 13.6% MSE reduction and 27.6% Sharpe-ratio improvement vs state-of-the-art baselines; better robustness in volatile periods.
- MRP-LLM regime classification accuracy 89.0% vs human consensus labels; quantised INT8 88.8% and INT4 88.5%, latency 1.2-1.8 s; VRAM about 144 GB FP16, 78 GB INT8, 42 GB INT4.

## Limitations
Discrete regime set; no explicit modelling of LLM epistemic uncertainty (error propagation in anomalies); heavy 72B model; future work on continuous/hierarchical regimes and RL-optimised adaptation.

## Transferable ideas for the FYP pipeline
- **LLM reasoning / fusion:** have the LLM classify the machine "operating regime" (e.g., normal, nozzle wear, lens contamination, gas supply issue, material batch change) from logs/alarms/documents into a JSON prior with confidence, then use it to gate or condition the numeric anomaly/quality model.
- **Text/RAG:** CoT prompt structure (observe evidence -> analyse -> conclude with label + confidence) yields auditable diagnostic reasoning.
- **Fine-tuning / deployment:** LoRA tuning of an open LLM on domain corpora, and quantisation (INT8/INT4) with measured accuracy loss and latency, is a deployment trade-off table worth replicating at smaller scale.
- **Evaluation:** validate the LLM's intermediate labels against human (technician) consensus, separately from end-task metrics.
