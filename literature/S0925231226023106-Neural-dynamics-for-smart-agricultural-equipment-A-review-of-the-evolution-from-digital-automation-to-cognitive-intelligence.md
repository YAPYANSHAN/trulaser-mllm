# Neural dynamics for smart agricultural equipment: A review of the evolution from digital automation to cognitive intelligence

- **Citation (IEEE):** T. Zhang, C. L. P. Chen, X. Luo, et al., "Neural dynamics for smart agricultural equipment: A review of the evolution from digital automation to cognitive intelligence," *Neurocomputing*, vol. 705, Art. no. 134912, 2026, doi: 10.1016/j.neucom.2026.134912.
- **Domain:** Review — agricultural machinery, embodied AI, foundation models (VLMs, LLM agents)
- **Relevance to FYP (1-5):** 2 — a machinery-focused review with useful framing of the shift from rule-based automation to VLM/LLM "cognitive" systems and their risks, but no concrete diagnostic method.

## Problem
Digital automation (deterministic control, HD mapping) works in structured farmland but fails in fragmented, unstructured hilly regions; engineering-centric interfaces impose high cognitive load on non-expert farmers. The review examines how neural dynamics plus VLMs, LLM agents and embodied AI can move machinery from automation to "cognitive intelligence".

## Data & modalities
Review; no new dataset. Covers multimodal perception (cameras, LiDAR, GNSS/BeiDou, IoT sensors), language instructions and operation histories.

## Method
Structured literature review in three transitions:
- **Perception:** geometric reconstruction → open-vocabulary semantic perception with VLMs.
- **Decision:** programmatic parameter definition → intent-driven interaction via LLM agents with chain-of-thought planning; multi-agent LLM fleet scheduling. Table 3 lists examples (e.g., VLM+LLM crop disease diagnosis framework; GPT-aided YOLO image diagnosis reporting 90% accuracy for text-assisted diagnostic reports; YOLOWorld+LLM pest management with 68.7% F1 knowledge extraction; Farm-LightSeek LLM for IoT data analytics).
- **Control:** offline model calibration → learning-based neuro-dynamic control.
Roadmap: continual learning, swarm neuro-dynamics, neuromorphic edge computing, dynamic intent inference for human-agent symbiosis.

## Results
No experiments; results are those quoted from surveyed works (see Table 3 examples above). Mechanization statistics for China given as context (e.g., 75.64% comprehensive crop mechanization by end-2024).

## Limitations
Identified by the authors: scarcity of domain multimodal data; hallucination with no mechanism to bound outputs by hard safety rules; edge-vs-cloud compute dilemma (latency, power, privacy); sim-to-real gap and physical safety. As a review, it is broad and largely conceptual, focused on agriculture.

## Transferable ideas for the FYP pipeline
- **LLM reasoning / safety:** add a hard rule layer that bounds LLM process-optimisation recommendations to TRUMPF-allowed parameter ranges, since hallucinated parameters could damage parts or the machine.
- **Vision:** "detector + LLM report" pattern (GPT-aided YOLO) is a validated template for defect-image diagnosis.
- **Deployment:** consider edge (local) inference versus cloud for latency, network availability and data privacy of shop-floor data.
- **HMI:** intent-driven natural-language interface lowers the barrier for machine operators who are not data experts — a usability point for the FYP's front end.
- **Literature framing:** useful for the FYP background chapter on the move from rule-based expert systems to foundation-model-based industrial assistants.
