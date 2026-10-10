# Responsible AI in healthcare: Mitigating hallucinations and enhancing multimodal fusion-based reasoning in medical imaging

- **Citation (IEEE):** S. Iqbal, X. Zhong, M. A. Khan, et al., "Responsible AI in healthcare: Mitigating hallucinations and enhancing multimodal fusion-based reasoning in medical imaging," *Information Fusion*, vol. 136, Art. no. 104483, 2026, doi: 10.1016/j.inffus.2026.104483.
- **Domain:** Medical imaging / medical large vision-language models (hallucination mitigation, uncertainty)
- **Relevance to FYP (1-5):** 3 - a different domain, but it addresses exactly the FYP's core risks for a VLM: image + text fusion, retrieval-grounded reasoning, calibrated uncertainty and hallucination metrics.

## Problem
Medical LVLMs hallucinate, meaning their outputs are inconsistent with the image or clinical facts. They are also overconfident and misalign features across heterogeneous modalities (images, notes, reports). Privacy and dataset heterogeneity limit scalability.

## Data & modalities
- Inputs: medical images (X-ray, CT, MRI), radiology reports and clinical notes.
- Knowledge sources such as PubMed and UMLS.
- Evaluated across multiple medical benchmark datasets for report generation and VQA, with hallucination benchmarks POPE and CHAIR. Code and data are released ("MLVLM").

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Base model:** LLaVA-Med, extended with three modules.
- **RAR (retrieval-augmented reasoning):** a teacher model retrieves expert-validated knowledge snippets (biomarkers, differential diagnoses). A student is then distilled to answer without retrieval at inference time.
- **CMCL (cross-modal contrastive learning):** aligns image and text embeddings. Text uses BioBERT combined with medical-ontology embeddings.
- **UMR (Unified Multimodal Reasoning) platform:** attention-driven fusion, dynamic modality weighting and hierarchical interaction modelling across images, notes and reports. It also supports human-in-the-loop validation and temporal context.
- **Uncertainty and calibration:** Bayesian uncertainty quantification, deep ensembles, Dirichlet-based calibration and temperature scaling.
- **New metrics:** Clinical Consistency Score (CCS), Hallucination Rate Reduction (HRR) and Cross-Modal Alignment Index (CMAI).

## Results (key numbers and metrics)
Compared with LLaVA-Med, the variants (+RAR, +CMCL, +UMR) achieve:
- BertScore +0.05 to 0.1
- BLEU +3 to 5
- METEOR +0.03 to 0.05
- ROUGE +0.02 to 0.05
- CMAI +10-15% (cross-modal alignment)
- HRR: 15-20% lower hallucination rate
- CCS +0.03 to 0.07

## Limitations
- The authors acknowledge limited interpretability, high computational complexity and data bias.
- Extensive clinical validation is still needed.
- Several metrics are newly defined by the authors, so they are hard to compare with other work.
- Gains are reported mostly as ranges, with no per-dataset detail in the abstract.

## Transferable ideas for the FYP pipeline
- **Fusion:** dynamic modality weighting between defect images, machine-table features and documentation snippets. Down-weight a modality when it is missing or low-quality.
- **Text/RAG:** a teacher-with-retrieval / student-without-retrieval distillation could produce a lighter on-premise model that keeps grounded behaviour.
- **LLM reasoning:** attach calibrated confidence to every diagnosis (deep ensembles or MC sampling plus temperature scaling), and route low-confidence cases to a human (human-in-the-loop).
- **Evaluation:** adapt CCS, HRR and CMAI to the laser domain, e.g., a "process consistency score" against the TRUMPF manuals and an image-text alignment index. Use POPE/CHAIR-style probing to check whether the VLM invents defects that are not in the image.
