# Evaluating Multimodal LLMs for Context-Aware Forensic Image Interpretation

- **Citation (IEEE):** T. Fedynyshyn, O. Partyka, I. Opirskyy, et al., "Evaluating Multimodal LLMs for Context-Aware Forensic Image Interpretation," *Int. J. Netw. Distrib. Comput.*, vol. 14, art. 23, 2026, doi: 10.1007/s44227-026-00102-6.
- **Domain:** Digital forensics — MLLM image interpretation plus agentic orchestration
- **Relevance to FYP (1-5):** 4 — the domain differs, but it is one of the clearest demonstrations of turning a high-recall, low-precision MLLM classifier into an evidence-grounded, auditable multi-agent pipeline (detector tools + OCR + retrieval + cross-check + abstention). The design can be reused for defect diagnosis.

## Problem
Forensic analysts must review huge volumes of phone images. The task is to detect military personnel, which requires distinguishing them from military-themed mannequins and civilians, and to attribute country and unit. Monolithic MLLM inference over-generalises: high recall but many false positives.

## Data & modalities
434 mobile-device images (military personnel, mannequins, civilians), with EXIF/provenance metadata. Inputs are images plus text prompts, with OCR text from insignia patches.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Baselines:** single-pass prompting of Gemini 1.5 Pro, LLaVA and GPT-4o via LangChain, asking for scene description, military presence, country and unit.
- **Agentic layer** in two variants: CrewAI (conversational, collaborative) and LangGraph (deterministic DAG with JSON-schema-validated node I/O and local retries). Sub-agents:
  - ProvenanceAgent: EXIF and hash.
  - PerceptionAgent: YOLOv8 person/insignia boxes and Tesseract OCR.
  - MannequinAgent: texture, pose and eye cues; abstains if p(human) < 0.6–0.7.
  - AttributionAgent: OCR tokens plus CLIP retrieval against a curated insignia gallery. Country is emitted only if at least two independent signals agree.
  - CrossCheckAgent: detects contradictions, which force abstention.
  - ReportAgent: JSON/HTML audit reports.
- GPT-4o handles perception and attribution. GPT-4o-mini plus heuristics handle the mannequin and cross-check steps. All intermediate artefacts are persisted.

## Results (key numbers and metrics)
- **Single-pass baselines:**
  - Recall: Gemini 0.99, LLaVA 0.98, GPT-4o 0.91.
  - Precision: 0.69, 0.69, 0.67.
  - Accuracy: 0.793, 0.793, 0.770.
  - Country accuracy: Gemini 0.787, GPT-4o 0.385, LLaVA 0.121.
  - Unit recognition was weak for all models. Mannequins were the main error source.
- **Agentic variants:**
  - CrewAI: precision 0.88, mannequin false-positive rate 0.12, recall 0.74, country accuracy 0.58.
  - LangGraph: precision 0.90, false-positive rate 0.08, recall 0.73, country accuracy 0.62.
  - Recall fell because of deliberate abstention ("unknown").

## Limitations
Small single-task dataset. Recall drops under conservative abstention. Country accuracy in the agentic variants (0.58–0.62) is below Gemini's single-pass 0.787 (the reasons are not fully analysed). Unit recognition remains weak. Relies on proprietary models and a small curated gallery.

## Transferable ideas for the FYP pipeline
- **Vision:** pair the MLLM with specialised tools: a YOLO-style detector for defect regions (dross, burrs, scorch, incomplete cut), OCR for part labels and machine HMI screenshots, and CLIP retrieval against a curated gallery of reference defect images.
- **LLM reasoning/fusion:** add a "two independent signals" rule. Only emit a root cause when image evidence AND table/sensor evidence (or a manual passage) agree; otherwise output "uncertain". A cross-check agent flags contradictions (e.g., image shows dross but gas pressure is nominal).
- **Deployment:** a LangGraph DAG with JSON-schema-validated outputs and persisted intermediate artefacts gives reproducible, audit-ready diagnosis traces.
- **Evaluation:** report the precision/recall trade-off and abstention rate. Compare single-pass MLLM vs. the agentic pipeline as a key FYP ablation.
