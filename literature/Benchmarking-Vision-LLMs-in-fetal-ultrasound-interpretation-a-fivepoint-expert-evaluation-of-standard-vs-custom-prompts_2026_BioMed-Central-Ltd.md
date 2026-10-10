# Benchmarking Vision LLMs in Fetal Ultrasound Interpretation: A Five-Point Expert Evaluation of Standard vs. Custom Prompts

- **Citation (IEEE):** W. ELsharif, M. Alzubaidi, M. Tukur, et al., "Benchmarking Vision LLMs in fetal ultrasound interpretation: a five-point expert evaluation of standard vs. custom prompts," *BioMedical Engineering OnLine*, vol. 25, art. 6, 2026, doi: 10.1186/s12938-025-01486-2.
- **Domain:** Medical imaging / zero-shot vision-LLM evaluation and prompt engineering
- **Relevance to FYP (1-5):** 2 - medical domain and tiny dataset, but shows how expert-crafted, domain-specific prompts change off-the-shelf VLM image interpretation and offers a reusable expert-rubric evaluation design.

## Problem
Can general-purpose vision LLMs interpret fetal ultrasound images, and do expert-tailored prompts improve them over generic prompts?

## Data & modalities
Nine fetal ultrasound images (anonymised teaching archive, standard views such as femur and trans-cerebellum; no pathological cases). Image + text prompt; text outputs rated by three expert sonographers.

## Method
Six vision LLMs accessed via the Chatbot Arena platform: Claude Sonnet 3.5, ChatGPT-4o, Gemini 1.5 Pro-002, Llama-3.2-Vision-90B, Pixtral-12B and Reka-Core. Zero-shot; no fine-tuning or retrieval. Two conditions: a standard generic prompt vs expert-crafted custom questions targeting five criteria - anatomical recognition, biometric potential, image quality, normality assessment, clinical recommendations - each scored 1-5 on a Likert scale (total out of 25). Statistics: repeated-measures ANOVA and Wilcoxon signed-rank tests with effect sizes.

## Results
Strong main effect of prompt type (F(1,5)=74.14, p<0.001, partial eta squared 0.921), plus question-type and interaction effects. With custom prompts, Claude Sonnet 3.5 and ChatGPT-4o reached median total scores of 19 and 18. Best on femur and trans-cerebellum images; clinical recommendations (Q5) and normality (Q4) easiest; anatomical recognition and image-quality assessment (Q1-Q3) weakest. Smaller Pixtral-12B and Reka-Core improved notably with tailoring; larger models (Llama-3.2-Vision-90B, Gemini) were inconsistent - size alone did not predict performance.

## Limitations
Only nine images (authors call it a pilot feasibility study); no pathology; gestational age unavailable for stratification; median Likert scores may miss rare critical errors; risk of hallucinated structures; closed-model versions via a public arena limit reproducibility.

## Transferable ideas for the FYP pipeline
- **LLM reasoning (prompting):** replace generic "what is wrong with this part?" prompts with engineer-designed question sets per criterion (e.g. edge quality/burr, dross, kerf width, bevel angle accuracy, likely parameter cause, recommended action) - the paper shows this is the largest single lever for zero-shot VLMs.
- **Evaluation:** a five-criterion 1-5 rubric scored by several domain experts (TRUMPF operators/engineers), analysed with Wilcoxon / ANOVA, is a practical evaluation protocol when ground truth is scarce; compare standard vs custom prompts as an ablation.
- **Vision:** expect weakest performance on fine visual measurement and image-quality judgement; delegate measurements (kerf, angle, burr height) to dedicated vision/metrology code and let the VLM interpret.
- **Model selection:** benchmark small open models with tailored prompts before assuming the largest model is needed.
