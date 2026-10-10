# Large language models in implant dentistry: a scoping review of applications, performance, and limitations

- **Citation (IEEE):** H.-J. Kong and Y.-L. Kim, "Large language models in implant dentistry: a scoping review of applications, performance, and limitations," *BMC Oral Health*, vol. 26, art. 1492, 2026, doi: 10.1186/s12903-026-08747-z.
- **Domain:** Medical/dental AI - scoping review of LLMs
- **Relevance to FYP (1-5):** 1 - dental domain review; only general lessons (hallucination persists despite RAG, text-only models cannot read images, human oversight needed) carry over.

## Problem
What is the current performance, range of applications and limitations of LLMs in implant dentistry, in clinical and educational settings, and how do they compare with human experts?

## Data & modalities
Scoping review (PRISMA-ScR) of PubMed, Web of Science, Scopus and Embase through December 2025; 18 eligible studies, all from 2024-2025. Mostly text-based evaluations (exam questions, patient questions, vignettes); two diagnostic-assessment studies.

## Method
Studies classified into patient interaction (n = 9), medical knowledge (n = 7) and diagnostic assessment (n = 2); analysis of model architectures (e.g., ChatGPT versions incl. o1, DeepSeek-R1, Gemini, medical-specific models), task performance and comparisons with dentists; discussion of RAG-augmented systems.

## Results
Advanced reasoning models (e.g., ChatGPT-o1, DeepSeek-R1) occasionally surpassed licensed dentists on certification-style exams. Medical-specific models did not consistently beat state-of-the-art generalist LLMs. Hallucinations persisted even with RAG, especially in systematic literature-search tasks. Text-only models cannot interpret diagnostic imaging (CBCT, radiographs), limiting clinical autonomy. Conclusion: LLMs are adjunctive support, not replacement for clinical judgement.

## Limitations
Small evidence base (18 studies); geographic concentration (six studies from Türkiye) and English-centric evaluation; heterogeneous designs/metrics; cross-sectional, in-silico benchmarks with fictional vignettes; no randomised controlled trials; no formal risk-of-bias assessment.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** do not assume a domain-specialised model beats a strong general model; benchmark both for laser-cutting Q&A.
- **Text/RAG:** RAG reduces but does not eliminate hallucination - add citation checking (answer must quote retrieved manual text).
- **Vision/fusion:** the review's "sensory blindness" critique supports the FYP's choice of a multimodal pipeline that actually inspects cut-part images rather than relying on text descriptions.
- **Evaluation:** avoid relying only on exam-style or vignette questions; include realistic, noisy shop-floor cases and expert comparison; keep a human-in-the-loop for safety-relevant recommendations.
