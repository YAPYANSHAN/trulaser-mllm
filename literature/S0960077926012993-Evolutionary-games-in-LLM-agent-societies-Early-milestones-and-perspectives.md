# Evolutionary games in LLM-agent societies: Early milestones and perspectives

- **Citation (IEEE):** K. Xie, Y. Liu, Z. Lan, et al., "Evolutionary games in LLM-agent societies: Early milestones and perspectives," *Chaos, Solitons and Fractals*, vol. 213, Art. no. 119158, 2026, doi: 10.1016/j.chaos.2026.119158.
- **Domain:** Evolutionary game theory / multi-agent LLM social simulation (review/perspective)
- **Relevance to FYP (1-5):** 1 - about cooperation dynamics among LLM agents; no industrial, multimodal or diagnostic content.

## Problem
Classical evolutionary game theory (EGT) relies on predefined strategy update rules. LLM agents instead choose actions from natural-language prompts describing rules, payoffs and history. The review asks what changes when LLM agents replace these rules, and whether cooperation still emerges.

## Data & modalities
None of its own ("No data was used"). It surveys prior simulation studies of LLM agents in social dilemmas (e.g., prisoner's dilemma, public goods games) with text prompts.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- A literature survey and perspective.
- Summarises how LLM agents operate in EGT: textual game descriptions and interaction history are put into the prompt, and the LLM outputs an action.
- Analyses why classic mechanisms (direct reciprocity, network reciprocity) do not automatically carry over.
- Categorises interventions into (i) EGT-side mechanisms (interaction structure, payoffs, update rules) and (ii) LLM-specific mechanisms (internal reasoning, anticipation of long-term consequences, framing).

## Results (key numbers and metrics)
Qualitative findings, with no new benchmark numbers:
- Replacing rules with LLM agents does not guarantee cooperation. Repeated play can produce retaliation instead of reciprocity, and static networks may not yield network reciprocity.
- Stronger reasoning can sharpen the incentive to free-ride.
- High average cooperation should not be read as sustained cooperation; it must also persist over time and recover after disturbances.

## Limitations
- Short perspective on an early-stage field.
- Evidence comes from heterogeneous small simulations.
- Open problems: formalising the evolution of language-based strategies, genuine long-term adaptation, and mixed human-AI populations.

## Transferable ideas for the FYP pipeline
- **LLM reasoning (multi-agent):** if the FYP uses several cooperating LLM agents (e.g., a vision agent, a machine-data agent and a documentation agent negotiating a diagnosis), do not assume they will cooperate or converge. Design explicit aggregation rules and incentives instead, such as a structured arbitration or voting step.
- **Evaluation:** judge agent behaviour on stability over time and recovery after perturbation (e.g., conflicting evidence), not just average agreement.
Otherwise there is little direct transfer.
