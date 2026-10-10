# trulaser-mllm

Final Year Project (NTU MAE, 2026/2027): **Smart Fault Detection and Process Optimisation with Multimodal LLM** for the TRUMPF TruLaser 3000 Bevel Cut Edition.

The project builds a pipeline in which small trained models detect cut defects from machine data, photos and process videos. An event-centric multimodal knowledge graph links what happened on the machine to what the manuals say, and a local LLM writes an evidence-cited diagnosis report.

The full research plan, with 49 cited papers, is an online document: [FYP Research Plan](https://claude.ai/code/artifact/37a2aff2-24ac-4253-b6e5-ca5c7ae74a4d).

## Folders

| Folder | What is in it | Start with |
|---|---|---|
| [`pipeline/`](pipeline/) | Python/PyTorch pipeline: table, image and video models, fusion with an "unknown" option, knowledge-graph lookup, manual retrieval, optimiser and LLM report (offline rules or Ollama) | [`pipeline/README.md`](pipeline/README.md) |
| [`knowledge_graph/`](knowledge_graph/) | Example event-centric multimodal knowledge graph: three weeks of made-up machine history (events, photos, videos, manual facts) and Neo4j scripts to load and query it | [`knowledge_graph/README.md`](knowledge_graph/README.md) |

## Quick start

```bash
# pipeline on synthetic data (Windows: use Anaconda Prompt)
conda create -n fyp python=3.11 -y
conda activate fyp
pip install -r pipeline/requirements.txt
python pipeline/run_pipeline.py
```

For the knowledge graph, follow the Neo4j steps in [`knowledge_graph/README.md`](knowledge_graph/README.md).

## Data

All data in this repository is **synthetic**. Real TruLaser exports, photos, videos and TRUMPF manuals must not be committed, because this repository is public. Keep them in a local `data/` folder, which is ignored by git.

The pipeline creates its own demo data (`pipeline/demo_data/`, about 40 MB) on the first run, so it is not stored here either.

## Not included

- Literature: paper PDFs, full texts and the reading notes are kept outside this repository.
