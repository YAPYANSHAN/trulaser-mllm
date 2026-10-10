# Technical architecture for integrating vision-language models with DICOM viewers

- **Citation (IEEE):** M. Albera, A. Colarieti, I. Albera, et al., "Technical architecture for integrating vision-language models with DICOM viewers," *European Radiology Experimental*, vol. 10, Art. no. 103, 2026, doi: 10.1186/s41747-026-00769-0.
- **Domain:** Medical imaging software / VLM workflow integration (radiology)
- **Relevance to FYP (1-5):** 3 - medical domain, but its system-engineering pattern is directly reusable for the FYP front end: reproducible, context-preserving evidence capture, staging before VLM submission, a provider-agnostic model adapter and auditability.

## Problem
To use VLMs in radiology, 2D images must be exported with their full viewing context (plane, slice, window/level, slab, overlays). Ad hoc screenshots and uploads lose this context, are not reproducible and force radiologists to switch applications.

## Data & modalities
Volumetric DICOM imaging (benchmarks used one MRI series). Outputs are 2D rendered frames (1000×1000 px, HEIC) plus text chat with the VLM.

## Method (architecture: encoders, fusion, LLM/VLM used, RAG/KG, fine-tuning e.g. LoRA, prompting)
- Split workspace: a diagnostic grid plus an assistant sidebar for evidence staging and chat.
- Capture does not screenshot. It serialises the viewer state (series, plane, slice, window/level, slab, camera, overlay policy) into replayable descriptors.
- A cloned offscreen viewer (VTK/OpenGL) re-renders the queued states from a shared in-memory voxel cache. Frames stream back for the user to curate before submission.
- Batch capture builds multi-slice, multi-plane and multi-series evidence.
- A thin provider-specific adapter layer packages images and parses responses, so the VLM provider is swappable.
- The serialised states give an auditable record of exactly what the model saw.
- No model is trained. The paper is an architecture and performance benchmark.

## Results (key numbers and metrics)
- Perfect reproducibility: identical states gave pixel-identical images, with 0 hash mismatches across 50 frames.
- Median capture latency 4.49-16.69 ms per frame depending on view type (hot cache).
- Median output size 27.9 kB per frame. HEIC is about 2.8× smaller than JPEG.

## Limitations
- Single device, hot cache, one MRI series and one logged run. Cold-cache and networked latency were not measured.
- The memory footprint of the shared voxel cache grows with many large studies.
- No clinical evaluation of VLM diagnostic accuracy.
- Deployments must keep identifiers out of exported pixels and filenames.

## Transferable ideas for the FYP pipeline
- **Data ingestion / deployment:** store the context of each evidence item with the image, not just the pixels: machine ID, job/program number, material/thickness, parameter set, timestamp, camera and lighting settings. Then any diagnosis can be reproduced and audited.
- **UI / deployment:** a split UI (data dashboard + chat sidebar) in which the engineer curates which images, tables and log rows are sent to the MLLM before submission. This keeps the human in the loop and reduces irrelevant context.
- **Deployment:** a thin adapter layer that isolates the LLM/VLM provider (local Qwen-VL vs. a cloud API) makes model comparison and swapping easy.
- **Evaluation:** benchmark the pipeline itself (capture latency, payload size, reproducibility via hashes) as well as model accuracy.
- **Deployment:** strip sensitive identifiers (customer or part names) before images leave the machine.
