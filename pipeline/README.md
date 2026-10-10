# FYP pipeline: multimodal LLM fault diagnosis for the TruLaser 3000

This code is the working version of the research plan. It takes four kinds of data for a laser-cutting job, the machine-database row, a photo of the cut edge, a video of the cutting process and the technical manuals, and produces a diagnosis report. The report says which defect is present, its likely causes with the evidence for each, the recommended actions and any suggested parameter changes.

It runs today on **synthetic** data that imitates TruLaser jobs, so you can learn how it works before the real data arrives. Every place you need to swap in real data is marked `PLACEHOLDER` or explained below.

## 1. Quick start (Windows, Anaconda Prompt)

```bash
cd path\to\pipeline
conda create -n fyp python=3.11 -y
conda activate fyp
pip install -r requirements.txt
python run_pipeline.py
```

The first run creates `demo_data/` (1,500 fake jobs, each with a photo and a short process video), trains everything on CPU in about four minutes, and writes `outputs/evaluation.md` plus one JSON report per diagnosed job in `outputs/reports/`.

To use a real language model instead of the offline rule-based writer, install [Ollama](https://ollama.com), which you already have, then:

```bash
ollama pull qwen2.5vl:7b
python run_pipeline.py --llm ollama --model qwen2.5vl:7b --image-to-llm
```

## 2. How the pipeline works

```
 machine table ─┐                              ┌─ knowledge graph (defect→cause→parameter→remedy)
 cut-edge photo ┼─► specialist models ──────► fusion ─► evidence packet ─► LLM report (validated JSON)
 process video ─┤   (table GBT, image CNN,     │                              ▲
 manuals ───────┘    video CNN-GRU)            └─ "unknown" if unsure          └─ optimiser suggests parameters
```

| Stage | File | What it does | Main papers it follows |
|---|---|---|---|
| 1 Ingest | `fyp_pipeline/ingest.py` | Loads CSV/Excel/SQLite, checks columns, turns a row into text, loads photos, splits manuals into cited chunks | Wang et al. 2026 (row serialisation); Chen et al. 2026 (image preprocessing) |
| 2a Table model | `tabular_model.py` | Gradient-boosted trees predict the defect from parameters; a surrogate predicts dross height and roughness | Nguyen et al. 2026 review; Bhoir & Verma 2026; Rao & Vaneesha 2026 |
| 2b Image model | `vision_model.py` | PyTorch CNN classifies the cut-edge photo and says which region it looked at | Kukuljan et al. 2026, Haupt et al. 2026, Abdelkader 2026 (why not rely on zero-shot VLMs) |
| 2c Video model | `video.py` | Samples the video into 16-frame clips, a CNN reads each frame and a GRU reads the sequence, clip results are averaged. It also measures brightness, glow size and glow position over short windows and reports only what differs from normal cuts | Liu W. et al. 2026 (clips at 8 FPS, aggregation); Guerra et al. 2026 and Asadi et al. 2026 (process-camera features); Costamagna et al. 2026 (motion tracking); Ding et al. 2026 (deviation from a normal baseline); Patel et al. 2026 (why not zero-shot video LLMs) |
| 3 Knowledge | `evidence.py`, `knowledge.py`, `knowledge_base/laser_kg.json` | Marks parameters as low/normal/high versus the cutting table, finds matching cause paths in the knowledge graph, retrieves manual text (BM25) | Li et al. 2026 (GAT-RAG); Zhang et al. 2026 (LLM-KGSO); Hou et al. 2026 (KE-CausalLLM) |
| 4 Fusion | `fusion.py` | Calibrates each model (table, image, video), weights them by confidence, measures disagreement, says "unknown" when unsure | Shi, Gao & Liu 2026 |
| 5 LLM report | `reasoner.py`, `llm.py` | Four-step reasoning prompt, fixed JSON schema, every claim must cite evidence ids, whitelist of actions, automatic retry if the output breaks a rule | Yang et al. 2026 (4-stage CoT); Shi et al. 2026; Zhang et al. 2026 (vineyard JSON) |
| 6 Optimiser | `optimiser.py` | Searches for better parameters with the surrogate, only in the directions the knowledge graph allows | Guerra et al. 2026; Bhoir & Verma 2026 |
| 7 Evaluation | `evaluate.py`, `run_pipeline.py` | Accuracy, macro-F1, calibration (ECE), coverage of "unknown", modality ablation, report validity and evidence citation rates | Several; see the research plan |

Full citations are in the research plan document.

## 3. Results on the synthetic demo

From `outputs/evaluation.md` (225 test jobs, random split):

| Model | Accuracy | Macro-F1 |
|---|---|---|
| Table model only | 0.66 | 0.39 |
| Image model only | 0.96 | 0.91 |
| Video model only | 0.85 | 0.83 |
| Table + image, conflict-aware fusion | 0.96 | 0.91 |
| Simple average of all three | 0.93 | 0.86 |
| **Conflict-aware fusion of all three** | **0.97** | **0.92** |

With the "unknown" option on, the system answers 79% of jobs and is 98% accurate on those. Run with `--no-video` to compare against table + image only. All five sample reports passed the schema and rule checks. These numbers only show the code works. The synthetic data is made up, so do not quote them as research results.

## 4. Plugging in your real data

1. **Machine table.** Export the TruLaser job records to CSV or Excel. Rename columns in `fyp_pipeline/schema.py` (`MACHINE_COLUMNS`) to match, or rename your columns to match. Add a `defect` column (the label your engineers gave), `dross_height_mm` and `roughness_ra_um` if measured, and `image_path` for the photo of that part.
2. **Defect classes.** Edit `DEFECT_CLASSES` in `schema.py` to the categories you actually record.
3. **Photos.** Use a fixed camera position and lighting (Chen et al. 2026). Switch the image model to the pretrained ResNet-18 for real photos by passing `backbone="resnet18"` in `FaultDiagnosisPipeline`.
4. **Videos.** Add a `video_path` column pointing to one video per job (any format OpenCV reads). Keep the camera fixed and the exposure constant, because video models are sensitive to framing and lighting (Patel et al. 2026 saw accuracy fall to about zero on dark videos). If one video covers many parts, cut it per part first. Change `CLIP_FRAMES` and `FRAME_SIZE` at the top of `video.py` to suit your camera. If some jobs have no video, either drop those rows or run with `--no-video`.
5. **Manuals.** Put TRUMPF manuals and troubleshooting tables (PDF, .md or .txt) in a folder and pass `--docs that_folder`.
6. **Knowledge graph.** Replace the placeholder triples in `knowledge_base/laser_kg.json` with ones from the manuals and your engineers. An LLM can draft them, as in Zhang et al. 2026 and the waste-to-resource KG paper, but have an engineer check them.
7. Run `python run_pipeline.py --data your_export.csv --docs your_manuals --split leave_material_out` to also test on a material the models never saw.

## 5. Ideas for extending it (good FYP chapters)

- Fine-tune an open vision-language model (Qwen2.5-VL-7B or LLaVA) with LoRA on your photos paired with expert descriptions (SAM-LLaVA, Pattern Recognition 2026; heritage-augmentation paper, 2026).
- Add a YOLO or SAM defect localiser in front of the image model, so the report can give the defect position and size.
- For real videos, replace the small frame CNN in `video.py` with a pretrained encoder (ResNet-18, or a video model such as VideoMAE) and train only the GRU and head, as the ADOS paper did with a frozen encoder and adapter (Liu W. et al. 2026).
- Feed short video summaries or key frames to a video-capable LLM (Qwen2.5-VL accepts video) and compare it against the trained video model, to test on laser cutting the finding of Patel et al. 2026 that zero-shot video LLMs are unreliable.
- Replace BM25 with BM25 plus embeddings (hybrid retrieval) and multi-hop graph search.
- Let the LLM query the machine database with Text-to-SQL (Su et al. 2026; MTC-SQL 2026).
- Replace random search with NSGA-II (`pip install pymoo`) for a full Pareto front of quality vs speed.
