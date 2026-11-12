# trulaser-mllm

Final Year Project (NTU MAE, 2026/2027): **Smart Fault Detection and Process Optimisation with Multimodal LLM** for the TRUMPF TruLaser 3000 Bevel Cut Edition.

The aim is a tool that looks at a laser-cutting job and explains what went wrong, why, and what to change. It combines machine records, logs, photos, process videos and documents in an event-centric multimodal knowledge graph, and a local LLM writes a report with evidence.

## Where things are

| Folder | What is in it |
|---|---|
| [`datasets/`](datasets/) | The data handed over by the production team. Read [`datasets/README.md`](datasets/README.md) first. |
| [`notebooks/`](notebooks/) | The pipeline, one notebook per step (table below). |
| [`neo4j/`](neo4j/) | Script that loads the knowledge graph into Neo4j, and example queries. |
| [`nscc/`](nscc/) | Job script and guide for running the LLM notebooks on an NSCC GPU (not yet tested there). |
| [`docs/`](docs/) | Notes for working on this project, starting with [GitHub basics](docs/GITHUB_BASICS.md). |
| `data/` | Not in git. Everything the notebooks create goes to `data/processed/`; real company data would go here too. |

## The notebooks

Run them in number order the first time. Each one reads what earlier ones saved in `data/processed/`.

| Notebook | What it does | Needs |
|---|---|---|
| 01 event timeline | Cleans the four log files and puts every event on one timeline | |
| 02 bunches and answer sheet | Finds the periods where one defect piles up, and records your cause for each bad job (the marking scheme) | 01 |
| 03 gradient boosting | Classical baseline: predict the defect from the job table | 01 |
| 04 knowledge graph | Builds the graph: knowledge layer (from the manual) and event layer (from the timeline) | 01 |
| 05 diagnose with LLM | For each bad job, walks the graph for evidence and asks the LLM for the cause | 02, 04, Ollama for the LLM modes |
| 06 evaluation | Scores the diagnoses against the answer sheet | 05 |
| 07 Neo4j | Same diagnosis asked to a Neo4j database, checked against notebook 05 | 04, 05, Neo4j running |
| 08 OWL ontology | The graph's rules as an OWL file, checked by a reasoner | 04, Java |
| 09 photo features | Cleans the edge photos, measures features, ablation | 01 |
| 10 logs + photos fusion | Random forest on logs, on photos, and three ways to blend them | 03, 09 |
| 11 manual to graph facts | Reads the 66-page manual and extracts the facts notebook 04 needs | Ollama for the LLM step |

Notebook 04 types the manual's facts in by hand by default. To build the graph from notebook 11's tables instead, run 11 first
and set `KNOWLEDGE = "llm"` in notebook 04.

Not built yet: photos and process videos are not in the graph (notebook 09 saves `photo_evidence.csv` for that step), and the
videos in `datasets/process_video/` are not used by any notebook.

## Running the notebooks

```
pip install -r requirements.txt
python run_all.py                 # runs notebooks/01 to 11 in order, saving outputs
python run_all.py 09 10           # only these
python run_all.py --skip 07 08    # skip the ones needing Neo4j (07) or Java (08)
```

Notebooks 05 and 11 run without Ollama too, but then they skip their LLM steps.

Two scoring files are kept out of the repo, like an exam's answer key. Copy them into `data/` to use them:
`manual_gold_facts.csv` (notebook 11, scores the extracted facts) and `ground_truth_jobs.csv` (notebook 06 step 4, optional).

## Plan of work

1. **Explore the data.** Open each file, count rows, look at photos and clips, and write down what is missing or messy.
2. **Clean and link.** Fix decimal commas and date formats, match inspection rows to jobs, and give every alarm and maintenance entry a place on the timeline.
3. **Build the event timeline.** Put jobs, alarms, maintenance and inspections in one time-ordered list. This becomes the event layer of the knowledge graph.
4. **Detect defects.** Train simple models on the job table, photos and videos, and check how well each works alone and together.
5. **Build the knowledge graph.** Turn the machine manual into cause and remedy facts, and link them to the events, photos and clips in Neo4j.
6. **Retrieve and explain.** For a new job, pull the relevant part of the graph and let a local LLM write a cited diagnosis.
7. **Evaluate.** Compare against simpler versions, such as the LLM alone or the manual text alone.

The full research plan is an online document: [FYP Research Plan](https://claude.ai/code/artifact/37a2aff2-24ac-4253-b6e5-ca5c7ae74a4d).

## Data rules

The data in `datasets/` is synthetic. Real company exports, photos, videos and manuals must never be committed, because this repository is public. Keep them in a local `data/` folder, which git ignores (see [`.gitignore`](.gitignore)).
