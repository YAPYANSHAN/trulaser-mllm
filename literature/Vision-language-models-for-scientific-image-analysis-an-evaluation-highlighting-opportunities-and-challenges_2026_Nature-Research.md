# Vision language models for scientific image analysis: an evaluation highlighting opportunities and challenges

- **Citation (IEEE):** P. Verma, M.-H. Van, and X. Wu, "Vision language models for scientific image analysis: an evaluation highlighting opportunities and challenges," *npj Computational Materials*, vol. 12, art. 218, 2026, doi: 10.1038/s41524-026-02069-y.
- **Domain:** Materials science and biology microscopy (SEM and fluorescence); zero-shot benchmarking of VLMs and SAM.
- **Relevance to FYP (1-5):** 4 - SEM images of materials are close in spirit to cut-edge and micrograph defect images. The paper benchmarks the same off-the-shelf VLM families the FYP could use, with concrete failure modes (scale bar, overlaps, class-order bias).

## Problem
How well do general-purpose VLMs and SAM handle expert microscopy tasks (classification, segmentation, counting, VQA) without any training? Where do they fall short of domain experts and trained CNNs?

## Data & modalities
- **NFFA-Europe 100% SEM dataset:** 10 classes, including fibres, nanowires, particles, powder, MEMS, patterned surfaces, tips and films.
- **BBBC005:** synthetic fluorescence cell images, split into a w1 subset (isolated cells) and a w2 subset (agglomerated cells).
- **Other images:** neuron and cell-division images for VQA.
- **Ground truth:** expert-made ground truths for counts and sizes are released on GitHub.
- Modalities are images plus text prompts.

## Method
- **Models:** ChatGPT-5 (web browser), Gemini-2.5 Pro (API and browser), Llama-3.2-Vision and LLaVA-1.5 (local), and SAM-2 (local, with standard and custom parameters).
- **Evaluation protocol:** standardised single-turn, zero-shot prompting for parity across models. There is no fine-tuning, RAG, chain-of-thought or self-consistency in the scored runs.
- **Tasks:**
  - classification across 10 SEM classes;
  - segmentation (SAM-2 versus ChatGPT running thresholding code);
  - counting, scored with MAPE;
  - five VQA subtasks: describe, size/count, stage identification, upscaling, and deblurring.
- **Illustrative follow-ups (not scored):** scale-aware re-prompting, a crop → threshold → watershed instruction, and depth-aware counting.

## Results
- **Classification:** Gemini 76.7% and ChatGPT 61.2% overall. Both exceeded 60% on fibres, coated films, particles, sponges and tips.
- **Classification failure modes:**
  - ChatGPT confused nanofibres with fibres when it ignored the scale bar.
  - LLaVA was biased towards the classes listed first in the prompt.
  - Llama never predicted the last class and was biased towards classes in the middle of the list.
- **Trained baselines for reference:** Inception-v3 reached 89.8% on NFFA in prior work, and CNNs reached 97.1% on a 3-class subset. Zero-shot VLMs lag these.
- **SAM-2 counting (MAPE):** custom parameters gave 4.83% versus 5.12% on w1, and 18.40% versus 40.77% on w2.
- **ChatGPT-code counting:** MAPE 7.8% on w1.
- **Other models on counting:** Gemini and Llama counted visually, close to ChatGPT-visual, but underestimated at high counts. LLaVA defaulted to round numbers.
- **VQA:**
  - All models read text and scale bars accurately and gave good descriptions.
  - Counting was weaker than size estimation.
  - Upscaled or "in-focus" images may contain invented detail.
  - Generated images and methods were inconsistent across repeated runs.

## Limitations
- Mostly browser-based runs.
- Results for some models come from sampled subsets.
- The scored runs use zero-shot prompting only, with no prompt-strategy study.
- VQA is evaluated qualitatively.
- Commercial models are black boxes.
- There is no head-to-head comparison with trained baselines.
- Impurities, overlaps and artefact diversity degrade all models.

## Transferable ideas for the FYP pipeline
- **Vision:** use SAM-2 (with tuned parameters) for instance isolation and measurement, such as dross droplets or striation regions. Use the VLM for semantic interpretation and rationale. The paper finds this division of labour more reliable than VLM-only counting.
- **LLM reasoning (prompting):** always tell the model to use the scale and calibration reference (pixel-to-mm, kerf width) and give expected dimension ranges. Randomise or balance the order of class options to avoid position bias.
- **Vision (tool use):** have the LLM run a fixed classical pipeline (crop → threshold → watershed) instead of choosing its own algorithm, which varies quality.
- **Evaluation:**
  - Report per-class confusion.
  - Use MAPE for counts and measurements.
  - Compare zero-shot VLMs against a small trained CNN baseline.
  - Test repeatability across runs.
- **Deployment:** do not use generative "enhancement" (upscale or deblur) on defect evidence, because it can invent detail.
