# SADL: sampling, deliberation, and pseudo-labeling for in-context learning in compositional visual question answering

- **Citation (IEEE):** L. H. Dang, T. M. Le, V. Le, et al., "SADL: sampling, deliberation, and pseudo-labeling for in-context learning in compositional visual question answering," *Discover Artificial Intelligence*, vol. 6, Art. no. 658, 2026, doi: 10.1007/s44163-026-01411-z.
- **Domain:** Vision-language reasoning / prompting (general VQA)
- **Relevance to FYP (1-5):** 3 - general-domain, but it gives a training-free recipe (retrieve similar image examples, decompose the question, few-shot prompt a VLM) that applies directly to defect-image QA with little labelled data.

## Problem
Large vision-language models (LVLMs) can do in-context learning (ICL) for visual QA from a few image-question-answer demonstrations. Designing good multimodal prompts for *compositional* questions is poorly understood, though. Language-only techniques such as chain-of-thought (CoT) and least-to-most (L2M) gave only minimal gains over vanilla few-shot prompting in the authors' preliminary tests.

## Data & modalities
Images plus natural-language questions from four public benchmarks: GQA, GQA-OOD (head/tail split), CLEVR and CRIC.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Inference only, with frozen parameters:
1. **Sampling:** retrieve training image-question pairs that are semantically close to the query using CLIP (ViT) similarity. This is retrieval-augmented demonstration selection.
2. **Deliberation:** an LLM (Vicuna 13B) decomposes the complex question into a chain of subquestions.
3. **Pseudo-labelling:** the same LVLM (OpenFlamingo) answers the subquestions one at a time to build pseudo-labels for the demonstrations. A correction step compares the final pseudo-answer with the known ground truth for the demonstration.
4. The annotated demonstrations form the few-shot prompt for the query.

## Results (key numbers and metrics)
- GQA: 47.11% overall accuracy vs. 44.59% for ZPVQA, about 7 points above vanilla few-shot.
- CRIC: 39.47% vs. 36.00% for ZPVQA.
- GQA-OOD: 35.46% vs. 32.24%. On the tail split, 27.82% vs. 23.13%.
- CLEVR: 41.14% overall.
- Ablations on CRIC:
  - Random samples instead of similar ones: about -12 points.
  - No question decomposition: 26.54%.
  - Subquestion labels all set to "unknown": 16.83%.
  - No correction step: 36.21%.

## Limitations
- Uses one open LVLM (OpenFlamingo) and one decomposition LLM (Vicuna 13B). It inherits Flamingo's hallucinations and ungrounded assumptions.
- Inference cost grows with the number of shots and LVLM calls.
- Absolute accuracies are modest, and the method is tested only on general VQA benchmarks.

## Transferable ideas for the FYP pipeline
- **Vision / RAG:** use CLIP-style image-embedding retrieval to pull the most similar historical defect images (with their known causes and parameters) into the VLM prompt as few-shot demonstrations. The paper finds similarity-based sampling is critical, worth about 12 points.
- **LLM reasoning:** split a diagnosis question such as "why is there dross on this bevel cut?" into subquestions (defect type → location → related parameters → likely cause). Answer them step by step with evidence from images and tables.
- **Data:** when labels are scarce, generate pseudo-labels for intermediate reasoning steps and anchor them to known final labels. Label quality matters: noisy pseudo-labels collapse performance.
- **Evaluation:** use the same ablation structure (retrieval on/off, decomposition on/off) in the FYP. Watch the inference cost per query.
