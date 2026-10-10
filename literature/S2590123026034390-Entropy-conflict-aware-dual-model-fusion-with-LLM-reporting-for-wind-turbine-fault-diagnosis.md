# Entropy-conflict-aware dual-model fusion with LLM reporting for wind turbine fault diagnosis

- **Citation (IEEE):** B. Shi, Z.-W. Gao, and Y. Liu, "Entropy–conflict-aware dual-model fusion with LLM reporting for wind turbine fault diagnosis," *Results in Engineering*, vol. 32, Art. no. 112421, 2026, doi: n/a.
- **Domain:** Industrial fault diagnosis (wind-turbine bearings/gearboxes) / decision fusion + KG + LLM reporting
- **Relevance to FYP (1-5):** 5 - a near-direct template. A data-driven branch and a knowledge-graph rule branch are fused with uncertainty and conflict handling plus an "Unknown" rejection. A LoRA-tuned LLM then writes evidence-faithful diagnostic reports, with dedicated faithfulness metrics.

## Problem
Deep vibration models are accurate but opaque. Rule-based models are traceable but weaker. Naive fusion of the two mishandles disagreement and uncertainty, and LLM-generated reports can invent evidence or contradict the decision.

## Data & modalities
Four public datasets: CWRU, NEPU and XJTU (bearings) and WTG (wind-turbine gearbox). The inputs are vibration signals and extracted features.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Branch 1, DSDC-Net:** depthwise-separable convolutions with dense connectivity learn multi-scale representations.
- **Branch 2, decision-tree-derived KG:** links signal features, thresholds, decision paths, fault categories and mechanism knowledge, so every rule is traceable.
- **Entropy-conflict-aware fusion:** probabilities are calibrated, the weaker branch is identified by entropy, inter-model conflict is quantified, and uncertain predictions are discounted.
- **Dual-threshold rejection:** samples with high conflict or low support are labelled Unknown. Thresholds are chosen by balanced accuracy.
- **Rule-constrained LLM reporting:** Llama3-8B is LoRA-fine-tuned (rank 16, alpha 32, 5 epochs, batch 32). It turns the fixed fusion result and evidence into reports and maintenance actions without changing the decision. Allowed and prohibited action sets apply; for Unknown, only conservative actions are permitted (re-measure, inspect, monitor, manual review).

## Results (key numbers and metrics)
- **Fusion:** average Accuracy 0.9037 and Macro-F1 0.9001 across the four datasets under identical branch outputs. Calibrated entropy raises branch-selection accuracy from 61.84% to 69.78%.
- **WTG:** statistically significant gains of +4.69 points Accuracy and +6.75 points Macro-F1.
- **Unseen load (leave-one-condition-out on CWRU):** Accuracy 0.91-0.95 (mean 0.93) and Macro-F1 0.90-0.94 (mean 0.92). This beats the strongest baseline, TFSAF-Net, by 1.5 and 2.5 points.
- **LLM reports, base vs. LoRA-tuned:**
  - Evidence Faithfulness Rate (EFR): 0.935 → 0.965
  - Conflict Explanation Accuracy (CEA): 0.880 → 0.940
  - Maintenance Recommendation Consistency (MRC): 0.925 → 0.960

## Limitations
- Vibration only; no images or text inputs to the diagnosis.
- The LLM is restricted to post-hoc reporting and does not reason over raw data.
- Threshold tuning trades coverage against reliability.
- Mostly lab benchmark datasets.

## Transferable ideas for the FYP pipeline
- **Fusion:** run parallel branches, (a) a learned model on machine tables and images and (b) a rule/KG branch from TRUMPF documentation (e.g., parameter thresholds). Fuse them with entropy and conflict weighting, and output "Unknown → inspect" when they disagree.
- **LLM reasoning:** keep the LLM *downstream* of a fixed decision for safety. Constrain its maintenance actions with allowed and prohibited lists per diagnostic state.
- **Fine-tuning:** LoRA on Llama3-8B with the settings above is a realistic FYP-scale recipe.
- **Evaluation:** adopt EFR, CEA and MRC to measure report faithfulness, plus a leave-one-condition-out test (e.g., unseen sheet thickness).
