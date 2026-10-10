# Cloud-Edge Collaborative Interpretable Fault Classification for Helical Tomotherapy Systems via LLM-VLM Reasoning

- **Citation (IEEE):** H. Yang, J. Guo, Y. Wang, et al., "Cloud-edge collaborative interpretable fault classification for helical tomotherapy systems via LLM-VLM reasoning," *Journal of Cloud Computing*, vol. 15, art. 99, 2026, doi: 10.1186/s13677-026-00921-6.
- **Domain:** Equipment fault diagnosis (medical radiotherapy machines) + industrial defect classification; LLM/VLM retrieval-driven reasoning
- **Relevance to FYP (1-5):** 5 - interpretable image-based equipment fault classification using LLM-generated fault descriptors, retrieval and LoRA-distilled VLM/LLM reasoning, validated also on MVTec AD and NEU-CLS (steel surface defects); closest blueprint in this batch for the FYP's image + reasoning stage.

## Problem
Helical tomotherapy system (HTS) faults vary in severity and need interpretable diagnosis. VLMs (CLIP, prompt learning) rely on direct image-to-category-name matching: poor on rare/fine-grained faults, no intermediate reasoning, too heavy for edge devices.

## Data & modalities
HTS-10K: 10,000 annotated fault images built from the institution's 2023-2025 adverse-event records, 7 categories (Surface Damage, Deformation, Material Loss, Contamination, Texture Anomaly, Intensity Abnormality, Structural Breakage). Public benchmarks: MVTec AD and NEU-CLS. Modalities: images + LLM-generated text descriptors (visual and contextual).

## Method
RdR-Med (Retrieval-driven Reasoning), cloud-edge split: edge does lightweight CLIP-style visual feature extraction; cloud does retrieval and reasoning. Step 1: offline, GPT-4o (temperature 0) generates structured visual and contextual descriptors per fault category, filtered by CLIP image-text similarity, stored as a retrieval database; at inference, top-K=2 descriptors of each type retrieved by image-descriptor similarity. Step 2: descriptor deliberation - a LoRA-SFT LLaVA-v1.6-Mistral-7B student refines descriptors against the image. Step 3: deliberative prediction - a LoRA-SFT Llama3-8B produces an explicit reasoning chain and the category from the refined descriptors, category set and instruction prompt. Teacher-student distillation from GPT-4o with generate-then-filter (CLIP grounding, consistency) to curb hallucination.

## Results
Accuracy (ViT-B/16 backbone): HTS-10K 82.05% vs CLIP 65.05, CoOp 72.92, PromptKD 74.60, CBD 70.03; MVTec AD 92.96% (95.45% with RN-50); NEU-CLS 90.03%. Consistent gains across ViT-B/16, ViT-B/32 and ResNet-50. K=2 better than K=1 (82.05 vs 78.52 on HTS-10K). Removing deliberation or reasoning lowers accuracy on all three datasets. End-to-end latency 16.1 ms/image vs CLIP 10.2 ms and CoOp 11.8 ms.

## Limitations
Descriptor database must be built per dataset/domain; dependence on GPT-4o as descriptor generator and teacher (cost, proprietary); multi-stage pipeline adds latency and complexity; dataset not public; classification only (no root-cause or parameter recommendations).

## Transferable ideas for the FYP pipeline
- **Text/RAG + vision:** have an LLM write visual and contextual descriptors for each TruLaser defect class (e.g. dross "irregular droplets adhering to bottom edge", burr, excessive striations, bevel-angle deviation, burn-out), filter them with CLIP, and retrieve image-descriptor matches instead of image-to-label matching.
- **LLM reasoning:** a two-step student pipeline (VLM refines evidence, LLM reasons to a decision) distilled from a frontier teacher with LoRA - practical for local deployment.
- **Fusion:** extend "contextual descriptors" with machine-database evidence (parameters, alarms) and manual excerpts.
- **Evaluation:** compare against zero-shot CLIP, CoOp and supervised CNN/ViT baselines; report ablations without deliberation/reasoning and latency.
- **Deployment:** edge perception at the machine, cloud reasoning - mirrors a factory set-up.
