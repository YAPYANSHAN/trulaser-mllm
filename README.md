# trulaser-mllm

Final Year Project (NTU MAE, 2026/2027): **Smart Fault Detection and Process Optimisation with Multimodal LLM** for the TRUMPF TruLaser 3000 Bevel Cut Edition.

The aim is a tool that looks at a laser-cutting job and explains what went wrong, why, and what to change. It combines machine records, logs, photos, process videos and documents in an event-centric multimodal knowledge graph, and a local LLM writes a report with evidence.

## Where things are

| Folder | What is in it |
|---|---|
| [`datasets/`](datasets/) | The data handed over by the production team. Read [`datasets/README.md`](datasets/README.md) first. |
| [`docs/`](docs/) | Notes for working on this project, starting with [GitHub basics](docs/GITHUB_BASICS.md). |

The project starts from the data only. Code is added step by step as the work goes on.

## Plan of work

1. **Explore the data.** Open each file, count rows, look at photos and clips, and write down what is missing or messy.
2. **Clean and link.** Fix decimal commas and date formats, match inspection rows to jobs, and give every alarm and maintenance entry a place on the timeline.
3. **Build the event timeline.** Put jobs, alarms, maintenance and inspections in one time-ordered list. This becomes the event layer of the knowledge graph.
4. **Detect defects.** Train simple models on the job table, photos and videos, and check how well each works alone and together.
5. **Build the knowledge graph.** Turn the troubleshooting guide into cause and remedy facts, and link them to the events, photos and clips in Neo4j.
6. **Retrieve and explain.** For a new job, pull the relevant part of the graph and let a local LLM write a cited diagnosis.
7. **Evaluate.** Compare against simpler versions, such as the LLM alone or the guide text alone.

The full research plan is an online document: [FYP Research Plan](https://claude.ai/code/artifact/37a2aff2-24ac-4253-b6e5-ca5c7ae74a4d).

## Data rules

The data in `datasets/` is synthetic. Real company exports, photos, videos and manuals must never be committed, because this repository is public. Keep them in a local `data/` folder, which git ignores (see [`.gitignore`](.gitignore)).
