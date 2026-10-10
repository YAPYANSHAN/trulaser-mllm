# Knowledge extraction and retrieval-augmented generation for intelligent maintenance of wind power equipment based on graph attention networks

- **Citation (IEEE):** X. Li, G. Li, T. Wang, et al., "Knowledge extraction and retrieval-augmented generation for intelligent maintenance of wind power equipment based on graph attention networks," *Chinese Journal of Mechanical Engineering*, vol. 39, Art. no. 100141, 2026, doi: 10.1016/j.cjme.2025.100141.
- **Domain:** Industrial fault diagnosis and maintenance (wind-turbine bearings) / KG-enhanced RAG
- **Relevance to FYP (1-5):** 5 - a direct template for a diagnosis → retrieval → recommendation pipeline. It combines signal-based fault classification with an LLM-built knowledge graph fused from text, visual and structured data, plus GPT-4o generation of maintenance advice.

## Problem
Most wind-turbine diagnosis studies stop at fault classification and do not produce actionable, personalised maintenance recommendations. Plain vector RAG models context poorly and loses multi-hop relations between fault, condition, signal and maintenance.

## Data & modalities
- An industrial bearing vibration dataset from a wind-power company, sampled at 12 kHz. It has nine fault classes (inner race, outer race, combined, cage, rolling element, etc.) across speeds and loads, with 1000 samples of 1024 points per class.
- A domain knowledge graph of about 1200 RDF triples, built from laboratory expertise and public O&M documentation. It fuses textual, visual and structured data.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
1. **Diagnosis:** a 1D-CNN with wavelet transform extracts multi-scale time-frequency features to identify the fault type.
2. **KG construction:** a multi-layer ontology (fault → maintenance → operating condition → signal). LLM plus a rule-based engine perform NER, relation extraction, event extraction and entity standardisation, producing RDF triples stored in Neo4j.
3. **Graph embedding:** a GAT embeds entities and relations, with attention over heterogeneous edges and k-hop aggregation. Each semantic path is indexed as a graph embedding plus its subgraph and triples.
4. **Retrieval:** cosine-similarity retrieval of semantic paths.
5. **Generation:** GPT-4o produces natural-language maintenance recommendations from the retrieved subgraphs and historical cases. An example output cites a 49.3 Hz energy surge, kurtosis and skewness, then gives replacement and alignment-check advice.

## Results (key numbers and metrics)
Generated recommendations were compared across three settings:

| Setting | BLEU | ROUGE-L | Human score (1-5) |
|---|---|---|---|
| No RAG | 19.4 | 28.5 | 2.8 |
| Traditional RAG | 24.7 | 35.2 | 3.7 |
| GAT-RAG | 31.6 | 44.1 | 4.6 |

GAT-RAG's gains over traditional RAG are relative improvements of 27.9% in BLEU and 25.3% in ROUGE-L. A human panel of 5 researchers, 3 senior experts and 10 frontline workers also rated the outputs.

## Limitations
- The KG is small (about 1200 triples) with limited coverage.
- Cross-domain applicability has not been verified.
- BLEU and ROUGE-L measure text overlap, not diagnostic correctness.
- Generation relies on the closed GPT-4o model.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** build a TruLaser ontology (defect → cause → process parameter → machine signal/alarm → corrective action). Use an LLM plus rules to extract triples from TRUMPF manuals and service logs into Neo4j, and retrieve whole semantic paths rather than isolated chunks.
- **Fusion:** feed the output of the vision/tabular classifier (e.g., "dross on bevel edge") as the query entity into the KG for structure-aware retrieval.
- **LLM reasoning:** generate recommendations that cite the measured evidence (feature values), as in the GPT-4o example.
- **Evaluation:** run an ablation of no-RAG vs. RAG vs. graph-RAG, and pair BLEU/ROUGE-L with expert and operator ratings.
