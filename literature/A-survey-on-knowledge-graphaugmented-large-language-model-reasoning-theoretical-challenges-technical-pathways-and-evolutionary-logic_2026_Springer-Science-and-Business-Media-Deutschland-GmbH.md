# A survey on knowledge graph-augmented large language model reasoning: theoretical challenges, technical pathways, and evolutionary logic

- **Citation (IEEE):** J. Wu, Y. Zhao, Z. Liao, et al., "A survey on knowledge graph-augmented large language model reasoning: theoretical challenges, technical pathways, and evolutionary logic," *Knowledge and Information Systems*, vol. 68, art. 261, 2026, doi: 10.1007/s10115-026-02880-5.
- **Domain:** NLP / neuro-symbolic AI, KG + LLM reasoning (survey)
- **Relevance to FYP (1-5):** 4 - a structured map of KG-LLM integration methods (KG prompting, KG-RAG, fine-tuning, reasoning-model collaboration, knowledge agents) that the FYP can use to choose and justify its evidence-grounded reasoning design.

## Problem
LLMs suffer factual hallucination, limited multi-step reasoning and opaque decisions; KGs offer structured, explainable knowledge, but integrating the two remains difficult. Existing surveys mostly catalogue methods without a theory of why integration is hard.

## Data & modalities
Survey (text and knowledge graphs; domain applications in health care, law and scientific research).

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- "Root-phenomenon-consequence" framework grounded in neuro-symbolic cognitive science (System 1 / System 2): three fundamental challenges - representation gap, synergy bottleneck, paradigm conflict.
- Five-dimensional taxonomy, evolving from external guidance to autonomous cognition: (1) prompt engineering (e.g., Think-on-Graph iterative graph search, KG-GPT, RoK with PageRank path filtering, KG-CoT, MindMap evidence graphs, KICGPT); (2) retrieval-augmented generation (KG-RAG, GraphRAG); (3) model fine-tuning with KG knowledge; (4) collaboration with large reasoning models; (5) knowledge agents.
- Comparison tables of core mechanism, KG utilisation, strengths and limitations per method.

## Results (key numbers and metrics)
Qualitative synthesis. Key observations: prompt methods are training-free and traceable but need many LLM calls; linearised prompts lose graph structure; most systems treat the KG as authoritative with no arbitration for conflicts between KG and LLM conclusions; RAG optimises knowledge delivery without true representational alignment.

## Limitations
Survey only, no benchmark; open problems in neuro-symbolic alignment, knowledge timeliness, conflict resolution, and cost of iterative graph reasoning.

## Transferable ideas for the FYP pipeline
- **Text/RAG (KG):** start with training-free KG prompting (Think-on-Graph / KG-CoT style) over a laser-cutting KG (defect -> cause -> parameter -> remedy), moving to KG-RAG and agents if needed.
- **LLM reasoning:** generate explicit reasoning paths (e.g., "dross on bottom edge -> low gas pressure or high speed -> check job parameters") from the KG and pass them as CoT evidence; MindMap-style evidence graphs give transparent explanations.
- **Fusion / reliability:** add a conflict-arbitration step when sensor/database evidence, image evidence and manual-based KG knowledge disagree, rather than always trusting the KG.
- **Evaluation:** measure number of LLM calls/latency as well as accuracy and faithfulness of reasoning paths.
