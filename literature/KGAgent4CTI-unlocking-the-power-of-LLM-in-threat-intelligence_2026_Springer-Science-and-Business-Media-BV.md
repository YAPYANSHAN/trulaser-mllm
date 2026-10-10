# KGAgent4CTI: unlocking the power of LLM in threat intelligence

- **Citation (IEEE):** L. Yang, H. Zhu, J. Mu, et al., "KGAgent4CTI: unlocking the power of LLM in threat intelligence," *Cybersecurity*, vol. 9, art. 76, 2026, doi: 10.1186/s42400-025-00458-2.
- **Domain:** Cybersecurity - LLM multi-agent knowledge-graph construction with hybrid RAG
- **Relevance to FYP (1-5):** 3 - different domain, but the multi-agent document-to-KG pipeline, hybrid (vector + BM25) retrieval with re-ranking, and version-aware indexing are directly reusable for ingesting TRUMPF manuals and mapping symptoms to a fault taxonomy.

## Problem
Building attack knowledge graphs from unstructured cyber-threat-intelligence (CTI) reports suffers from NER boundary drift, long-tail omissions, multi-hop dependencies, and version drift of the MITRE ATT&CK framework that parametric models cannot track.

## Data & modalities
Text (CTI reports in multiple formats incl. PDF/HTML) and the MITRE ATT&CK knowledge base. Benchmark corpus incl. 11 sub-techniques introduced after ATT&CK v11 (zero-shot set); case study on over 500 real CTI reports.

## Method
Multi-agent pipeline with five specialised agents: A_preprocess (format conversion, cleaning, semantic segmentation of documents), A_entity (template-guided entity extraction to JSON), A_relation (CoT-prompted relation extraction to subject-predicate-object triples), A_technique (enhanced RAG: query rewriting that abstracts IPs/hashes/URLs to entity types, hybrid retrieval combining HNSW vector top-5 and BM25 top-5 over ATT&CK technique blocks, re-ranking to counter lost-in-the-middle, iterative re-retrieval if evidence insufficient), and A_merge (triple consolidation into the KG). Version-aware indexing lets the knowledge base update with ATT&CK releases without retraining. LLM: GPT-4 via API (low temperature); no fine-tuning.

## Results
Zero-shot technique identification: precision 92.3%, recall 81.2%, F1 86.4%; recognised 9 of 11 unseen techniques, while recall of baselines TRAM, TTPDrill and AttacKG fell to 0.15, 0.31 and 0.25. On 500+ real reports: 18,069 entity, 9,023 relation and 4,095 technique instances extracted. Iterative targeted retrieval balanced precision and token cost better than providing all technique descriptions or single-shot retrieval. KG supports attack-scenario reconstruction and attribution.

## Limitations
Relies on a cloud GPT-4 API (cost, privacy); text-only (multimodal fusion of images left to future work); no live web search; evaluation partly qualitative for the real-report case study.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** an agent that converts and semantically chunks TRUMPF manuals, alarm-code lists and service bulletins; another that extracts (component, symptom, cause, remedy) triples into a laser-cutting fault KG.
- **Text/RAG:** hybrid dense + BM25 retrieval is valuable because alarm codes and part numbers are exact-match tokens; add re-ranking and an "evidence sufficient?" loop.
- **Query rewriting:** normalise raw machine values (error codes, IDs) to semantic types before retrieval.
- **Versioning:** version-aware index for firmware/manual revisions so diagnoses cite the correct document version.
- **Evaluation:** include a zero-shot set of fault types unseen in examples to test generalisation.
