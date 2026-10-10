# EBRB–LLM Hybrid Architectures for Trustworthy Agentic AI: Vision, Opportunities, and Challenges

- **Citation (IEEE):** J. Liu, C. Nugent, D. Yu, et al., "EBRB–LLM Hybrid Architectures for Trustworthy Agentic AI: Vision, Opportunities, and Challenges," *Int. J. Comput. Intell. Syst.*, vol. 19, art. 332, 2026, doi: 10.1007/s44196-026-01529-z.
- **Domain:** Trustworthy AI / neuro-symbolic agentic LLM architectures (position paper; scenarios include industrial safety)
- **Relevance to FYP (1-5):** 4 — no experiments, but it gives a concrete architectural pattern for evidence-based, uncertainty-aware LLM diagnosis with rule-grounded explanations and deferral, directly useful for the FYP's "reasoning" stage. Belief rule bases have a history in fault diagnosis.

## Problem
LLM agents lack calibrated uncertainty, hallucinate, and give rationales that may not be faithful ("explainability theater"). This conflicts with the EU AI Act, NIST AI RMF and WHO requirements for high-risk settings, including industrial operations.

## Data & modalities
None (position paper). The conceptual inputs are multimodal: clinical notes, financial reports, system logs and sensor summaries, which the LLM converts to structured attributes.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
A three-layer EBRB–LLM "guardrail":
1. **Perception & orchestration (LLM):** ingests multimodal inputs, extracts structured attributes (with schema validation), and proposes candidate actions in a ReAct style.
2. **Belief rule reasoning (Extended Belief Rule Base):** computes similarity-based rule activation and Evidential Reasoning (ER) aggregation. This yields belief degrees over hypotheses (e.g., incident or fault types), an explicit ignorance mass βΘ, and rule activation traces. Domain and safety rules are encoded here.
3. **Safety, deferral & explanation:** approve only if max belief ≥ τc and ignorance ≤ τu. Otherwise request more evidence or escalate to a human. The LLM writes explanations constrained to the EBRB trace.

Reflection is triggered by high ignorance or conflict among rules, not heuristically. The paper compares EBRB with KGs, RAG and other neuro-symbolic methods on belief fusion, ignorance, traceability, thresholds and suitability as a governor. Scenarios: acute-care triage, finance, cybersecurity and industrial safety (LLM synthesises logs and sensor streams; EBRB blocks unsafe or premature actions).

## Results (key numbers and metrics)
No empirical results. The contributions are conceptual: the architecture, a mapping to TAI dimensions, domain scenarios and a research agenda.

## Limitations
Not validated empirically. Open challenges include scalable rule induction, co-adaptation between the LLM and EBRB, propagating LLM extraction errors into ignorance mass, and how to evaluate governed hybrid agents. Building rule bases requires domain knowledge.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** use the MLLM for perception (read images, tables, manuals → structured attributes such as defect type, gas pressure deviation or nozzle condition). Pass these to a transparent rule/belief layer encoding TRUMPF troubleshooting rules (e.g., "dross + low pressure → gas supply"). This produces fault hypotheses with belief and ignorance scores.
- **Evidence-based explanations:** constrain the LLM's final explanation to the activated rules and retrieved evidence, so the diagnosis is traceable to the manual or table rows.
- **Safety/deployment:** add confidence and ignorance thresholds that trigger "need more evidence" (e.g., request a closer image or a sensor log) or escalation to the operator instead of a forced answer.
- **Data ingestion:** validate LLM-extracted attributes against a schema before reasoning.
- **Evaluation:** measure deferral rate vs. accuracy and the faithfulness of explanations to traces.
