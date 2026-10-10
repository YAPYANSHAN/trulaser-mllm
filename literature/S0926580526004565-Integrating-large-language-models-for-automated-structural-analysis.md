# Integrating large language models for automated structural analysis

- **Citation (IEEE):** H. Liang, M. Talebi-Kalaleh, and Q. Mei, "Integrating large language models for automated structural analysis," *Automation in Construction*, vol. 192, Art. no. 107215, 2026, doi: 10.1016/j.autcon.2026.107215.
- **Domain:** Civil/structural engineering — LLM tool use (finite element analysis code generation)
- **Relevance to FYP (1-5):** 3 — an engineering LLM pipeline that grounds answers by calling deterministic engineering software; directly transferable as the "LLM + calculation tool" pattern, though no fault diagnosis or images.

## Problem
FEM-based structural analysis needs substantial manual effort and specialist knowledge. No systematic framework uses LLMs to go automatically from a descriptive text problem to verified structural analysis outputs.

## Data & modalities
Text in, code and numerical/graphical outputs out. New small benchmark SAWP-20: 20 structural-analysis word problems (static 2-D frames, varying stories/bays, asymmetric layouts) with ground-truth solutions, descriptions and reference code.

## Method
- Three-stage code-generation pipeline: parameter extraction → finite element model construction (OpenSeesPy) → visualization (OpsVis); staging mitigates long-context failures and eases fault isolation.
- Domain-specific prompt design: embedded commonsense and spatial-reasoning instructions (node numbering, supports, load assignment).
- In-context learning with a single reference example (ICL template).
- Generated Python is executed; an answer is correct if it runs and its numerical outputs closely match ground truth. Each experiment repeated three times.
- LLMs compared: GPT-5.4, GPT-4o, GPT-4, Gemini 1.5 Pro, Llama-3.3.

## Results
- Accuracy on test examples: GPT-5.4 100%, GPT-4o 100%, GPT-4 85%, Gemini 1.5 Pro 80%, Llama-3.3 30%.
- Domain-specific instructions improved performance by 30% on asymmetric configurations.
- Generalizes from one reference example to more stories/bays and asymmetry.
- Without the ICL template, GPT-4o produced generic or incorrect answers (shown as failure cases).

## Limitations
Small, manually curated benchmark (20 problems), static 2-D frames only; few runs due to API cost; proof-of-concept, not engineering-ready; error types: missing nodes/elements and mis-assigned loads or supports because the LLM cannot "see" its generated model; trained only on correct patterns.

## Transferable ideas for the FYP pipeline
- **LLM reasoning / tools:** let the LLM call deterministic tools (SQL queries over the TruLaser machine database, Python calculations of cutting speed/energy per length, OpenCV measurements) rather than computing numbers itself; staged pipeline (extract parameters → query/compute → interpret).
- **Prompting:** a single well-crafted in-context example of a full diagnosis (evidence → reasoning → recommendation) plus domain rules in the system prompt can greatly improve reliability.
- **Evaluation:** small curated benchmark of fault cases with ground truth; correctness = executable + numeric match; run each case multiple times to measure stability; compare proprietary vs open models.
- **Multimodal validation:** authors propose feeding rendered outputs back to a multimodal LLM to self-check — analogous to re-checking a recommended parameter set against images of the resulting cut.
