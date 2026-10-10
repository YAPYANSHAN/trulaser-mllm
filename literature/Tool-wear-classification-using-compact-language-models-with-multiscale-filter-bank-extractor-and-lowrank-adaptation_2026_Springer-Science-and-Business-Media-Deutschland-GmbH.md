# Tool wear classification using compact language models with multi-scale filter bank extractor and low-rank adaptation

- **Citation (IEEE):** D. H. Nguyen, T. S. Pham, and N. D. M. Phan, "Tool wear classification using compact language models with multi-scale filter bank extractor and low-rank adaptation," *Signal, Image and Video Processing*, vol. 20, Art. no. 660, 2026, doi: 10.1007/s11760-026-05727-2.
- **Domain:** Industrial fault diagnosis / machining tool-condition monitoring with LLMs
- **Relevance to FYP (1-5):** 4 - an industrial manufacturing diagnosis using compact LLMs with LoRA. It fuses learned sensor embeddings with prompt-encoded statistical descriptors in the LLM embedding space, which directly shows how to feed machine data to an LLM.

## Problem
Deep-learning tool-wear monitoring often relies on large, compute-heavy models that are hard to deploy. Existing LLM fault-diagnosis approaches (FD-LLM etc.) use fixed signal-to-text transforms or complex alignment. The authors want an efficient way to learn from raw signals and keep interpretable statistics available for LLM reasoning.

## Data & modalities
- MATWI dataset (licensed, not public): acceleration (vibration) and cutting forces Fx/Fy.
- Turning of CK45 and RVS 304 stainless steel without coolant, under varied cutting parameters.
- Binary label (safe/unsafe) from a wear threshold. Stratified 80:20 split over non-overlapping windows.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
1. **Multi-scale filter bank extractor:** a parallel multi-kernel CNN with squeeze-and-excitation attention, applied to the raw signals (implicit features).
2. **Feature projector** into the LLM token-embedding space.
3. **Prompt embeddings** carry explicit statistical descriptors (e.g., mean, RMS, other statistics) as text cues.
4. A **compact LLM backbone** with a classification head, fine-tuned with **LoRA**.

Backbones tested: Qwen2.5-0.5B, Qwen2.5-1.5B, Llama-3.2-1B, Gemma-3-1B and SmolLM2-1.7B. Baselines: BiLSTM, CNN-LSTM and CWT-image CNNs (EfficientNet-CWT, etc.). Embedding-space analysis uses silhouette scores.

## Results (key numbers and metrics)
- Best mean accuracy 94.96% and weighted F1 94.89%. All five backbones score about 94%, with low variance.
- The strongest baseline, EfficientNet-CWT, reaches about 91%.
- Removing the filter bank: -6.49% accuracy and -6.82% F1 on average.
- Replacing the LLM with an MLP: -8.76% accuracy and -4.26% precision.
- LoRA cuts trainable parameters while keeping full fine-tuning quality.
- The LLM makes the clusters more compact and separable (silhouette analysis with SmolLM2).

## Limitations
- One binary dataset under fairly consistent conditions.
- No tool-disjoint or leave-one-set-out evaluation (cross-condition generalisation untested).
- Baselines include no other LLM-based methods.
- The dataset is not public.
- Binary output only, without textual explanation.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series → LLM fusion:** project learned embeddings of machine time series (laser power, gas pressure, axis loads, sensor logs) into the LLM as soft tokens. Alongside them, put a text prompt listing explicit statistics and table values (e.g., "mean cutting speed = X m/min, gas pressure = Y bar, material = 1.4301, 10 mm"). This hybrid of implicit and explicit features beat either alone.
- **Fine-tuning / deployment:** 0.5-1.7B models with LoRA run on modest hardware near the machine. Compare several small backbones, as done here.
- **Evaluation:** use leave-one-job, leave-one-material or leave-one-machine-condition splits to test generalisation, which this paper lacks. Include an LLM-based baseline and run ablations that remove each component.
- **Interpretability:** check whether the LLM improves class separability with embedding analysis (t-SNE, silhouette).
