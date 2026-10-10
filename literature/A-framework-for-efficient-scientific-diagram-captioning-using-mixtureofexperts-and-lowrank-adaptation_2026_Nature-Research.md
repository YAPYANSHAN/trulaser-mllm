# A framework for efficient scientific diagram captioning using mixture-of-experts and low-rank adaptation (LoRaMoE-Cap)

- **Citation (IEEE):** D. Kamboj and G. Harit, "A framework for efficient scientific diagram captioning using mixture-of-experts and low-rank adaptation," *Scientific Reports*, vol. 16, art. 21556, 2026, doi: 10.1038/s41598-026-51267-7.
- **Domain:** Vision-language / scientific diagram captioning
- **Relevance to FYP (1-5):** 3 - LoRA + Mixture-of-Experts captioning of technical diagrams relates to interpreting engineering drawings/manual figures and to routing inputs to defect-specific experts at low inference cost.

## Problem
Diagrams (biology, astronomy, engineering circuits) have complex layouts, symbols and text-graphic interplay; general VLMs (BLIP-2, MiniGPT-4, LLaVA) are slow and not tuned for this. AI2D lacks captions for supervised training.

## Data & modalities
Diagram images + text captions. New AI2D-Caption dataset: 4,908 AI2D diagrams (Astronomy 1,124; Biology 3,524; Engineering circuits 153; Others 107) captioned by ~50 postgraduate domain annotators under faculty supervision.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Two stages: (1) pretraining to align visual and textual modalities into a unified multimodal representation; (2) fine-tuning in which the representation is routed by a gating network to parallel domain experts, each adapted with LoRA.
- Sparse MoE: only a subset of experts is active per input; KL-based regularisation encourages balanced, stable expert utilisation.
- All experts trained under a shared caption-generation objective (roles emerge implicitly).
- Baselines: zero-shot BLIP-2, MiniGPT-4, LLaVA and others. No RAG/KG.

## Results (key numbers and metrics)
- Average BLEU 0.42 and average SPICE 0.38, outperforming zero-shot VLM baselines.
- Average inference time about 3 s per diagram, with fewer parameters than competing models.
- Qualitative analysis on low-resolution diagrams shows factual errors (e.g., reversed subduction direction, wrong rock-cycle transitions), i.e., hallucination persists.

## Limitations
No explicit evidence that experts specialise in distinct diagram aspects; comparisons are against zero-shot baselines rather than matched parameter/data budgets; errors on low-resolution diagrams; small engineering subset.

## Transferable ideas for the FYP pipeline
- **Text/RAG / data ingestion:** captioning figures in TRUMPF manuals (cutting-head schematics, parameter charts) into text makes them indexable for RAG; a LoRA-tuned captioner can be trained on a few thousand annotated figures.
- **LLM reasoning:** MoE-with-LoRA routing idea: one LoRA adapter per defect family or material class, with a gating step (or simple router on detected defect type) selecting the adapter, keeping inference cheap.
- **Fine-tuning:** two-stage align-then-specialise training schedule.
- **Evaluation:** include qualitative error audits for factual inversions (e.g., "increase" vs "decrease" gas pressure), not only BLEU/SPICE; low-resolution input robustness should be checked.
