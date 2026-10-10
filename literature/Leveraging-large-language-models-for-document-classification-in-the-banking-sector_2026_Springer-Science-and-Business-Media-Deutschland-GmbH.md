# Leveraging large language models for document classification in the banking sector

- **Citation (IEEE):** R. Nogueira, H. Mentzingen, and N. Garcia, "Leveraging large language models for document classification in the banking sector," *International Journal of Data Science and Analytics*, vol. 22, art. 126, 2026, doi: 10.1007/s41060-026-01077-x.
- **Domain:** NLP / document AI (banking)
- **Relevance to FYP (1-5):** 2 - banking documents, but the zero-shot, label-description-driven classification of long PDFs with retrieval-based context selection is a useful pattern for routing technical documents and maintenance records in the FYP's documentation pipeline.

## Problem
Real-world document classification must cope with variable, long, sometimes scanned/handwritten documents and semantically overlapping classes, while traditional models need labelled data and technical expertise and give little explanation.

## Data & modalities
Text extracted from PDFs (incl. OCR via Tesseract for digitised/handwritten files). Dataset: 270 public Portuguese PDF files, equally distributed over nine banking classes (e.g., annual reports, trial balances, land registry certificates, property/urban registry, energy certificates, "Other"); released publicly.

## Method
Zero-shot LLM framework configurable by non-technical users who supply label names and descriptions; the LLM returns a class plus explanation. Context-selection strategies compared: RAG (semantic retrieval of relevant chunks), first N pages, first + last pages, and TF-IDF selection, with N between 5 and 10 pages (at most half the document). Models: GPT-4o, GPT-4o-mini, GPT-3.5-turbo (OpenAI API). Benchmarks: NLI zero-shot (bart-large-mnli), embedding similarity (all-MiniLM-L6-v2), and a simple whole-document LLM call. Metrics: macro accuracy, precision, recall, F1 and token usage.

## Results
GPT-4o achieved the best results across strategies, with RAG best (accuracy 99.3% vs 98.9% with TF-IDF in Table 1). RAG, first-pages and first+last-pages consistently beat TF-IDF, with the largest gap for GPT-3.5-turbo. GPT-4o-mini and GPT-3.5-turbo were competitive when given good context. GPT-4o best separated near-identical classes (land registry vs property registry); GPT-3.5-turbo made ten more errors there. Selective retrieval cut token cost relative to sending whole documents without losing accuracy; the NLI baseline lagged substantially.

## Limitations
Reliance on an external LLM provider (privacy in regulated settings); performance depends on the quality of user-written label descriptions; no numerical confidence score (hinders HITL); small dataset and label set - scalability untested; only OpenAI models evaluated.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** zero-shot classify incoming TRUMPF documents, service reports and operator notes (e.g., "alarm log", "maintenance report", "parameter sheet") using label descriptions, with OCR for scanned pages.
- **Text/RAG:** retrieve only relevant chunks instead of whole manuals to cut tokens; compare retrieval strategies explicitly.
- **LLM reasoning:** require a class plus rationale and add an explicit confidence score (the authors' identified gap) to enable HITL review.
- **Evaluation/deployment:** report token cost alongside accuracy; test smaller models with good retrieval as cheaper alternatives.
