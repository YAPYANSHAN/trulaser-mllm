# Large models for machinery fault diagnosis: Current advances and future directions

- **Citation (IEEE):** R. Yan, J. Ren, J. Wen, et al., "Large models for machinery fault diagnosis: Current advances and future directions," *Chinese Journal of Mechanical Engineering*, vol. 39, Art. no. 100277, 2026, doi: 10.1016/j.cjme.2026.100277.
- **Domain:** Industrial machinery fault diagnosis / review of LLMs and multimodal large models
- **Relevance to FYP (1-5):** 5 - a comprehensive roadmap of LM-driven machinery fault diagnosis. It covers fine-tuning, ICL, RAG, multimodal alignment, knowledge enhancement, agents and lightweight deployment, and forms the backbone of a literature review for this FYP.

## Problem
Statistical and deep-learning fault diagnosis generalises poorly across scenarios when data are scarce. Large models (GPT, DeepSeek, Qwen, multimodal LMs) promise few- and zero-shot diagnosis, but systematic reviews of the evolution of this field and its future directions are lacking.

## Data & modalities
A review based on Web of Science publication trends. It covers vibration, acoustic, thermal images, operation logs, maintenance documents and time series.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **Past:** machine learning (SVM, k-NN, ANN), deep learning and transfer learning for machinery fault diagnosis (MFD).
- **Present:** foundations of LMs, pre-trained models, and fine-tuning taxonomies:
  - additive: adapters, prefix tuning, side tuning, prompt tuning
  - reparametrised: LoRA
- **Two-perspective taxonomy:**
  - "LM for MFD": ICL-based, fine-tuning-based and RAG-based adaptation of existing LMs
  - "LM of MFD": purpose-built language-based, multimodal and time-series LMs, which convert signals to text, fuse heterogeneous data, or tokenise time series
- **Future directions:**
  - reasoning-driven MFD
  - knowledge-enhanced MFD (KG in pre-training, knowledge-consistency losses, RAG)
  - multimodal MFD, with four alignment strategies: linear feature projection, scaling up encoders (e.g., ViT-22B), adapters and Q-Former perceivers
  - agent-empowered MFD
  - continual learning
  - lightweight/edge deployment
- **Discussion:** data sufficiency, reliability under limited data, real-time deployment, and how LMs relate to small models. In the LM-centred paradigm, small models extract features for the LM. In the small-model-centred paradigm, the LM orchestrates them as an agent.

## Results (key numbers and metrics)
A review with no new experiments. Tables 1-2 summarise reviewed works with their advantages and limitations.

## Limitations
- Qualitative synthesis with no quantitative benchmark comparison.
- Coverage is focused on rotating machinery (vibration).
- Manufacturing processes such as laser cutting are not specifically treated.

## Transferable ideas for the FYP pipeline
- **Architecture choice:** adopt the "small-model-centred, LM-as-orchestrator" pattern. Specialised small models (a defect-image CNN/YOLO, a tabular anomaly detector on machine tables) feed evidence to an LLM agent that reasons and explains.
- **Fusion:** start with linear projection of encoder features into the LLM embedding space (simplest). Consider a Q-Former/adapter if noise is high.
- **Text/RAG + KG:** knowledge-enhanced reasoning using TruLaser manuals, with consistency constraints against fault mechanisms.
- **Fine-tuning:** LoRA or prompt tuning as the cheapest adaptation route.
- **Deployment:** lightweight optimisation (quantisation, distillation) for shop-floor PCs. Continual learning for new fault types.
