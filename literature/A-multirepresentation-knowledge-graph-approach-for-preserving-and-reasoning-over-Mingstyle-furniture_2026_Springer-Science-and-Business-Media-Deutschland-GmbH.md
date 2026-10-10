# A multi-representation knowledge graph approach for preserving and reasoning over Ming-style furniture

- **Citation (IEEE):** X. Ru, H. Wan, M. Wang, et al., "A multi-representation knowledge graph approach for preserving and reasoning over Ming-style furniture," *npj Heritage Science*, vol. 14, art. 499, 2026, doi: 10.1038/s40494-026-02779-y.
- **Domain:** Cultural heritage / knowledge graphs + LLM question answering (neuro-symbolic)
- **Relevance to FYP (1-5):** 4 - domain differs, but the hybrid KG-RAG with an LLM planner plus graph and rule (SHACL) executors handling engineering constraints (dimensions, standards, compatibility) is directly applicable to evidence-grounded laser-cutting diagnosis.

## Problem
Ming-furniture knowledge (structure, joinery, materials, ergonomics) is fragmented across catalogues, standards, e-commerce records and user feedback. Questions often require validity checking against structural and standards constraints, which standard RAG and GraphRAG handle poorly.

## Data & modalities
Text from museum archives, monographs/catalogues, national standards, e-commerce records and user reviews; an expert terminology ontology. A QA benchmark with question types C1-C4 (direct, multi-hop, constraint-based, and a further category).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Ontology-constrained extraction: Qwen2.5 performs end-to-end JSON triple extraction (subject, relation, object, evidence pointer), plus a recall-enhancement module.
- Entity normalisation by fuzzy clustering with LLM arbitration.
- Dual representation sharing global IDs: Neo4j property graph (multi-hop path retrieval) and RDF/OWL/SHACL semantic graph (logical/rule validation), with named graphs and evidence nodes for provenance.
- HybridRAG QA: LLM planner decomposes questions and plans queries; executors run graph traversal (Cypher) and SPARQL/SHACL constraint checks; answers carry sentence-level evidence tags (e.g., [MUSEUM::], [STD::]).
- Baselines: LLM-only, Standard-RAG (Chroma + Qwen embeddings, top-K), Graph-RAG (PG only), Onto-RAG (OWL only), Microsoft GraphRAG.

## Results (key numbers and metrics)
- Refined information extraction: average F1 0.87.
- QA expert score 4.87/5.0 for HybridRAG, outperforming standard RAG and general graph baselines; Graph-RAG (PG only) about 4.5 on multi-hop questions.
- Microsoft GraphRAG strong on narrative multi-hop questions but drops on constraint-satisfaction (C3) tasks; metrics include path ratio and Constraint Satisfaction Rate.

## Limitations
Single domain, Chinese-language sources; relies on expert-built ontology; evaluation partly by expert scoring; engineering complexity of maintaining two graph representations.

## Transferable ideas for the FYP pipeline
- **Text/RAG (KG):** build a laser-cutting KG from TRUMPF manuals, parameter tables and maintenance logs via ontology-constrained LLM triple extraction with evidence pointers back to the source page.
- **LLM reasoning:** use an LLM planner + deterministic executors: graph queries for cause chains (defect -> parameter -> component) and SHACL/rule checks for hard constraints (e.g., gas pressure range for given thickness, focus position limits) so recommendations never violate machine specs.
- **Evaluation:** stratify questions into direct, multi-hop and constraint-check types; report a constraint-satisfaction rate; compare against plain vector RAG and GraphRAG baselines.
- **Deployment:** sentence-level evidence tags ([MANUAL::p.x], [DB::job_id]) for auditable reports.
