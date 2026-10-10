# Interpretable root-cause analysis of construction defects via knowledge-enhanced causal reasoning with large language models

- **Citation (IEEE):** M. Hou, Y. Zhu, and Z. Wang, "Interpretable root-cause analysis of construction defects via knowledge-enhanced causal reasoning with large language models," *Discover Artificial Intelligence*, vol. 6, art. 1166, 2026, doi: 10.1007/s44163-026-01640-2.
- **Domain:** Engineering quality management - LLM + knowledge graph + causal root-cause analysis
- **Relevance to FYP (1-5):** 5 - a near-blueprint for the FYP's reasoning stage: KG + RAG + causal inference + CoT LLM producing structured root-cause reports with standard-clause citations and remediation, evaluated against ML and GPT-4 baselines.

## Problem
Visual defect detectors answer "what" but not "why". Root-cause identification for construction defects is limited by insufficient domain knowledge, correlation-only reasoning and non-interpretable outputs.

## Data & modalities
4,152 annotated samples collected over 18 months from 12 projects in four Chinese provinces; six defect categories (cracks, leakage, hollowing, rebar corrosion, settlement, honeycombing); split 70/15/15. Inputs are textual defect descriptions plus structured causal evidence (no images used). Knowledge sources: 287 engineering standard documents, 1,128 on-site defect case records, 1,543 expert causal rules.

## Method
KE-CausalLLM, three modules: (1) **Engineering KG** with 3,867 entities and 9,214 edges; triples extracted from standards by few-shot prompted LLaMA-3-70B-Instruct; KG encoded with a 4-layer GAT (256-d, 8 heads). (2) **Causal reasoning**: structural causal model with counterfactual inference via the do-operator to find the minimal sufficient root-cause set (sufficiency threshold 0.85). (3) **KG-augmented LLM**: RAG dynamic subgraph retrieval (BGE-large-zh embeddings over serialised subgraphs) + chain-of-thought prompting on LLaMA-3-70B-Instruct, instruction-fine-tuned on the domain data (lr 2e-5, batch 16, 40 epochs, AdamW, 8x A100). Output: structured report with root causes, causal-chain evidence, standard clause references and remediation.

## Results
Accuracy 91.8%, F1 90.9%, AUC 0.957 vs SVM (74.3% acc), RF (78.6%), XGBoost (80.2%), BERT-Defect (83.7%), GPT-4 5-shot CoT (81.4%), KG-GNN (84.1%), CausalBERT (85.3%, F1 84.4%). Correctness requires Jaccard >= 0.7 against engineer-labelled root-cause sets. Cross-project-type (residential, roads, underground, bridges) mean accuracy 91.1%; 1.29 s average inference. Interpretability Likert score 4.29/5 from 10 senior experts and 20 engineers. Ablations show each module (KG, causal reasoning, standards) contributes.

## Limitations
Causal sufficiency cannot be verified without randomised interventions (unobserved confounders); data concentrated in Chinese projects/standards; text-only - no visual modality yet; 70B model with 8K context is resource-heavy.

## Transferable ideas for the FYP pipeline
- **Text/RAG + KG:** build a laser-cutting KG from TRUMPF manuals, cutting-parameter tables, service cases and expert rules (defect -> cause -> parameter -> remedy); retrieve relevant subgraphs per case.
- **LLM reasoning:** CoT prompt that must output root cause, causal chain evidence (machine-table values, image findings), manual/standard references and remediation steps.
- **Causal module:** counterfactual "what if gas pressure were nominal?" checks to prune candidate causes before the LLM explains them.
- **Evaluation:** baselines spanning classical ML on tabular features, few-shot GPT-class LLM, and the full pipeline; Jaccard-based root-cause matching; expert Likert interpretability scoring; ablations per module.
- **Fusion:** extend with image evidence (the authors' stated next step) - exactly the FYP's multimodal contribution.
