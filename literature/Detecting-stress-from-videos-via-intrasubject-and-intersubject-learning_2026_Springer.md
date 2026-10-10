# Detecting stress from videos via intra-subject and inter-subject learning

- **Citation (IEEE):** Y. Ding, Y. Dai, L. Cao, et al., "Detecting stress from videos via intra-subject and inter-subject learning," *Health Inf. Sci. Syst.*, vol. 14, art. 53, 2026, doi: 10.1007/s13755-026-00450-1.
- **Domain:** Affective computing / video-based mental stress detection (health informatics)
- **Relevance to FYP (1-5):** 2 — unrelated domain, but its patterns transfer: baseline deviation, retrieval of similar reference cases as in-context examples, and instruction tuning of Qwen2-VL with extra feature tokens.

## Problem
Video stress detectors assume uniform labels across subjects, but stress responses differ strongly between individuals. Grounded in allostasis theory, the authors model stress as a personalised deviation from each subject's own resting physiological baseline rather than as an absolute state.

## Data & modalities
RGB facial videos from the UVSD, RSL and MuSE datasets (MuSE: 28 students; exam vs. non-exam period used for long-term stress). Physiological signals (rPPG pulse, HRV/RMSSD) are derived contactlessly from video. Facial expression features and text prompts are also used.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- **CalmScore:** selects each subject's most relaxed reference clip using resting HRV.
- **Visual encoder:** pre-trained with multiple tasks: rPPG regression (negative-Pearson loss) and emotion-semantic learning.
- **PD-RAM:** computes multimodal feature deviations between the current and resting states and modulates them by resting RMSSD (a proxy for regulation capacity). A learnable linear layer projects them into "discrepancy tokens" in Qwen2-VL's embedding space. These are concatenated with Qwen2-VL visual and prompt tokens.
- **IS-ICIT:** a physiology-aware retriever finds the reference subject with the closest resting RMSSD. That subject's stressed, unstressed and resting clips become in-context exemplars, and Qwen2-VL is instruction-tuned with these contrastive prompts and varied prompt formulations.

## Results (key numbers and metrics)
- UVSD: accuracy 96.89%, F1 96.85%. RSL: accuracy 91.01%, F1 88.67%.
- The best zero-shot foundation model, GPT-4V, reached F1 74.06% (UVSD) and 62.75% (RSL), giving gains of +22.79 and +26.60 F1 points.
- Also outperformed the earlier best supervised method and was evaluated on MuSE long-term stress.
- Ablations show each component is needed, and that random or partial retrieved exemplars perform worse than the full scheme.

## Limitations
Resting baselines are not collected under standardised lab conditions. Each subject has a single resting reference with no longitudinal refinement. Data are scarce, and generalisation across populations is untested.

## Transferable ideas for the FYP pipeline
- **Tabular/time-series (baseline deviation):** represent machine state as a deviation from a "golden"/nominal baseline for the same material–thickness–program (e.g., expected vs. actual cutting speed, gas pressure, laser power). Feed the deviations, not just absolute values, to the LLM.
- **Text/RAG (retrieval of similar cases):** retrieve historical jobs with similar machine and material signatures, including both good and defective examples, as contrastive in-context exemplars for diagnosis.
- **Fusion:** project numeric feature vectors into the VLM token space with a learned linear adapter. This is a lightweight way to inject sensor/table features into Qwen2-VL-class models.
- **Fine-tuning:** use instruction tuning with paraphrased prompt variants to make the model robust to how operators phrase questions.
- **Evaluation:** compare against zero-shot GPT-4V/Gemini baselines and run ablations on the retrieval strategy.
