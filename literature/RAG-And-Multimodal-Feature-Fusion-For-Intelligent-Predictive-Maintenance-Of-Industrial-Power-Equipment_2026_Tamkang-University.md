# RAG And Multimodal Feature Fusion For Intelligent Predictive Maintenance Of Industrial Power Equipment

- **Citation (IEEE):** H. Yang, X. Meng, H. Yu, et al., "RAG And Multimodal Feature Fusion For Intelligent Predictive Maintenance Of Industrial Power Equipment," *Journal of Applied Science and Engineering*, vol. 33, art. 26033066, 2026, doi: 10.6180/jase.202610_33.066.
- **Domain:** Industrial fault diagnosis / predictive maintenance — power equipment, multimodal LLM + RAG
- **Relevance to FYP (1-5):** 5 — an end-to-end industrial pipeline combining a LoRA-tuned MLLM, multimodal knowledge-base RAG, a YOLO detector and a four-stage CoT that matches defects to standards. This is very close to the FYP architecture.

## Problem
Predictive maintenance faces three problems:
- heterogeneous maintenance knowledge spread across many equipment types and regulatory standards
- cross-modal gaps between textual fault reports and defect imagery
- knowledge bases that go stale without retraining

General LLMs hallucinate, single-pass RAG gives insufficient evidence, and CLIP-style models adapt poorly to equipment semantics.

## Data & modalities
- **Text:** a technical-supervision record set (2022–2024) of 3,097 records with 7 fields (problem description, violation basis, rectification suggestion, etc.). Records are classified by accident type (GIS, switchgear, transformer, …) and phase (construction, design, operation).
- **Multimodal:** 12,541 image–text pairs (2020–2024) covering 10 equipment components and 8 defect types (e.g. oil leakage, insulation cracks). The training set is augmented; the test set keeps the original annotations.

## Method
**Unimodal (text) branch:**
- A knowledge tree of standards (8 accident types × 4 phases), with GMM clustering and an inverted index.
- LLM-generated augmentation of violation cases.
- **MoE-LoRA** with gated top-K routing to domain experts (substation, transmission line), using under 0.5% of the base model's parameters.
- In-context example retrieval with RoBERTa-large embeddings (k=3).
- A **confidence-driven active retrieval agent** that fuses BM25 and Text2Vec retrieval and reflects over multiple rounds.
- Base LLMs: Qwen2.5-72B and DeepSeek-R1.

**Multimodal branch:**
- A DeViSE-style **cross-modal aligned knowledge base** trained with triplet loss.
- **YOLOv7** detections concatenated into the prompt.
- **Four-stage CoT:** image description → equipment localisation → defect identification → standard/rule matching.
- LoRA fine-tuning (r=128, α=256) of InternVL2.5-8B or Qwen2.5-VL-7B.
- Deployed with role-based access control on RTX 3090 GPUs.

## Results
- **Text branch (Qwen2.5-72B):** Hit@3 80.51%, Hit@5 83.54%, MRR 0.77. The Text2Vec baseline reached only Hit@3 65.01% and Hit@5 70.73%.
- **Text-branch ablations:** without the agent, Hit@3 is 71.32% and MRR 0.67; without MoE, MRR is 0.64.
- **Multimodal (InternVL2.5 full):** equipment accuracy 88.10%, defect accuracy 92.86%, overall 80.95%.
- **Multimodal comparisons:**
  - LoRA-only InternVL2.5: 66.67% overall.
  - Commercial models: Qwen2.5-VL 33.32%, GLM-4V 36.31%, Hunyuan-T1 21.23%.
  - Domain adaptation lifted Qwen2.5-VL from 33.32% to 71.43%.
- **Multimodal ablations (overall accuracy):** text-only input 60.51%, image-only 42.30%, without CoT 66.67%, without the multimodal KB 72.64%.
- **Latency:** response time under 2 s when deployed locally. The system is piloted at a provincial electric power research institute.

## Limitations
- Weak on rare defect categories with few samples.
- Synchronising the knowledge base at scale in real time is still slow.
- Depends on GPU servers, so compression is needed for edge deployment.
- Test-set size and statistical testing are not clearly reported. The accuracy values suggest a small test set.
- The paper lists its received date after its accepted date, a typo in the metadata.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** adopt the four-stage CoT almost directly for laser cutting: describe the cut image → localise the region (edge, bevel face, pierce point) → identify the defect → match it to the TruLaser manual's remedy or parameter table.
- **Vision:** add YOLO detections of defect regions to the VLM prompt.
- **Fine-tuning:** LoRA-tune an open VLM (InternVL2.5-8B or Qwen2.5-VL-7B) on labelled cut-part images. The paper shows large gains over zero-shot commercial models.
- **Text/RAG:**
  - Index manuals and fault codes hierarchically (machine subsystem × fault phase).
  - Use hybrid BM25 + dense retrieval with multi-round reflective retrieval until the evidence is sufficient.
  - Build a cross-modal knowledge base of past defect cases (image + resolution).
- **Evaluation:** report Hit@k/MRR for retrieval, per-stage accuracy for diagnosis, and latency. Run modality ablations (text-only vs image-only vs fused).
