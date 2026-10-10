# Implementing generative artificial intelligence in precision oncology: safety, governance, and significance

- **Citation (IEEE):** R. Hamamoto, T. Koyama, S. Takahashi, et al., "Implementing generative artificial intelligence in precision oncology: safety, governance, and significance," *Journal of Hematology & Oncology*, vol. 19, art. 14, 2026, doi: 10.1186/s13045-026-01781-y.
- **Domain:** Medical AI (precision oncology) - narrative review of generative AI, LLMs/VLMs, RAG and governance
- **Relevance to FYP (1-5):** 2 - clinical domain and no experiments, but its RAG + human-in-the-loop (HITL) governance recipe (audit logs, uncertainty, escalation, data standards) transfers to a safety-relevant industrial diagnosis assistant.

## Problem
How generative AI can be safely implemented in precision oncology to link literature, guidelines, trial protocols and patient data, while handling hallucination, knowledge freshness, bias, privacy and regulatory accountability.

## Data & modalities
Review - no new dataset. Covers EHR free text, genomic variant data, clinical-trial protocols, radiology and pathology images, and synthetic EHR data. Discusses data standards OMOP, mCODE and FHIR.

## Method
Narrative review organised as: history of generative models (RBM/DBN, VAE, GAN, diffusion, Transformer/MoE); medical LLM applications (medical QA and decision support - e.g., Med-PaLM lineage, EHR note drafting/structuring, imaging report generation incl. RadAlign, synthetic EHRs e.g. HiSGT/SynEHRgy, triage chatbots); and three precision-oncology axes: (1) LLM-based mutation interpretation, (2) clinical-trial eligibility verification, (3) multimodal foundation models computing "tumor phenotypes" from imaging/pathology for report drafting and molecular-surrogate estimation. Proposes a strategy centred on RAG and HITL workflows, standardised data preparation, multicenter prospective evaluation, auditable logs, governance aligned with GMP and the EU AI Act, and synthetic data with differential privacy.

## Results
No original experiments; summarises published results (tables of models such as Claude Sonnet, Mistral Medium, Med-PaLM, etc.). Key conclusions: grounding via RAG and HITL review is necessary; clinically significant errors still persist in generated imaging reports; evaluation should use outcome-based, prospective studies and reporting standards (TRIPOD, CONSORT).

## Limitations
Narrative (not systematic) review; oncology-specific; rapidly evolving model landscape means specific comparisons date quickly; no quantitative synthesis.

## Transferable ideas for the FYP pipeline
- **Text/RAG:** ground every diagnosis in retrieved TRUMPF manual / maintenance-procedure passages and keep the corpus versioned ("knowledge freshness").
- **LLM reasoning:** output explicit, calibrated uncertainty and escalation rules (e.g., "safety-related fault - refer to service technician") rather than single confident answers.
- **Data ingestion:** use a common data model for machine-database tables (consistent schema, units, timestamps), analogous to OMOP/FHIR, before LLM access.
- **Deployment/governance:** auditable logs of prompts, retrieved evidence and outputs; HITL approval before parameter changes are applied to the machine; consider EU AI Act / machinery-safety framing in the FYP report.
- **Evaluation:** move beyond text metrics toward prospective, outcome-based tests (e.g., did the recommended fix resolve the defect?).
