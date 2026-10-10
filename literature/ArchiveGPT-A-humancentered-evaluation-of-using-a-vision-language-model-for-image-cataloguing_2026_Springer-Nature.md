# ArchiveGPT: A Human-Centered Evaluation of Using a Vision Language Model for Image Cataloguing

- **Citation (IEEE):** L. Abele, G. Anders, T. Aydın, et al., "ArchiveGPT: A human-centered evaluation of using a vision language model for image cataloguing," *Humanities and Social Sciences Communications*, vol. 13, art. 1241, 2026, doi: 10.1057/s41599-026-08367-6.
- **Domain:** Digital humanities / archives (GLAM) / human-AI evaluation of VLM output
- **Relevance to FYP (1-5):** 2 - unrelated domain, but a useful case of an off-the-shelf VLM filling a structured template from image+text, with documented hallucination modes and a human-in-the-loop evaluation design.

## Problem
Photographic archives grow faster than manual cataloguing. Can a VLM draft catalogue descriptions that approach expert quality, and will archive professionals trust and adopt such a tool?

## Data & modalities
Photographic prints on labelled cardboard mounts (image + printed/handwritten label text) with archaeological content from the Leibniz-Zentrum für Archäologie (LEIZA). 40 items, each with an expert-written and an AI-generated description following a common catalogue template. Online experiment with N = 139 participants (experts - students and professionals in archive/archaeology - and non-experts).

## Method
InternVL2-Llama3-76B (open-source VLM, chosen for top OpenCompass multimodal ranking, Aug 2024) with few-shot prompting and a detailed template-filling prompt; no fine-tuning. Three generations per item with varied generation parameters; a non-expert "human in the loop" selected the best one (preferring missing-field errors over misplaced fields or hallucinations); then translated to German and expert-verified. Participants rated accuracy and usefulness, judged AI vs expert authorship, estimated their own detection ability, and reported trust/willingness to use AI. Analysis with GLMMs and signal-detection (d').

## Results
Detection was above chance: accuracy ranged from 54.9% (non-experts on AI texts) to 67.8% (experts on expert texts); main effect of description type χ²(1)=31.58, p<.001; no significant effect of expertise. Participants underestimated their detection ability (self-estimate 49.23% vs actual 61.99%). Descriptions rated more accurate and useful were harder to identify as AI. Three VLM error types: "Not given" for fields actually present, correct info in the wrong field, and hallucinated content; OCR errors limited quality. Experts were less willing to adopt AI tools, citing preservation responsibility.

## Limitations
Translation step may have altered meaning; small, heterogeneous expert group (many students); generic rather than model-specific trust measures; only 40 items; human curation means results do not reflect raw model output.

## Transferable ideas for the FYP pipeline
- **LLM reasoning:** structured output templates (fixed fields) for diagnosis reports, plus explicit "not available" handling - and validation that checks each field against the source evidence to catch misplaced or hallucinated values.
- **Vision / ingestion:** expect OCR errors when a VLM reads labels, nameplates or HMI screenshots on the TruLaser; extract text with a dedicated OCR step or from the machine database rather than relying on the VLM.
- **Evaluation:** blinded expert rating of LLM vs engineer-written diagnoses (accuracy, usefulness) and a trust/adoption questionnaire for TRUMPF operators; generate several candidates and select/verify (best-of-n with human or rule check).
- **Deployment:** position the system as draft generator under engineer verification to address professional trust concerns.
