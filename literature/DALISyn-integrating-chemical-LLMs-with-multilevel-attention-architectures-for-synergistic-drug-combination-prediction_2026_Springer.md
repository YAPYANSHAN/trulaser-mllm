# DALI-Syn: integrating chemical LLMs with multi-level attention architectures for synergistic drug combination prediction

- **Citation (IEEE):** H. Du, Y. Tian, W. Wang, et al., "DALI-Syn: integrating chemical LLMs with multi-level attention architectures for synergistic drug combination prediction," *Health Information Science and Systems*, vol. 14, art. 49, 2026, doi: 10.1007/s13755-026-00441-2.
- **Domain:** Bioinformatics / drug discovery (cancer drug-combination synergy prediction).
- **Relevance to FYP (1-5):** 1 — unrelated domain; only the pattern of a frozen domain foundation-model encoder + symmetric cross-attention with a tabular feature vector is transferable.

## Problem
Predicting synergistic drug pairs for cancer therapy. Graph-based methods capture only local topology of molecules (over-smoothing, weak long-range context) and shallow fusion misses drug-cell line interactions.

## Data & modalities
SMILES strings (from PubChem) for drugs and gene-expression vectors for cell lines (CCLE, 977 LINCS landmark genes). O'Neil dataset: 22,737 samples, 38 drugs, 39 cell lines; Loewe score >30 = synergy, <0 = antagonism, 0-30 discarded, giving 10,650 samples (1,973 positive / 8,677 negative). Independent AstraZeneca test set: 668 pairs, 57 drugs, 24 cell lines, no overlap.

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
ChemBERTa-2 (RoBERTa-based chemical language model, base version) produces [CLS] embeddings of SMILES. Dynamic Multi-scale Convolution (DMC) and multi-head self-attention refine drug and cell-line features locally and globally. A symmetric, parameter-sharing cross-attention module performs bidirectional drug<->cell-line fusion before a classifier. Attention maps used for interpretation. No generative LLM, RAG, or prompting; GPT-4 comparison explicitly omitted.

## Results (key numbers and metrics)
O'Neil benchmark: AUC 0.970 (vs 0.943 second-best) and AUPR 0.908, beating MFSynDCP, DeepDDS, DeepSynergy, XGBoost/RF. AstraZeneca independent set: AUC 0.84, ACC 0.78, F1 0.85, AUPR 0.91 (relative gains of 16%/14%/13% over DeepDDS series). Ablation: replacing ChemBERTa-2 with Morgan fingerprints or a GAT encoder reduced performance.

## Limitations
Class imbalance and label noise; no external biological networks (drug-protein, PPI); no comparison with general LLMs because no mature pathway exists for feeding heterogeneous structured data into text LLMs.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series + fusion:** Pair a pretrained domain encoder (e.g., a text encoder over alarm messages or a vision encoder over cut-edge images) with an MLP/attention encoder for machine-parameter vectors, fused through symmetric cross-attention — a lightweight alternative or complement to pure LLM fusion.
- **Data ingestion:** Their removal of ambiguous "near-zero" labels suggests excluding borderline quality grades when training a defect classifier, to sharpen class boundaries.
- **Evaluation:** Use AUPR alongside AUC for imbalanced fault classes, and an independent, non-overlapping test set (e.g., different material/thickness jobs) to test generalisation.
- **LLM reasoning:** Their stated gap — interfacing structured numeric data with text LLMs — is exactly what the FYP addresses; cite as motivation.
