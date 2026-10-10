# Harnessing multimodal large language models to interpret ecological momentary assessment-generated caregiving photographs

- **Citation (IEEE):** C. Muasher-Kerwin, M. C. Hughes, A. Sanatizadeh, et al., "Harnessing multimodal large language models to interpret ecological momentary assessment-generated caregiving photographs," *Discover Artificial Intelligence*, vol. 6, Art. no. 152, 2026, doi: 10.1007/s44163-026-00879-z.
- **Domain:** Healthcare / digital health: zero-shot GPT-4 interpretation of caregiver photographs and text.
- **Relevance to FYP (1-5):** 2 - unrelated domain and a small pilot study, but it is a clear template for *human-expert evaluation* of zero-shot MLLM image interpretations and shows the gap between "describes the image correctly" and "captures the intended meaning".

## Problem
Ecological momentary assessment (EMA) produces large volumes of photographs and short texts that clinicians lack time to review. Can a general-purpose MLLM accurately describe, interpret and summarise such photographs, with or without the accompanying text?

## Data & modalities
Images + short free text. 12 health-science students simulated glioblastoma family caregivers for 7 days (ExpiWell app, 3 prompts per day). They submitted 177 photographs of caregiving challenges or successes, each with a narrative.

## Method
- Model: GPT-4 (multimodal) through private Microsoft Azure for data security. Zero-shot, no fine-tuning, no RAG.
- Prompting: a fixed background instruction; each photo labelled as challenge or success; standardised question "Based on the photo, what do you interpret as the challenge or success?"
- Synthesis: group-level top-5 challenges and successes, first from photos alone, then from photos plus text.
- Evaluation:
  - Two blinded domain experts rated each output on 4-point Likert scales for accuracy (content) and agreement (with the participant's intended meaning), after calibration on 10 photos; ICC was computed with a two-way random-effects model.
  - Safety review of each output.
  - BERT sentiment (nlptown, 5-point) on participant vs GPT-4 text.
  - all-MiniLM-L6-v2 cosine similarity between participant narratives and GPT-4 outputs.

## Results
- Accuracy mean 3.64/4; agreement with intended meaning only 2.48/4 (2.54 after removing poor photos).
- Inter-rater ICC: accuracy 0.670 (single) / 0.802 (average); agreement 0.692 / 0.818.
- Semantic similarity mean 0.296: only 4.4% above 0.60, 47.5% between 0.30 and 0.60, and 94 observations below 0.30.
- Similarity between with-text and photo-only themes: challenges 0.493, successes 0.654. Challenges needed the text more.
- Sentiment means 3.33 (participants) vs 3.40 (GPT-4); GPT-4 avoided strongly negative ratings (positive bias).
- Errors: a sideways photo was read as a broken railing; one cut described as several; an over-the-counter drug called a prescription drug.

## Limitations
Students simulating caregivers, not real caregivers; variable photo quality; the Likert scale is not psychometrically validated; one model only (GPT-4, version unknown on Azure); small sample.

## Transferable ideas for the FYP pipeline
- **Evaluation:** Rate each VLM defect explanation on two separate axes:
  - *Description accuracy*: is what is visible on the cut part described correctly?
  - *Diagnostic agreement*: does the explanation match the engineer's root cause?

  Use two blinded raters with a calibration round and report ICC.
- **Evaluation:** Add sentence-embedding similarity between the LLM explanation and the engineer's reference note as a cheap automatic proxy, but expect it to be loose (about 0.3 here).
- **Data ingestion / vision:** Normalise image orientation (EXIF rotation) before inference; a sideways photo caused a serious misreading. Enforce photo-capture guidelines (angle, lighting, scale reference) for cut-part images.
- **Fusion:** Images alone were weaker for the "problem" category, so pair defect photos with machine-log context (job parameters, alarms) rather than relying on vision only.
- **Deployment:** Use a private enterprise endpoint for proprietary machine data, as the authors did with Azure.
