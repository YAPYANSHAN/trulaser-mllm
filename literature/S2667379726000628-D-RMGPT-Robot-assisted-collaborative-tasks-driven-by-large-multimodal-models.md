# D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models

- **Citation (IEEE):** M. Forlini, M. Babcinschi, G. Palmieri, et al., "D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models," *Biomimetic Intelligence and Robotics*, vol. 6, art. 100334, 2026, doi: 10.1016/j.birob.2026.100334.
- **Domain:** Human-robot collaboration; LMM-based perception and task planning for assembly and cooking.
- **Relevance to FYP (1-5):** 3 - industrial manufacturing use of off-the-shelf GPT-4V/GPT-4 with zero-shot image perception; the prompt-engineering lessons for reducing VLM hallucination transfer directly to defect inspection.

## Problem
Human-robot collaboration interfaces are usually highly customised and rely on costly training data. The authors want a general, marker-free, training-free planner. It should help inexperienced operators with tasks that have precedence constraints, and it should adapt when the operator ignores its advice.

## Data & modalities
- RGB images from two cameras.
- One "component list" image that encodes the parts, their descriptions and their assembly precedence dependencies.
- Speech commands and pointing gestures.
- Human-action video clips, classified by a 3D CNN-LSTM.
- Test cases: a toy aircraft from the YCB dataset (8 components plus a power tool, screws and nuts) and pizza preparation.

## Method
- **DetGPT-V:** GPT-4V, later replaced by GPT-4o. It does one-shot perception from prompted images, detecting which components or ingredients are present, what the operator is pointing at, and what speech commands mean.
- **R-ManGPT:** GPT-4. It acts as the operations and task manager, planning the next step and producing discrete robot actions. A 3D CNN-LSTM action classifier (100% test accuracy reported) feeds it.
- **Precedence constraints:** solved by giving the model a single image that lists all precedence relationships, not by using a graph solver.
- **No fine-tuning.** The authors refined the prompt step by step. The final form asks each component a separate, targeted YES/NO question in an isolated query, with a schematic output format and system/assistant/user roles. An earlier version that asked the model to reason over precedence and double-check its answer gave non-deterministic results.

## Results
- Assembly success rate: 83%. Pizza task: 87% (Wilson 95% CI 67.87-95.46%). Overall: 86.8% (CI 73.0-94.2%).
- Assembly time for inexperienced operators was about 33% lower than manual assembly (mean 311 s).
- DetGPT-V had higher precision and recall than ViLD and OWL-ViT. The open-vocabulary detectors confused parts with similar colour and shape.
- Detection hallucinations: 22 out of 840 opportunities (2.3%).
- Prompt redesign cut GPT response time from 25.7 s to 14.2 s (44.7%).
- GPT processing takes about 30% of total assembly time.
- Speech and pointing inputs were identified correctly 98.5% of the time.

## Limitations
- The model struggles to count components and locate them in the image.
- Results depend heavily on the prompt; less structured prompts gave lower accuracy.
- Cloud inference adds latency.
- The task fails when false positives break an essential precedence constraint.
- Only two scenarios were tested, each with a small number of trials (15).
- The model itself has no verification layer.

## Transferable ideas for the FYP pipeline
- **Vision:** for defect checks, ask the VLM one narrow YES/NO question per defect type (dross, burr, striations, incomplete cut, bevel-angle deviation) in a separate query, instead of one open-ended request. Per the paper, this lowers hallucination and response time.
- **Fusion / LLM reasoning:** encode process rules (cause-effect tables, parameter precedence) as a compact reference that sits in the context window, the way the component-list image is used here.
- **LLM reasoning:** add a verification pass that re-queries each newly claimed fault before the final diagnosis, as the authors' proposed fallback does.
- **Evaluation:** report success rates with Wilson confidence intervals, count hallucinations against the number of error opportunities, and log latency per step.
- **Deployment:** keep perception, reasoning and actuation as decoupled modules so that one perception error does not spread into an unsafe recommendation.
