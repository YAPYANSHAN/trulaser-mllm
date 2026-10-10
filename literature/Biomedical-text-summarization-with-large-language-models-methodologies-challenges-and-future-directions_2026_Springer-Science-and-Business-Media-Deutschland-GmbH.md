# Biomedical Text Summarization with Large Language Models: Methodologies, Challenges, and Future Directions

- **Citation (IEEE):** S. Mushtaq and K. Veningston, "Biomedical text summarization with large language models: methodologies, challenges, and future directions," *International Journal of Data Science and Analytics*, vol. 22, art. 29, 2026, doi: 10.1007/s41060-025-00956-z.
- **Domain:** Biomedical NLP / text summarization (systematic review)
- **Relevance to FYP (1-5):** 1 - biomedical text-only survey; transferable only for general points on domain adaptation (LoRA/PEFT), hallucination and evaluation metrics for generated text.

## Problem
Biomedical literature, clinical records and EHRs are growing faster than professionals can read them; the paper surveys how LLMs are used for extractive and abstractive biomedical summarisation and what blocks deployment.

## Data & modalities
Systematic review following PRISMA over PubMed, Scopus, IEEE Xplore and ACM Digital Library, 2016-2024: 113,906 records identified, 187 full texts retrieved, 170 assessed, 120 studies included. Underlying modality is text (biomedical papers, clinical notes, EHRs); benchmark datasets are tabulated.

## Method
Taxonomy and comparison of approaches: classical extractive methods (e.g. TextRank) through transformer models (BERT, T5, BART, GPT-4) and domain-specific models (BioBERT, PubMedBERT, SciBERT, Med-PaLM); training paradigms (pre-train then fine-tune, parameter-efficient fine-tuning such as LoRA/PEFT); domain adaptation strategies; evaluation metrics (ROUGE, BLEU, BERTScore and others) and their shortcomings.

## Results
Qualitative synthesis: LLMs have improved fluency, coherence and contextual relevance of biomedical summaries. Persistent problems are factual inconsistency/hallucination, insufficient domain adaptation, ambiguous abbreviations (e.g. "CRP" with multiple meanings), scarce annotated datasets, limited explainability, privacy and bias. ROUGE/BLEU do not capture clinical relevance or factual accuracy. PEFT methods such as LoRA are highlighted for low-resource settings. No new experimental numbers.

## Limitations
Review-only; PRISMA screening is susceptible to publication bias and English-language restriction; coverage ends in 2024; text-only focus (multimodal summarisation listed as future work).

## Transferable ideas for the FYP pipeline
- **Text/RAG:** build a glossary of TRUMPF/laser-cutting abbreviations and ambiguous terms (e.g. parameter codes, gas/nozzle acronyms) to disambiguate retrieval and generation - the paper's abbreviation problem maps directly to machine documentation.
- **LLM reasoning:** LoRA/PEFT on a small curated corpus (manuals, fault reports) is the recommended route for low-resource domain adaptation.
- **Evaluation:** do not rely on ROUGE/BLEU to score generated diagnoses or optimisation reports; use factual-consistency checks against source evidence, BERTScore as a secondary metric, and expert review (human-in-the-loop).
- **Fusion:** future-direction emphasis on integrating structured knowledge and multimodal inputs supports the FYP's combined table + image + document design.
