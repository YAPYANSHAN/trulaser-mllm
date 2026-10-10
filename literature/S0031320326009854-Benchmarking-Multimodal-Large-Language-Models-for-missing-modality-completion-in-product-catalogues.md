# Benchmarking Multimodal Large Language Models for missing modality completion in product catalogues

- **Citation (IEEE):** J. Fu, W. Deng, K. Zheng, et al., "Benchmarking Multimodal Large Language Models for missing modality completion in product catalogues," *Pattern Recognition*, vol. 180, art. 114020, 2026, doi: 10.1016/j.patcog.2026.114020.
- **Domain:** E-commerce / recommendation — MLLM cross-modal generation benchmark
- **Relevance to FYP (1-5):** 2 — e-commerce domain; relevant only for handling missing modalities (e.g. a fault record without an image or without a text description) and for evidence that bigger MLLMs are not always better.

## Problem
Product listings often lack images or text descriptions, harming presentation and recommendation. Can MLLMs generate the missing modality (Image→Text, Text→Image), and does it help downstream recommenders?

## Data & modalities
Amazon Reviews 2023 dataset, nine product categories; product images and textual descriptions; user–item interactions for recommendation evaluation. Small human study (54 items, 5 annotators).

## Method
- **MMPCBench** with two sub-benchmarks: Content Quality Completion (CQBench — cosine similarity, token overlap, BERTScore for text; PSNR, SSIM, MSE, CLIP score for images) and Recommendation (RecBench — multimodal recommenders such as VBPR using completed features).
- MLLMs: Qwen2.5-VL 7B/32B/72B and Gemma-3 4B/12B/27B, 4-bit quantised. Text→Image: MLLM writes a prompt rendered by Stable Diffusion 3.5 Large Turbo (fixed renderer).
- **GRPO** alignment via TRL with **LoRA rank 16**, group size 16, single H100.

## Results
- MLLMs capture high-level semantics but struggle with fine word- and pixel/patch-level alignment.
- Scale non-monotonic: Gemma-3 27B best for Image→Text (cosine 0.210, BERTScore 0.872; 4B 0.166); Qwen2.5-VL peaks at 7B (32B/72B ~10–15% lower). Text→Image best PSNR 8.52/SSIM 0.373 (Gemma-3 12B).
- Strong category effects (e.g. Video Games Image→Text cosine 0.341).
- Completed modalities give recommendation performance close to ground truth; content quality correlates only weakly with recommendation accuracy.
- GRPO improves Image→Text but not Text→Image (e.g. SSIM 0.340 → 0.339, CLIP 0.723 unchanged).

## Limitations
Text→Image quality depends on the diffusion backbone; small human study; RecBench has limited sensitivity to fine-grained differences; only two model families.

## Transferable ideas for the FYP pipeline
- **Data ingestion / fusion:** when a machine-DB fault record has no image (or an image lacks an operator note), use an MLLM to generate a textual description of the image (Image→Text) as a fill-in feature; avoid relying on generated images.
- **Model selection:** benchmark several sizes; a 7B VLM may beat larger siblings for the specific task, and 4-bit quantisation makes local deployment feasible.
- **Fine-tuning:** GRPO + LoRA (rank 16) on one GPU is a feasible recipe to align a VLM for describing cut-edge images, if a reward (e.g. BERTScore to expert descriptions) is defined.
- **Evaluation:** evaluate both description quality and downstream utility (does the generated description improve diagnosis accuracy?), since they can diverge.
