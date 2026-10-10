# Multimodal large language models for ADOS-M1 behavioral assessment

- **Citation (IEEE):** W. Liu, Y. Pan, D. Zhang, et al., "Multimodal large language models for ADOS-M1 behavioral assessment," *Neurocomputing*, vol. 706, Art. no. 135024, 2026, doi: 10.1016/j.neucom.2026.135024.
- **Domain:** Medical / clinical behavioral assessment (autism) with multimodal LLMs
- **Relevance to FYP (1-5):** 3 — clinical domain, but the architecture (frozen modality encoders + lightweight adapters + LoRA-tuned instruction LLM producing protocol-structured text outputs) is a close template for fusing images, tables and docs into an LLM diagnosis.

## Problem
ADOS is the gold-standard autism assessment but needs extensive expert observation. Prior AI methods predict a diagnostic label directly and ignore the structured, item-level ADOS scoring protocol, reducing interpretability and clinical compatibility.

## Data & modalities
Clinical ADOS-M1 dataset of 447 participants with refined paradigm annotations and item-level clinical scores. Recordings up to ~1 hour, split into non-overlapping 30-second clips. Modalities: video (8 FPS), audio, and dialogue transcripts (with speaker roles doctor/parent/child).

## Method
- **Visual branch:** frozen UML visual encoder (240 tokens × 1024-D) + linear projection adapter.
- **Audio branch:** frozen Whisper-large-v3 + OSUM adaptor (3 Conv1D + 4 Transformer layers + linear).
- **Dialogue branch:** speaker diarization (S2SND) → WhisperX ASR → wav2vec2 age estimation for role assignment → text transcript.
- All tokens fed to an instruction-tuned LLM (Qwen family, 0.5B to 8B; best variant VAD-Qwen3-8B) fine-tuned with LoRA.
- Two tasks reformulated as structured text generation: (1) paradigm classification of each clip, (2) item-level behavioral score prediction per ADOS rules. Clip predictions aggregated; subject-level ASD detection via rule-based ADOS algorithm or ML classifier.

## Results
- Paradigm classification accuracy 73.77% (best model).
- Mean item-level accuracy 72.61% at clip level.
- Subject-level ASD detection up to 86.67% accuracy (doctor-annotated ground truth); outperforms unimodal, conventional multimodal fusion and script-centric baselines; larger instruction-tuned LLMs perform better.

## Limitations
Requires controlled recording environments with synchronized audio/video; temporal perception of long videos limited; single ADOS module and one clinical site, so cross-module/dataset generalization untested.

## Transferable ideas for the FYP pipeline
- **Fusion:** freeze a vision encoder for cut-part/defect images, project its tokens with a small adapter into a Qwen3-8B-class LLM, and LoRA-tune the LLM; serialize machine-database rows as text tokens alongside.
- **LLM reasoning:** reformulate diagnosis as structured generation following an expert protocol (e.g., TRUMPF troubleshooting checklist items: edge quality, dross, kerf, burr scored per item), then derive the overall fault class by rules from item scores — interpretable and auditable.
- **Data ingestion:** a two-step pipeline (first classify which segment/image is relevant, then assess) mirrors filtering relevant sensor windows or images before diagnosis.
- **Evaluation:** report item-level and job-level accuracy separately; compare LLM sizes (0.5B → 8B).
