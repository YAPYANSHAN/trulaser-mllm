# Bridging the domain gap for VLMs: A scientific fine-tuning framework for precision and pedagogy in astronomical image understanding

- **Citation (IEEE):** L. Li, J. Liu, S.-K. Yeung, et al., "Bridging the domain gap for VLMs: A scientific fine-tuning framework for precision and pedagogy in astronomical image understanding," *Computers and Education: Artificial Intelligence*, vol. 11, Art. no. 100673, 2026, doi: 10.1016/j.caeai.2026.100673.
- **Domain:** AI in education (space/astronomy); domain adaptation of vision-language models.
- **Relevance to FYP (1-5):** 3 - Non-industrial domain, but it is a compact, reproducible recipe for LoRA fine-tuning a small open VLM (Qwen3-VL-4B) on ~10k domain images with LLM-generated structured text, on a single GPU - directly reusable for cut-part/defect images.

## Problem
Educational VLM use mostly invokes general models directly; there is no systematic fine-tuning methodology for discipline-specific visual corpora. General VLMs give surface-level, imprecise descriptions of specialised images.

## Data & modalities
Images + structured text. 5,181 raw astronomy images crawled from NASA China portal, ESA, CASC, CNSA, Wikimedia Commons; augmentation (rotation, colour perturbation, local cropping) adds 4,873, giving 9,838 validated images. Text generated with the DeepSeek API in a four-level Bloom's-taxonomy structure: Description, Explanation, Connection, Extension (with prompt constraints on difficulty/content).

## Method (encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Qwen3-VL-4B-Instruct fine-tuned with LoRA (attention and FFN) via LlamaFactory on an NVIDIA RTX 5090 (32 GB); batch 2, gradient accumulation 8, max grad norm 1.0, 3 epochs, lr 5e-5 cosine, 5% validation split; stopped at 900 steps (loss 2.7634 to 1.3137, -52.46%). No RAG. Evaluation: 909 test images (303 original + 303 rotated + 303 colour-perturbed), six paraphrased queries, automated key-information extraction and pairwise comparison vs. base model; classroom pilot with 7-point Likert questionnaire.

## Results (key numbers and metrics)
- Overall accuracy 62.2% to 91.3% (+29.1 pp); originals 63.0% to 91.4%; rotated 62.4% to 89.4%; colour-perturbed reached 93.1%.
- Fine-tuned model better than baseline in 858 samples (94.4%) of pairwise comparisons.
- 156 seventh-grade students: usability 6.51, recognition accuracy 6.22, learning utility 6.34 (out of 7); positive rates 92.9%, 86.5%, 89.7%.

## Limitations
Synthetic LLM text without systematic expert scientific validation; augmentation matched to the test perturbations (inflates robustness claims); accuracy/loss are indirect outcome measures; single 4B model and single domain; hallucination risks acknowledged; data not public.

## Transferable ideas for the FYP pipeline
- **Vision / LLM fine-tuning:** Same recipe for the FYP: LoRA on Qwen3-VL-4B (or similar) using cut-part/defect photos paired with structured text; fits a single 32 GB GPU; LlamaFactory simplifies training.
- **Data ingestion:** Generate training text from documentation with an LLM in a fixed hierarchical schema - e.g., Observation (defect seen) / Cause (parameter or machine condition) / Evidence (table values, manual section) / Action (parameter change) - then have a TRUMPF-experienced reviewer validate a sample.
- **Evaluation:** Test with paraphrased queries and image perturbations (lighting, rotation) but keep perturbations distinct from training augmentations; pairwise base-vs-fine-tuned comparison; operator Likert usability study.
- **Deployment:** A 4B model is feasible on-premise for shop-floor use.
