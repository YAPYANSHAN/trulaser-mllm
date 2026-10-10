# Large language model-augmented offline reinforcement learning framework for sepsis management in critical care

- **Citation (IEEE):** Y. Lim, B. Jeon, S.-A. Park, et al., "Large language model-augmented offline reinforcement learning framework for sepsis management in critical care," *npj Digital Medicine*, vol. 9, art. 457, 2026, doi: 10.1038/s41746-026-02611-8.
- **Domain:** Medical decision support - multimodal (structured time-series + clinical text) offline reinforcement learning
- **Relevance to FYP (1-5):** 3 - clinical domain, but the fusion of structured time-series with LLM-summarised free text via gated/cross-modal attention, and using offline RL for action (parameter) recommendation, maps onto combining machine tables with operator notes for process optimisation.

## Problem
Sepsis RL policies have relied on structured vitals/labs, which are noisy, missing and irregular, and ignore contextual information in clinical notes; notes are irregular in timing and density, making multimodal RL difficult.

## Data & modalities
Structured ICU time-series (vital signs, labs, treatments: fluids and vasopressors) + unstructured clinical notes (physician, nursing, radiology reports, discharge summaries). Datasets: MIMIC-III, MIMIC-IV (public) and a tertiary ICU dataset from SNUH; cross-dataset validation.

## Method
MORE-CLEAR: an LLM produces structured summaries of clinical notes to reduce irregularity; text encoded with BERT, ClinicalBERT or Llama 3.1-8B; structured state encoded separately; gated fusion and cross-modal attention dynamically weight modalities. The fused state feeds offline RL (Conservative Q-Learning, CQL; BCQ also compared). Text strategies compared: initial note as static context vector (best) vs stacking recent notes. The LLM is restricted to summarisation/representation, not acting as the policy. Evaluation via off-policy evaluation (doubly robust, fitted Q-evaluation, weighted importance sampling, OPERA) and BDESR-stratified estimated survival rate.

## Results
Multimodal policies consistently outperformed structured-only and text-only policies on OPE metrics and estimated survival; ClinicalBERT + CQL was the most robust combination, BERT + CQL also strong. Structured-only still beat text-only. LLM-summarised notes gave better and more stable value estimates and reduced overestimation vs raw notes. Patients whose care aligned with the learned policy (low BDESR) had higher survival. RL beat supervised baselines. SNUH performance held with 60% of data.

## Limitations
Off-policy evaluation only (no prospective trial); gains bounded by documentation quality and cross-site shift; policy reflects local practice patterns; binary terminal reward; offline RL sensitive to distribution shift and low-coverage state-action regions.

## Transferable ideas for the FYP pipeline
- **Data ingestion:** use an LLM to convert free-text operator/maintenance notes into structured summaries before fusing with machine tables - reduces noise and missingness.
- **Fusion:** gated fusion + cross-modal attention between tabular process data and text embeddings; keep a static "job context" vector (material, thickness, nozzle, job notes) as in the initial-note strategy.
- **Process optimisation:** offline RL (e.g., CQL) over historical cut logs could suggest parameter adjustments, with the LLM limited to explanation, not control.
- **Evaluation:** off-policy evaluation and "alignment-with-recommendation vs outcome" stratification as a proxy when live trials on the TruLaser are impossible.
