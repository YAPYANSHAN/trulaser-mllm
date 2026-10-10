# Exploring teacher-student interaction through multimodal large language models: an empirical investigation

- **Citation (IEEE):** G. Chen, G. Han, J. Niu, et al., "Exploring teacher-student interaction through multimodal large language models: an empirical investigation," *Sci. Rep.*, vol. 16, art. 7602, 2026, doi: 10.1038/s41598-026-38626-0.
- **Domain:** Educational technology — classroom behaviour analysis with a fine-tuned MLLM
- **Relevance to FYP (1-5):** 3 — unrelated domain, but a compact, reproducible recipe for LoRA fine-tuning a small open VLM (VisualGLM-6B) on a few thousand annotated images to output both a class label and a structured explanation. It is close in scale to an FYP defect-image dataset.

## Problem
Manual classroom observation of teacher–student interaction is slow and subjective. Classical ML captures only single behaviours. Can a fine-tuned MLLM classify interaction types and describe them interpretably?

## Data & modalities
30 open-platform classroom videos (Smart Education of China). Keyframes give 2,380 annotated images: guided 737, collaborative 485, questioning 321, independent 359, exhibitive 477. Each image has a text annotation describing teacher behaviour, student behaviour and image features, plus the interaction type. Image plus text only (no audio).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Base model: VisualGLM-6B (a BLIP-2 visual encoder bridged to ChatGLM-6B).
- **Two-step LoRA:**
  1. LoRA on the BLIP-2 image layers.
  2. LoRA with rank 10 added to ChatGLM layers 1 and 12.
- Hyperparameters: max source length 64, max target length 256, batch size 8, learning rate 1e-4, 1,000 iterations.
- Prompt engineering defines the five categories and requires a structured output (type plus teacher/student/image descriptions).
- Deployed as a Streamlit video-analysis app.
- Evaluation: confusion matrix, BERTScore (P/R/F1) between generated and reference descriptions, and qualitative comparison with experts.

## Results (key numbers and metrics)
- Overall accuracy: 82%. Best on guided, independent and exhibitive interactions. Collaborative and questioning were the hardest.
- BERTScore F1 per description:
  - Guided: teacher 0.733, student 0.707, image 0.764.
  - Collaborative: lower (teacher 0.664, student 0.633, image 0.636).
  - Questioning: lowest score for teacher behaviour.
- Outputs were more structured and interpretable than expert annotations, but misclassifications and hallucinations persisted.

## Limitations
Small dataset from 30 videos. No audio. Overlapping interaction types confuse the model. Some hallucination. Baseline comparison is limited to a qualitative before/after fine-tuning comparison (the un-tuned model hallucinated actions such as writing on a board); no other VLMs were benchmarked. Single annotation source.

## Transferable ideas for the FYP pipeline
- **Vision / fine-tuning:** a two-stage LoRA (vision adapter first, then low-rank adapters in selected LLM layers) on ~2k labelled images is feasible on modest GPUs. Apply this to cut-part and defect photos with labels (burr, dross, striations, discolouration, incomplete cut) and short structured explanations.
- **Annotation schema:** pair each image with a structured target: defect type, visual evidence description and suspected cause. This lets the model learn to explain, not just classify.
- **Evaluation:** combine a confusion matrix for the class label with BERTScore (or an LLM judge) on the explanation text against expert write-ups. Expect visually similar or overlapping classes to be hardest.
- **Deployment:** a Streamlit front end is a quick way to demonstrate the operator-facing diagnosis tool.
