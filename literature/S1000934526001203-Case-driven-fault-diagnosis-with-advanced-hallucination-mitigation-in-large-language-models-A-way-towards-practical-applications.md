# Case-driven fault diagnosis with advanced hallucination mitigation in large language models: A way towards practical applications

- **Citation (IEEE):** H. Liu, L. Tao, H. Ji, et al., "Case-driven fault diagnosis with advanced hallucination mitigation in large language models: A way towards practical applications," *Chinese Journal of Mechanical Engineering*, vol. 39, Art. no. 100331, 2026, doi: 10.1016/j.cjme.2026.100331.
- **Domain:** Industrial PHM / fault diagnosis (power transformers) with structure-constrained reasoning
- **Relevance to FYP (1-5):** 4 - turns fault cases and documents into fault trees and hypergraphs, and enforces logical constraints to suppress hallucinated diagnostic paths. This is highly relevant to evidence-based diagnosis, although the LLM role is minor.

## Problem
LLM-based PHM diagnosis suffers from three kinds of hallucination: (1) broken or fragmented diagnostic paths across hierarchical knowledge (fault trees, technical roadmaps); (2) logical conflicts and missing constraints (order, mutual exclusion, compliance); (3) false node activation under weak or noisy signals. As a result, case-driven diagnosis produces inexecutable or contradictory solutions.

## Data & modalities
- The team's PHM corpus of 16,472 patents, from which 309 power-transformer fault diagnosis and handling documents were selected.
- LLM extraction plus expert verification converted these into fault trees (FTA) in Mermaid Markdown, then into multi-scale hypergraphs (JSON).
- Five scenes: gas/oil anomaly, winding, bushing/insulation, core/structural, lightning/overvoltage.
- Samples are depth-3 diagnostic paths, with negatives in a 1:3 ratio: temporal reversal, missing step and semantic interference. Split 7:2:1 with no leakage.
- Qwen-Plus (DashScope API) generated 20 natural diagnostic questions per scene.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
The SC-MDG framework has four modules:
- **MSSE (multi-scale structure-aware encoder):** unifies heterogeneous diagnostic graphs via cross-layer node alignment and a standard event dictionary.
- **SCOC (structural consistency optimisation controller):** encodes sequential, mutual-exclusion and compliance constraints in a differentiable optimisation that reconciles conflicting paths.
- **HSP (hypergraph spike perceptor):** spiking gating plus Bayesian uncertainty propagation regulate node activation under weak signals. It is backed by a "Signal Propagation Theorem".
- **EGR (evidence-guided generation and ranking):** outputs ranked, executable, interpretable diagnostic solutions.

The LLM is used only for query generation (temperature 0.7, top-p 0.9). The authors stress that the accuracy gains come from the structural framework, not from LLM post-correction. Training is phased: nodes, then consistency, then ranking.

## Results (key numbers and metrics)
- Across five diagnostic scenarios, an average accuracy improvement of 15% over six state-of-the-art methods (e.g., GNN+LLM, Bayesian+LLM).
- Clear superiority in suppressing hallucinations.
- Metrics include accuracy, F1, RMSE and structural consistency.
- The ablation shows a trade-off: GNN gives higher accuracy and F1, while SNN gives better robustness and speed.

## Limitations
- Single domain (transformers).
- Datasets and labels are generated automatically from fault trees, so they are rule-derived rather than field-validated.
- Heavy, complex architecture.
- Real-time latency not yet addressed.
- Cross-domain transfer is future work.

## Transferable ideas for the FYP pipeline
- **Text/RAG + KG:** convert TruLaser troubleshooting knowledge into fault trees, e.g., Mermaid Markdown that an LLM can read and generate (top event "poor bevel edge quality" → gas pressure / nozzle / focus / feed). Parse these into a graph.
- **LLM reasoning:** check LLM-proposed diagnostic chains against explicit constraints: order (check nozzle before lens), mutual exclusion and compliance with the machine's limits. Reject or re-rank violating paths.
- **Evaluation:** build hard negatives (reversed, missing-step and distractor paths) to test whether the reasoning module detects invalid chains, and report a hallucination metric.
- **Data ingestion:** use an LLM to synthesise realistic operator questions from fault-tree nodes for test sets.
