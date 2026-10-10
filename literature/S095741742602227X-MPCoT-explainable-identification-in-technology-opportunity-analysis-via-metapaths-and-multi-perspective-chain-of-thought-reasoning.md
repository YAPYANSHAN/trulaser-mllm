# MPCoT: explainable identification in technology opportunity analysis via metapaths and multi-perspective chain-of-thought reasoning

- **Citation (IEEE):** H. Li, H. Liang, Y. Wang, et al., "MPCoT: explainable identification in technology opportunity analysis via metapaths and multi-perspective chain-of-thought reasoning," *Expert Systems With Applications*, vol. 331, Art. no. 133318, 2026, doi: 10.1016/j.eswa.2026.133318.
- **Domain:** Technology/innovation management; patent analytics; explainable heterogeneous GNNs + LLM natural-language explanation.
- **Relevance to FYP (1-5):** 2 - Unrelated application, but the architecture (black-box predictor, then structural evidence extraction, then RAG + multi-perspective CoT LLM explanation evaluated by LLM judges and humans) maps well onto explaining a fault classifier's output.

## Problem
Technology opportunity analysis (TOA) predicts which technologies (IPC codes) may converge but does not explain why or how. HGNN-based TOA models are black boxes, reducing trust and hiding flaws.

## Data & modalities
Text/graph. 13,517 LLM-related patents (incoPat, 2010-2023) plus cited patents and papers (Scopus), built into a technology heterogeneous graph (co-occurrence, affiliation, citation). Structured knowledge base: IPC classification annotations, patent and paper titles/abstracts. Link prediction split 8:1:1 with random negative samples.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
(1) Pre-trained THGNN-TCP (static mode) HGNN predicts technology convergence links via metapaths. (2) Metapath explanation: extract the instance's computational graph, learn approximate discrete masks over metapath instances via Gumbel-Softmax reparameterization (K=30, penalty 0.05) maximising mutual information with the original prediction. (3) Natural-language explanation: RAG over the structured knowledge base (keyword lookup by IPC code; no vector search needed since data are structured) supplies DeepSeek-V3 with domain context; three-perspective CoT (CN2 into CN1, CN1 into CN2, convergence into a third technology), four steps each, with step-wise self-verification (choose between a correct and incorrect perspective, correct and re-verify); final prompt extracts implementation paths + reasons as JSON. No fine-tuning.

## Results (key numbers and metrics)
- TOA model: AUC 0.942, AP 0.901, F1 0.771.
- Metapath explanations best on both fidelity metrics (accuracy and probability fidelity) vs. GNNExplainer, PGExplainer, PaGE-Link, xPath, CI-Path (1,000 sampled positive links).
- 900 explanations rated on a 4-level scale by three LLM judges (DeepSeek-R1-0528, Doubao-Seed-1.6-Thinking, Gemini-2.5-Pro) and nine experts; strong Kendall concordance. With metapath evidence: AI 3.589 +/- 0.790, human 3.157 +/- 0.915; without: AI 2.886 +/- 0.446, human 2.684 +/- 0.636.

## Limitations
Metapath types defined manually; prompting only, no domain fine-tuning; node features and complex correlations not fully used in explanations; no ground-truth explanations; single domain dataset.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** Feed the LLM the *evidence that drove the predictor* (e.g., top SHAP features or KG paths from parameter to defect) rather than letting it explain freely - evidence-informed prompts scored ~0.5-0.7 higher.
- **Text/RAG:** For structured machine tables, retrieval can be exact keyword/ID lookup (e.g., by alarm code, material, nozzle) instead of embeddings.
- **LLM reasoning:** Multi-perspective CoT (material/parameter view, machine-condition view, operator/process view) with step-level self-verification before producing JSON recommendations.
- **Evaluation:** 4-level rubric (infeasible / plausible but unsupported / supported / fully justified), multiple LLM judges plus blinded experts with Kendall's W for agreement.
- **Fusion/KG:** A heterogeneous graph of jobs, parameters, defects and alarms with metapaths could ground explanations.
