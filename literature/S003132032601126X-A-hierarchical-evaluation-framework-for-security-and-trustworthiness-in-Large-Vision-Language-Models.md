# A hierarchical evaluation framework for security and trustworthiness in Large Vision-Language Models

- **Citation (IEEE):** X. Feng, M. Feng, N. Zhang, et al., "A hierarchical evaluation framework for security and trustworthiness in Large Vision-Language Models," *Pattern Recognition*, vol. 180, Art. no. 114161, 2026, doi: 10.1016/j.patcog.2026.114161.
- **Domain:** LVLM evaluation and benchmarking: ethical understanding, robustness, reasoning reliability and misuse resistance (hateful/harmful meme detection).
- **Relevance to FYP (1-5):** 2 - the subject matter (ethics/memes) is unrelated, but the evaluation methodology (prompt-permutation testing, rationale-hallucination rate, connector-architecture robustness findings) transfers to evaluating the FYP's VLM.

## Problem
LVLMs are deployed in safety-critical settings without a standard way to measure trustworthiness across modalities. Single-prompt evaluations hide prompt sensitivity and positional bias; models can be "perceptually accurate yet ethically blind"; correct answers can be reached with wrong reasoning ("Clever Hans").

## Data & modalities
Image + text (memes). VALUE-Bench: six public datasets, ten tasks - ELEMENT (unethical), CHMEMES (Chinese toxic memes), Harm-C, HMC (hateful memes), MultiOFF (offensive), Misogyny (shaming, stereotype, violence, objectification); English and Chinese; official test splits.

## Method
Four-pillar evaluation of 19 LVLMs (LLaVA, InstructBLIP, BLIP-2, CogVLM, Qwen-VL-Chat, InternVL, VisualGLM, IDEFICS, mPLUG-Owl 1/2, InternLM-XComposer 1/2, MoE-LLaVA, Monkey, SPHINX, Honeybee, MMICL, MiniCPM-V, VisCPM) plus text LLMs/commercial APIs (ChatGPT, ERNIE-Bot, GPT-4o, Qwen-7B, ChatGLM3, Baichuan2):
1. **Ethical understanding:** "Triple-check" - 3 templates that permute phrasing and option order; free-text answers mapped to options with all-MiniLM-L6-v2 cosine similarity (below 0.5 = refusal; calibrated on 200 samples, Cohen's kappa = 0.83).
2. **Adversarial / OOD robustness:** text attacks (delete/insert/synonym/translation; max 15% tokens, 20 greedy steps); image attacks PGD-style l-inf 8/255, 10 steps; domain/language/label-shift OOD.
3. **Reasoning reliability:** hallucination = correct label with wrong rationale, judged by Qwen-VL-Chat.
4. **Misuse resistance:** rate of correct refusals of harmful requests.
Greedy decoding, seed 42, max 64 new tokens.

## Results
- Severe prompt sensitivity: MMICL dropped from over 80% to 0% across semantically equivalent questions. Triple-check exposed positional bias (mPLUG-Owl2, VisCPM, BLIP-2, InstructBLIP anchor to one option).
- K = 3 templates cut cross-template variance by 39% vs K = 2; K = 4-5 added under 6%.
- OOD: linear/MLP-projection models (LLaVA, MiniCPM-V, VisCPM) most robust; Q-Former models at the bottom; CogVLM (17B) trailed LLaVA (13.4B) by about 16 F1.
- Rationale hallucination as high as 39.5% (SPHINX, Chinese memes).
- Misuse resistance: VisualGLM about 50% but over-defensive; InternLM-XComposer2-VL 4.4%; many models 0%.

## Limitations
Restricted to image-text meme/ethics tasks with fixed adversarial budgets; the hallucination judge is itself an LVLM; short (64-token) outputs; no industrial or technical content.

## Transferable ideas for the FYP pipeline
- **Evaluation:** Use Triple-check for the FYP's VLM: ask each defect/fault question with 3 paraphrases and rotated option order, and report the averaged score to expose prompt brittleness.
- **Evaluation:** Score the *rationale* separately from the label ("correct fault class but wrong evidence" = hallucination), since evidence-based diagnosis is an FYP goal.
- **LLM reasoning:** Map free-text VLM answers to a closed fault taxonomy via sentence-embedding similarity with a refusal threshold, so outputs stay machine-readable.
- **Vision / model choice:** Prefer VLMs with linear/MLP projectors (LLaVA-style, MiniCPM-V) over Q-Former ones for robustness to domain shift such as shop-floor photos.
- **Deployment:** Test robustness to image noise (lighting, metal reflections) and OCR-like text perturbations in operator notes.
