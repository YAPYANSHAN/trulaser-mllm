# A benchmark multimodal oro-dental dataset for large vision-language models (COde)

- **Citation (IEEE):** H. Lv, I. Haq, J. Du, et al., "A benchmark multimodal oro-dental dataset for large vision-language models," *Scientific Data*, vol. 13, art. 990, 2026, doi: 10.1038/s41597-026-07342-9.
- **Domain:** Medical (dental) multimodal dataset / VLM fine-tuning
- **Relevance to FYP (1-5):** 3 - medical domain, but the pipeline (heterogeneous images + structured/text records -> LoRA-tuned Qwen-VL for classification and report generation) maps directly onto FYP images + machine records -> diagnostic report.

## Problem
There is a shortage of large public multimodal dental datasets suitable for training VLMs; existing ones contain only radiographs or lack textual diagnostic records.

## Data & modalities
COde: 8,775 checkups from 4,800 patients (2018-2025, ages 10-90); 50,000 intraoral photographs, 8,056 radiographs (panoramic, periapical, CBCT converted to 2D slices) and textual records (diagnosis, treatment plan, follow-up), converted to tabular form. Text translated Chinese to English, teeth numbers normalised to FDI, privacy cleaning with random IDs, expert verification. Released as CSV/JSON and ShareGPT format.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- LLMs used in preprocessing for translation and disease-name extraction/normalisation.
- Synthetic QA queries written for two benchmarks: (1) classification of six oro-dental anomalies; (2) full diagnostic report generation from multimodal inputs.
- Fine-tuned Qwen-VL 3B and 7B with LoRA adapters on all transformer blocks (A800 GPUs; 3 epochs, cosine LR). Baselines: base models zero-shot and GPT-4o (including few-shot prompting).
- Augmentation: randomised image order, random assignment of QA pairs per record.

## Results (key numbers and metrics)
- Classification: fine-tuned Qwen-7B accuracy 78.92%, F1 79.39%; GPT-4o best baseline at ~55.83% accuracy; Qwen-3B zero-shot lowest at 48.97% accuracy / 49.93% F1.
- Report generation (BLEU, METEOR, cosine similarity): fine-tuned Qwen-7B average similarity 71.46%; GPT-4o few-shot was the most faithful baseline.

## Limitations
Single clinical centre (local practices, imaging protocols, documentation style); possible demographic/socioeconomic bias; evaluation uses automatic text metrics.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** follow the COde workflow: normalise identifiers (e.g., job/part IDs, material codes), convert machine logs to tabular form, LLM-assisted normalisation of free-text fault notes, anonymise operator data, export to ShareGPT for VLM tuning.
- **Fusion / LLM reasoning:** feed multiple images per case (several cut-part photos) plus a serialised record of process parameters into Qwen-VL; randomise image order as augmentation for robustness.
- **Fine-tuning:** LoRA on Qwen-VL 3B/7B is feasible on modest GPUs; compare against GPT-4o zero/few-shot as baselines, as done here.
- **Evaluation:** two-task benchmark design (defect classification + full diagnostic report generation) with accuracy/F1 and BLEU/METEOR/embedding similarity.
- **Robustness:** LMMs can still infer with missing modalities, useful when some jobs lack images.
