# Illusion of competence: vision-language models provide confident but inaccurate explanations in cytological diagnostics

- **Citation (IEEE):** I. Kukuljan, M. F. Dasdelen, J. Schäfer, et al., "Illusion of competence: vision-language models provide confident but inaccurate explanations in cytological diagnostics," *Scientific Reports*, vol. 16, art. 20526, 2026, doi: 10.1038/s41598-026-60372-6.
- **Domain:** Medical imaging (cytomorphology) / VLM benchmarking and explainability
- **Relevance to FYP (1-5):** 4 - a cautionary benchmark showing general VLMs (GPT-4o, Gemini, Llama-3.2) fail at fine-grained visual classification and give ungrounded explanations; directly informs whether to rely on a VLM vs a dedicated vision model for laser-cut defect images.

## Problem
Are generalist and biomedical large vision-language models (LVLMs) accurate, generalisable and trustworthy (grounded explanations) for fine-grained cell classification and morphology assessment?

## Data & modalities
Images + text prompts. HiCervix (40,229 cervical cells, 29 classes), Acevedo (17,092 peripheral blood WBC images, 11 classes), BMC (171,373 bone-marrow cells, 21 classes), WBCAtt (10,300 images, 11 morphological attributes), MLL23 (>40,000 images, 18 classes; external out-of-domain test). Test: 50 images/class; few-shot: one image per class; fine-tuning: up to 200 images/class (Acevedo).

## Method
Benchmarked GPT-4o, Gemini-2.0-flash, Llama-3.2-11B multimodal, DeepSeek-VL2-small (2.8B), and biomedical LLaVA-Med, CONCH, BiomedCLIP under zero-shot (image + label list, "analyse features before deciding") and few-shot (one labelled exemplar per class in the prompt) prompting. Fine-tuned GPT-4o (OpenAI fine-tuning API) vs an MLP head on DINOv2 and the hematology foundation model DinoBloom-S (22M). Explanations rated by an expert cytomorphologist (1 excellent - 5 misleading); also tested VLM segmentation of cell structures and identification of decision-relevant regions.

## Results
Zero-/few-shot near random: GPT-4o peripheral blood F1 0.22 ± 0.02 zero-shot, 0.36 ± 0.03 few-shot; models defaulted to majority classes. Fine-tuned GPT-4o: 0.55 (10/class), 0.65 (50), 0.74 (100), then plateaued; DinoBloom+MLP: 0.79, 0.86, 0.87 at the same sizes. Out-of-domain MLL23 at n=200: DinoBloom 0.54 vs GPT-4o 0.50; zero-shot GPT-4o 0.19 (random 0.10). Explanations: correct cases 1.1 ± 0.3, wrong cases 2.8 ± 1.4, with 30% rated poor/misleading - textbook descriptions not grounded in the image. Smaller VLMs failed with multi-image few-shot prompts (context limits).

## Limitations
Single domain (cytology); limited test size (50/class); closed models' versions change over time; expert rating by one assessor on a sample; only GPT-4o fine-tuned among VLMs.

## Transferable ideas for the FYP pipeline
- **Vision:** do not rely on zero-shot GPT-4o-class VLMs to classify subtle cut-quality defects (dross, striation, burr, bevel-angle deviation); use a dedicated encoder (e.g., DINOv2 features + small head) as the primary classifier and feed its label/confidence to the LLM.
- **LLM reasoning:** require explanations to cite measurable evidence (detected region, numeric parameter values) rather than generic laser-cutting textbook knowledge; penalise ungrounded rationales.
- **Evaluation:** include zero-shot, few-shot and fine-tuned baselines, an out-of-domain test (different material/thickness or machine), majority-class bias checks, and expert Likert scoring of explanation faithfulness.
- **Data:** learning curves show ~100 labelled images per class can saturate a foundation-model head - useful for planning defect-image collection.
