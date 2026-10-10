# NavAI: an application-agnostic LLM framework for navigation tasks in virtual reality environments

- **Citation (IEEE):** J. Wang, S. S. Letha, M. DiGiovanni, et al., "NavAI: an application-agnostic llm framework for navigation tasks in virtual reality environments," *Automated Software Engineering*, vol. 33, art. 124, 2026, doi: 10.1007/s10515-026-00676-z.
- **Domain:** Software engineering / VR automated testing — VLM-driven agents
- **Relevance to FYP (1-5):** 2 — unrelated application, but gives measured evidence on hybrid local-detector + cloud-VLM pipelines and multi-model voting cost/benefit, relevant to FYP deployment design.

## Problem
Automated navigation in general VR applications (unseen scenes, dynamic interactions) is hard for vision-language navigation methods trained on 360° datasets or specific simulators. The authors want an application-agnostic, screenshot-and-control LLM navigation framework and to quantify trade-offs of optimisation strategies.

## Data & modalities
Screenshots from two Unity environments (indoor and outdoor) across three distance regimes; text commands/goals; control primitives. Each configuration run six times; ground truth for success established by multi-annotator consensus (κ = 0.83).

## Method
- Pipeline split into **perception, decision making and control execution**: Action Navigator (maps natural-language commands to control primitives), Comprehensive Interpreter (scene grounding + multi-step state), Decision Voter.
- Models: gpt-4o-2024-08-06 (visual interpretation/action selection), gpt-4o-mini (termination voter), gemini-2.5-flash, grok-2-vision.
- **Hybrid perception:** COCO-pretrained YOLOv8n (no fine-tuning) gates/grounds objects first, with LLM textual scene description as fallback.
- **Full Mode:** three models invoked sequentially with majority voting for goal checking and action selection.
- Metrics: success rate, end-to-end latency, token consumption per stage.

## Results
- Full Mode: 100% success in all environments; Gemini single-model variants (with/without YOLO) also 100% without voting.
- Outdoors, YOLO-assisted variants cut navigation time by up to ~53% and tokens by up to ~82% vs LLM-only; small overhead indoors.
- Full Mode uses 1.2–1.9× tokens of single models indoors and up to ~2.9× of Gemini+YOLO outdoors; latency per attempt ~15–220 s.
- Action Navigator mapped all seven tested commands correctly, mean overhead 0.74 s.
- GPT and Grok variants sensitive to environment/distance.

## Limitations
Only two Unity assets, simulator without headset; small number of scenarios (descriptive, low statistical power); LLM nondeterminism and non-pinned model endpoints; latency too high for real-time use; path quality not measured.

## Transferable ideas for the FYP pipeline
- **Vision / deployment:** run a cheap local detector (YOLO) on cut-part images first and pass detections/crops to the MLLM — reduces tokens and latency; fall back to full-image MLLM description when the detector finds nothing.
- **LLM reasoning:** multi-model voting gives cross-verification but may not raise accuracy over the best single model — measure before adopting; consider it only for high-stakes diagnoses.
- **Evaluation:** log per-stage token usage and latency alongside accuracy; repeat runs to account for LLM nondeterminism; pin model versions for reproducibility.
- **Architecture:** modular perception → reasoning → action separation maps onto image analysis → diagnosis → recommended parameter change.
