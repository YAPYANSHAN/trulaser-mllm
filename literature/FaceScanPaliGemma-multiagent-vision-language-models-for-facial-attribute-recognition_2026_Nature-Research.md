# FaceScanPaliGemma multi-agent vision language models for facial attribute recognition

- **Citation (IEEE):** N. AlDahoul, M. J. T. Tan, H. R. Kasireddy, et al., "FaceScanPaliGemma multi-agent vision language models for facial attribute recognition," *Sci. Rep.*, vol. 16, art. 10246, 2026, doi: 10.1038/s41598-026-39584-3.
- **Domain:** Computer vision — facial attribute recognition with fine-tuned small VLM agents
- **Relevance to FYP (1-5):** 3 — unrelated domain, but a strong blueprint for an agentic system of small, task-specialised, LoRA/QLoRA-fine-tuned VLMs routed by a small LLM. These specialists beat zero-shot GPT-4o/Gemini at a fraction of the cost. Applicable to defect-type and defect-location agents.

## Problem
Facial attribute classification (race, gender, age, emotion) is hard because of subjectivity and high variation within classes. General VLMs used zero-shot underperform, and monolithic models are costly. The paper argues for specialised small models in an agentic design.

## Data & modalities
FairFace (86,744 training images; race, gender, age group) and AffectNet (emotion). Inputs are images plus a text prompt listing the categories.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Four PaliGemma-3B agents, each fine-tuned for one attribute.
- An **analysis agent** (Llama-3.2-3B) parses the user query into steps and routes images.
- A generic PaliGemma **face-detection agent** extracts the faces that match the prompt (e.g., by posture or action).
- The specialist agents classify each face against a category list, and results return to the analysis agent for the final answer. The workflow is sequential.
- **Fine-tuning:** LoRA rank 4 under 4-bit NF4 quantisation (QLoRA-style), learning rate 2e-5, batch size 2 with gradient accumulation, Adam, linear schedule with warm-up, 5 epochs.
- **Baselines:** GPT-4o, GPT-4o-mini, Gemini 1.5 Flash, LLaVA(-Next) and base PaliGemma, all zero-shot, plus CLIP zero-shot and CNN state of the art.

## Results (key numbers and metrics)
- Accuracy: race 81.1%, gender 95.8%, age group 80.0% (FairFace), emotion 59.4% (AffectNet; F1 59%).
- Outperforms all zero-shot VLMs, with the best accuracy and F1 among VLMs for race, gender and age.
- Emotion falls below specialised state of the art trained on far larger data (e.g., FMAE pre-trained on Face9M, POSTER++).
- Inference takes 0.135 s per face (~7 fps) on an A100 80 GB. Models are open-sourced.

## Limitations
Prompt design was not explored exhaustively. Not evaluated under real-world lighting, occlusion or noise. No explainability (no rationale or saliency). Ethical sensitivity of demographic attribute recognition. Emotion performance lags dedicated models.

## Transferable ideas for the FYP pipeline
- **Vision / fine-tuning:** rather than one large MLLM, fine-tune small open VLMs (PaliGemma-3B class) with QLoRA (r=4, 4-bit) as specialist agents. Possible agents: defect-type classifier, cut-edge quality grader, part-region detector. This is feasible on a single GPU.
- **LLM reasoning / orchestration:** a small router LLM decomposes operator questions ("why is there dross on the bevel edge of part 12?") and dispatches the relevant image region to the right specialist. Results are then merged with table evidence.
- **Detection then classification:** first localise the region of interest (defect or edge), then classify the crop. This mirrors face detection followed by attribute agents.
- **Evaluation:** compare fine-tuned specialists against zero-shot GPT-4o/Gemini baselines and report latency (frames per second) for inline deployment.
- **Gap to address:** add rationale generation or saliency, since explainability is a stated weakness here.
