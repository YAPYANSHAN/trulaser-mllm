# CURENet: Combining Unified Representations for Efficient Chronic Disease Prediction

- **Citation (IEEE):** C.-T. Dao, N. M. T. Phan, J.-E. Ding, et al., "CURENet: combining unified representations for efficient chronic disease prediction," *Health Information Science and Systems*, vol. 14, art. 7, 2026, doi: 10.1007/s13755-025-00396-w.
- **Domain:** Healthcare / multimodal EHR prediction (text + lab values + time series)
- **Relevance to FYP (1-5):** 3 - medical domain, but its fusion of LoRA-tuned LLM embeddings of text/textualised lab values with a time-series transformer over irregular events is directly analogous to fusing machine logs, parameter tables and notes.

## Problem
EHRs combine unstructured notes, structured lab tests and irregular longitudinal visits, but most predictors use one modality or shallow fusion and ignore temporal irregularity, limiting chronic-disease prediction.

## Data & modalities
Public MIMIC-III and private FEMH (Far Eastern Memorial Hospital, Taiwan) datasets. Modalities: clinical notes (text), lab tests converted to text, and time-series visit sequences including visit duration and inter-visit intervals. Task: multi-label prediction of the top-10 chronic diseases (plus a heart-failure case study).

## Method
Text branch: LLM (best backbone Medical-Llama3-8B, derived from Meta-Llama-3-8B) fine-tuned with LoRA and 4-bit NF4 quantisation to embed clinical notes and textual lab results. Temporal branch: Time Series Transformer encoding visit sequences with duration/interval features. Fusion: concatenation of LLM semantic embedding and temporal embedding, followed by a multi-label classifier. Baselines: BERT and LoRA-tuned Mistral-7B-v0.1, Llama-2-7B, Llama-2-13B, Llama-3-8B and Medical-Llama3-8B, plus prior multimodal EHR models. Metrics: accuracy, precision, recall, weighted/macro F1, Recall@k, NDCG@k, AUC.

## Results
Over 94% accuracy in multi-label top-10 chronic disease prediction on both datasets (table values around 0.94). On MIMIC-III test set, macro F1 1.49% higher than LoRA Medical-Llama3-8B alone; overall gains of about 2-4% over baselines. Medical-domain LLMs consistently beat general-purpose ones. QLoRA-style setup allows inference on GPUs with roughly 8-12 GB memory. Heart-failure case study: improved recall, AUC and F1.

## Limitations
Interpretability still limited (attention visualisation / feature attribution are future work); generalisability, cold-start patients and deployment across hospitals not addressed; private dataset not shareable; fusion is simple concatenation.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series:** encode TruLaser event and alarm sequences with a time-series transformer that explicitly includes durations and gaps between events (irregular sampling, like hospital visits).
- **Tabular ingestion:** textualise numeric records (e.g. "laser power 4.2 kW, gas pressure 12 bar, feed 3.1 m/min, nitrogen") so an LLM can embed them alongside operator notes - the lab-values-as-text trick.
- **Fusion:** concatenate LLM text embeddings and temporal embeddings as a strong, simple baseline before trying cross-attention.
- **LLM reasoning / deployment:** LoRA + 4-bit quantisation of an 8B model makes fine-tuning feasible on a single student GPU; prefer a domain-adapted base model where one exists.
- **Evaluation:** multi-label metrics (macro F1, Recall@k, NDCG@k) suit multiple simultaneous fault causes.
