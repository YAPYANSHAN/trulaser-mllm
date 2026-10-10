# Tuning and clinical application of large language models in Traditional Chinese Medicine: scoping review

- **Citation (IEEE):** C. Han, G. Yang, H. Li, et al., "Tuning and clinical application of large language models in Traditional Chinese Medicine: scoping review," *Chinese Medicine*, vol. 21, Art. no. 71, 2026, doi: 10.1186/s13020-026-01346-8.
- **Domain:** Medical NLP / domain-adaptation of LLMs (scoping review)
- **Relevance to FYP (1-5):** 2 - unrelated domain, but it is a useful survey of how practitioners adapt LLMs to a niche knowledge domain (LoRA, continued pre-training, RAG, prompting) and of the evaluation patterns used. Good for justifying technique choices in the literature review.

## Problem
LLMs are increasingly applied to Traditional Chinese Medicine (TCM), but there is no systematic picture of tuning techniques, data construction, evaluation methods and applications, or of where they fall short.

## Data & modalities
Scoping review (PRISMA-ScR) of seven databases (including PubMed, Web of Science, IEEE Xplore, ACM DL, arXiv) up to May 2025. 27 studies were included (21 English, 6 Chinese). Training data in the reviewed studies is mostly text: clinical case records (73.9%) and TCM classics (65.2%). Multimodal data (tongue images, pulse, facial features) is severely lacking.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
Review method: systematic search, screening and charting of base model and parameters, tuning techniques, data characteristics, evaluation methods and metrics, comparison models, applications and limitations. Techniques found in the reviewed studies:
- LoRA fine-tuning: 65.2%
- Prompt engineering: 47.8%
- Continued pre-training: 43.5%
- RAG: 39.1%
- Knowledge graphs: about 21%
- Multiple techniques combined: 87.0%

Base models were mostly Chinese open LLMs (ChatGLM, Qwen, Baichuan, LLaMA families).

## Results (key numbers and metrics)
- Applications: knowledge consultation (10 studies), diagnostic assistance (13), evaluation benchmarks (4).
- Evaluation: human assessment (77.8%) and accuracy (63.0%) were most common. Specialised TCM benchmarks are emerging.
- Strengths: integrating heterogeneous knowledge, basic syndrome-differentiation reasoning, cross-language knowledge conversion.
- Weaknesses: complex holistic reasoning, individualised diagnosis, and hallucination as a systematic barrier.

## Limitations
- About 37% of the included studies are preprints.
- High heterogeneity prevents meta-analysis.
- Only English and Chinese literature.
- Focus on application rather than technical depth.

## Transferable ideas for the FYP pipeline
- **LLM fine-tuning / RAG design:** the field's default stack is a combination: LoRA on an open base model + prompt engineering + RAG, optionally with a knowledge graph. This supports a hybrid design for the TRUMPF assistant (LoRA on fault Q&A + RAG over manuals) rather than a single technique.
- **Data:** a domain corpus should combine "theory" (manuals, laser-cutting process knowledge, the equivalent of classics) with "case records" (historic fault tickets, operator logs). Note the warning that text-only data limits diagnosis when the real task is multimodal. That is an argument for adding images and tables in the FYP.
- **Evaluation:** use both automatic accuracy and structured human expert assessment. Consider a small domain benchmark.
- **LLM reasoning:** treat hallucination as systematic. Ground outputs in retrieved evidence and cite sources.
