# Toward trustworthy and explainable AI-driven industrial fault diagnosis: A data-to-deployment review

- **Citation (IEEE):** T.-D. Nguyen, M.-C. Nguyen, N.-L. Ngo, et al., "Toward trustworthy and explainable AI-driven industrial fault diagnosis: A data-to-deployment review," *Results in Engineering*, vol. 32, Art. no. 113189, 2026, doi: 10.1016/j.rineng.2026.113189.
- **Domain:** Industrial fault diagnosis / review (ML, DL, transfer learning, XAI, deployment)
- **Relevance to FYP (1-5):** 4 - a methodological backbone for the FYP's evaluation, XAI and deployment chapters: data leakage, domain shift, explanation validation and staged commissioning. LLMs are barely covered.

## Problem
Intelligent fault diagnosis reports high benchmark accuracy, but performance degrades across machines, operating regimes, sensors and time. The review asks how to make diagnostic evidence credible, how to choose transferable methods, and how to assure industrial use.

## Data & modalities
- A structured narrative review (not a systematic review), mainly covering 2020-2025 plus foundational works and a few early-2026 papers.
- Covers public benchmark datasets and sensor modalities (vibration, acoustic, current, thermal, images, process data), and compares the roles of multi-sensor fusion.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
The review is organised along the data-to-deployment pathway:
- acquisition and preprocessing
- traditional ML (feature engineering, conditions under which it is the right choice)
- deep learning (architectures, overfitting control, robustness evaluation)
- transfer learning and domain adaptation (negative transfer, catastrophic forgetting)
- XAI, with a decision-oriented taxonomy: local attribution, global effects such as ALE/PDP, counterfactuals such as CEM/DiCE, and spatial/temporal attribution
- industrial deployment and integration (edge vs. cloud, workflows)
- cross-method synthesis and research priorities

## Results (key numbers and metrics)
Qualitative conclusions:
- Data leakage, class imbalance, sensor instability and untested domain shift make complex models look more reliable than they are.
- Traditional ML remains preferable when physical features are stable and labels are few. Deep learning suits raw, sequential, image or multimodal data. Transfer learning is useful only when source-target compatibility and negative transfer are evaluated.
- Explanations are evidence to be examined, not proof. They must be validated for fidelity, stability, physical plausibility and usefulness to engineers.
- Deployment should be staged: independent validation → shadow operation → advisory use → bounded automation → fleet integration, with readiness gates between stages.
- Priorities: independent validation, uncertainty calibration, edge efficiency and human evaluation. Long-term: lifelong adaptation, fleet learning and validated digital twins.

## Limitations
- A narrative review, so the selection is not exhaustive or reproducible like a PRISMA review.
- No quantitative meta-analysis.
- Only marginal coverage of LLM/VLM-based diagnosis.

## Transferable ideas for the FYP pipeline
- **Evaluation:** use split protocols that prevent leakage (by job, sheet, material or date). Report class-imbalance-aware metrics and test explicitly under domain shift (new material or thickness).
- **LLM reasoning/XAI:** treat the LLM's explanation as a claim to be validated. Check its fidelity to the underlying model outputs, its stability under paraphrased prompts and its physical plausibility against laser-cutting physics, and run user studies with operators.
- **Deployment:** frame the FYP prototype as "advisory/shadow mode" in the staged pathway, combine it with calibrated uncertainty and abstention/escalation rules, and define readiness gates for progression.
- **Fusion:** use the review's comparison of multi-sensor fusion roles to justify the choice of early, feature-level or decision-level fusion.
