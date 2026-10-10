# Distinguishing cancer patients' mild and severe symptoms in radiotherapy via zero-shot and few-shot large language model-based probabilistic prompts

- **Citation (IEEE):** M. W. Chen, Y. Yan, X. Shen, et al., "Distinguishing cancer patients' mild and severe symptoms in radiotherapy via zero-shot and few-shot large language model-based probabilistic prompts," *BioData Mining*, vol. 19, art. 47, 2026, doi: 10.1186/s13040-026-00547-z.
- **Domain:** Medical informatics — LLM-based anomaly detection on structured patient-reported outcome (PRO) data
- **Relevance to FYP (1-5):** 3 — medical domain, but the method transfers well: prompting LLMs to do anomaly detection on structured/tabular records with probabilistic anomaly scores and explanations, under heavy class imbalance. This closely mirrors flagging abnormal laser-cutting jobs.

## Problem
ML/DL toxicity-monitoring models for radiotherapy patients are expensive to retrain, need large data, and give poor clinical explanations. The goal is to classify mild vs. severe symptoms with little or no labelled data, with explanations.

## Data & modalities
Structured, de-identified prostate-cancer PRO questionnaire data (KUMC, 2021–2024). There are 22 instruments (urinary, bowel, sexual, vitality/hormonal). Targets and class counts:
- Rectal pain/urgency: 10,356 mild vs. 586 severe.
- Sexual dysfunction: 8,444 mild vs. 1,998 severe.
- Depression: 10,266 mild vs. 665 severe.

Severe classes are rare, so the problem is framed as anomaly detection. Text only (serialised records).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Six prompt designs within an "AD-LLM" framework (no fine-tuning):
- **Zero-shot** with Llama-3.1-8B: two variants, Mild-only and Mixed context.
- **Few-shot**: five examples each, in three variants (mild only, severe only, mixed).
- **Probabilistic one-shot** with GPT-4o: one mild or one severe anchor example, or a two-shot variant with high- and low-confidence examples.

Prompts ask for an `anomaly_score` in [0, 1] with confidence bands (>0.75 strong concern, 0.4–0.75 moderate, <0.4 normal) plus a natural-language rationale. The "normal-only" variant forbids reference to severe patterns. Evaluation uses AUC, AUCPR, precision, recall and F1 with bootstrap 95% CIs, plus ROC/PR curves and confusion matrices.

## Results (key numbers and metrics)
- Bowel pain was best. Probabilistic one-shot GPT-4o (Mild + Severe) reached AUC 0.9416 [0.9302, 0.9524] and AUCPR 0.8780. Another configuration reports precision 0.9092, recall 0.7506 and F1 0.8222. GPT-4o Mild reached the highest F1 of 0.8262.
- Depression was moderate (AUC ~0.65–0.75, F1 ~0.64).
- Sexual dysfunction was hardest (AUCPR < 0.35, precision < 0.32, F1 < 0.46).
- Probabilistic one-shot was generally the best strategy.

## Limitations
Performance varies widely across symptom domains. Single institution and a single cancer type. Prompt-only, with no domain adaptation. Recall-oriented settings produce many false alarms. Proprietary GPT-4o is used for the best results.

## Transferable ideas for the FYP pipeline
- **Tabular/LLM reasoning:** serialise a machine-database row (job parameters, alarms, quality flags) into a prompt. Ask for a calibrated anomaly/fault score with explicit bands plus a rationale. This gives a ranked, explainable output instead of a bare label.
- **Prompting:** use anchor examples (one normal job, one defective job, or high- and low-confidence exemplars). Compare zero-, few- and one-shot designs systematically as an ablation in the FYP.
- **Class imbalance:** treat rare defects as anomalies, define "normal" from good-cut records, and evaluate with AUCPR, not just accuracy.
- **Evaluation:** report bootstrap CIs, ROC/PR curves and per-defect-type breakdowns. Expect large variation by fault category.
- **Deployment:** a small open model (Llama-3.1-8B) is a cheap local baseline against GPT-4o-class models.
