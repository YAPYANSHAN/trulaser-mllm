# AD-GPT: large language models in Alzheimer's disease

- **Citation (IEEE):** Z. Liu, L. Tang, Z. Sun, et al., "AD-GPT: large language models in Alzheimer's disease," *BMC Medical Informatics and Decision Making*, vol. 26, art. 286, 2026, doi: 10.1186/s12911-026-03579-x.
- **Domain:** Biomedical informatics / domain LLM with RAG and query routing
- **Relevance to FYP (1-5):** 4 - biomedical domain, but the architecture (task-partitioned databases, BERT query router, small fine-tuned Llama experts, router/context verifiers, citation-validity metrics) is a strong blueprint for an evidence-grounded, hallucination-controlled diagnostic assistant.

## Problem
General LLMs give inaccurate or superficial answers on Alzheimer's-disease genomics and literature, and hallucinate citations. Need reliable retrieval and synthesis across structured genomic databases and unstructured publications.

## Data & modalities
Structured: GTEx cis-eQTL and sQTL across 13 brain regions, NCBI genomic locations, OMIM gene functions. Unstructured: about 150,000 AD-related PubMed (MEDLINE) publications.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- RAG with task-specific database partitioning for three tasks: (1) genetic information retrieval, (2) association-study reasoning, (3) general AD knowledge synthesis.
- BERT-based query router (stacked routing) assigns queries to tasks; router verifier with automatic query refinement and context verifier check task assignment and evidence relevance.
- Task experts: Llama 3.2-3B (Task 1), Llama 3.1-8B (Tasks 2-3), fine-tuned and combined with task-specific retrieval.
- Evaluation metrics: accuracy, factual consistency, citation validity rate (citations verifiable in external bibliographic databases), instruction inconsistency/answer relevance.
- Baselines: ChatGPT series (incl. o1), Claude series, DeepSeek-8B, Gemini 1.5 Flash, Llama 2/3.1/3.2, Qwen2.5, Grok 3. Served via FastAPI in Docker.

## Results (key numbers and metrics)
- Correct routing rate rose to 96% with verifier and automatic query refinement.
- Task 1 accuracy 90.84% (base Llama 3.2-3B 32%) vs ChatGPT-o1 85.33%, Claude 3.5 Haiku 74.28%, Llama 3.1-70B 70.52%, Llama 2-70B 59.59%, Qwen2.5 17.14%.
- Tasks 2-3: significant improvements over base Llama 3.1-8B in evidence grounding, especially citation metrics; reduced hallucination.

## Limitations
Limited genomic scope; text and tabular only (multimodal data future work); clinical interpretability still to be improved; code release pending publication.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** partition the knowledge store by task: machine-database facts (Text2SQL), defect-image case library, and manuals/service documents; route each query with a lightweight classifier.
- **LLM reasoning:** use small fine-tuned experts (3B-8B) per task instead of one large model; add a verifier that checks that retrieved evidence actually supports the question before generation.
- **Evaluation:** adopt citation-validity rate (does each cited manual page/DB record exist and support the claim?), factual consistency and routing accuracy as metrics alongside diagnosis accuracy.
- **Deployment:** containerised FastAPI service for the pipeline.
