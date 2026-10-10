# A model-driven knowledge graph treatment for process-centric cyber threat mitigation

- **Citation (IEEE):** A. Chis, A.-M. Ghiran, and R. A. Buchmann, "A model-driven knowledge graph treatment for process-centric cyber threat mitigation," *Knowledge and Information Systems*, vol. 68, art. 210, 2026, doi: 10.1007/s10115-026-02819-w.
- **Domain:** Cybersecurity / conceptual modelling, knowledge graphs, GraphRAG
- **Relevance to FYP (1-5):** 2 - cybersecurity domain; transferable only as a pattern for turning structured diagrams/process models into RDF knowledge graphs queried via SPARQL and LLM GraphRAG.

## Problem
Cyber-threat analysis must involve business and technical stakeholders, follow "secure by design" principles and keep design decisions semantically traceable for AI analysis; existing threat-modelling tools only offer visual inspection.

## Data & modalities
Diagrammatic models (BPMN business processes linked to data-flow diagrams and threat models with trust zones, threats and mitigations) serialised into RDF graphs; natural-language questions. Demonstrated on illustrative cases rather than a quantitative dataset.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Domain-specific modelling language (DSML) hybridising BPMN, DFD and threat modelling (STRIDE-type categories), developed with Design Science Research and Agile Modeling Method Engineering (AMME) on the ADOxx metamodelling platform.
- Model-to-RDF transformation (Turtle/TriG serialisation) into Graphwise GraphDB triplestore; SPARQL competency queries.
- GraphRAG: relevant RDF subgraphs extracted and injected as context into a system prompt for OpenAI GPT-4.1 (Azure) to answer natural-language questions; model-driven aggregation reports of missing mitigations.
- No fine-tuning.

## Results (key numbers and metrics)
Qualitative/design evaluation: requirements satisfied, competency-question evaluation via SPARQL categories, example GraphRAG answers (e.g., identifying that none of 3 possible mitigations for repudiation is in place for an entity). No headline quantitative accuracy metrics reported in the sections read.

## Limitations
Tied to OpenAI, RDF and ADOxx; LLM is read-only (cannot modify graphs/models); no enterprise-scale scalability tests; triplestore + LLM costs for SMEs; users tend to fall back to free natural-language interaction.

## Transferable ideas for the FYP pipeline
- **Text/RAG (KG):** model the TruLaser process (job -> sheet -> part -> cut contour -> parameter set -> defect -> cause -> corrective action) as an explicit schema and serialise it to RDF/graph; answer questions with SPARQL for exact facts and LLM GraphRAG for explanation.
- **LLM reasoning:** inject only the extracted subgraph relevant to the current fault as context, reducing hallucination and providing traceable evidence.
- **Evaluation:** define competency questions up front (e.g., "which defects in job X lack a documented corrective action?") and verify the KG/LLM can answer them.
- **Deployment:** keep the LLM provider swappable behind a prompt/adapter layer, as done here.
