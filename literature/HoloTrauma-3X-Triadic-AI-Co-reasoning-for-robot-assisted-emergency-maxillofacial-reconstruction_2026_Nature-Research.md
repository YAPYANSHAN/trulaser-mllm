# HoloTrauma 3X: Triadic AI co-reasoning for robot-assisted emergency maxillofacial reconstruction

- **Citation (IEEE):** Q. Zhou, Y. Liu, C. Wang, et al., "HoloTrauma 3X triadic AI co-reasoning for robot assisted emergency maxillofacial reconstruction," *npj Digital Medicine*, vol. 9, Art. no. 439, 2026, doi: 10.1038/s41746-026-02573-x.
- **Domain:** Medical AI: emergency maxillofacial trauma surgical planning using multimodal 3D imaging, VLM-LLM co-reasoning with RAG, and robotic trajectory planning.
- **Relevance to FYP (1-5):** 3 - the domain is unrelated, but the architecture (multimodal encoder -> structured visual description -> domain-knowledge RAG -> LLM priority-ranked reasoning -> parameter extraction with confidence gate) closely mirrors the FYP's planned pipeline.

## Problem
Emergency facial trauma requires simultaneous assessment of airway, bone and occlusion within minutes. Conventional virtual surgical planning takes 3-5 days and evaluates structures sequentially; modalities (CBCT, dental scans, radiographs) are not jointly analysed; decisions are rarely grounded in formal guidelines.

## Data & modalities
CBCT volumes (512^3), dental cast point clouds (18,384 points), cephalometric radiographs, clinical measurements. 8427 trauma patients from public datasets (12 institutions) + 3 hospitals; 847 acute emergency cases analysed in detail; 347 robot-assisted cases for the motion planner. Knowledge base of 15,400 documents (ATLS protocols, trauma guidelines, complication models).

## Method
- **Triadic encoder:** 3D volumetric transformer (10 layers, 512-D) + PointNet++ + ResNet-34 with spatial attention -> cross-modal transformer fusion with modality weights -> 1024-D feature (8.3 s).
- **VLM-LLM co-reasoning (12.7 s):** fine-tuned CLIP ViT-L/14 projection -> 6-layer vision-to-language decoder with a 4,800-term trauma vocabulary producing structured injury descriptions -> PubMedBERT dense retrieval over FAISS (top-7 passages, 127 ms) -> GPT-4-Turbo (temperature 0.3) priority-ranked reasoning -> parser extracting numeric plan parameters plus a confidence score; Cconf < 0.75 is flagged for senior-surgeon review.
- **Optimisation and planning:** priority-weighted loss (airway 10, stabilisation 5, occlusion 2, aesthetics 1) with Adam; RRT* robot path planning.
- **Privacy:** only de-identified structured descriptors are sent to the LLM API.
- **Validation:** patient-level 5-fold CV, leave-one-centre-out, 3 seeds.

## Results
- Positional MAE 0.42 mm (maxilla) / 0.38 mm (mandible); airway volume MAE 1.47 cm^3 (31.2% better than GPT-4V-Emergency, 2.14).
- 94.7% postoperative Class I occlusion; condylar MAE 0.51 mm.
- 31.4% less operation time and 42.3% fewer complications than conventional methods.
- Ablation: no triadic fusion raised maxillary MAE to 0.54 mm and airway error to 2.83 cm^3; replacing VLM-LLM reasoning with direct regression gave MAE 0.48 mm and lost interpretability. Surgeons reported needing the reasoning traces to trust the plan.
- Most planning time is the optimiser (2.3 min); the LLM accounts for only 5.6%.

## Limitations
Geographic and demographic diversity (e.g., paediatric cases) is limited; the robot component is validated on only 347 cases; the study is retrospective (prospective trials pending); it depends on a cloud LLM API (latency, governance); results are strikingly high and not yet prospectively confirmed.

## Transferable ideas for the FYP pipeline
- **Vision -> text/RAG:** Turn visual and sensor findings into a *structured, controlled-vocabulary description* (e.g., "bottom dross, 0.4 mm height, left contour, 15 mm S355") before retrieval, then query the TruLaser manuals and parameter tables with that description.
- **Text/RAG:** Use a domain encoder plus FAISS top-k retrieval with timing budgets; build a curated knowledge base (manuals, cutting-parameter charts, maintenance guides).
- **LLM reasoning:** Prompt for priority-ranked recommendations (safety -> machine protection -> quality -> throughput), then parse them into numeric parameter changes (power, speed, focus, gas pressure).
- **Deployment:** Add a confidence gate that routes low-confidence outputs to a human engineer, and send only de-identified structured data to cloud LLMs.
- **Evaluation:** Ablate "fusion vs separate encoders" and "LLM reasoning vs direct regression", and report both accuracy and user trust and acceptance.
