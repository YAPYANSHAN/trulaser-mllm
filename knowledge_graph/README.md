# Example data: event-centric multimodal knowledge graph

This folder lets you try the working principle in your research plan (section "Event-centric multimodal knowledge graph") before you have real TruLaser data. **Everything here is made up.** It imitates three weeks of one laser cutter so the graph has something to find.

## What is in it

| File | What it holds | Rows |
|---|---|---|
| `csv/events.csv` | Every event in time order: jobs, inspections, alarms, maintenance | 494 |
| `csv/jobs.csv` | Parameters of each job (material, thickness, power, speed, gas pressure, bevel angle, jobs since nozzle change) | 240 |
| `csv/photos.csv` | One photo per job: file, what the image model said, confidence, and a 64-number embedding for similarity search | 240 |
| `csv/videos.csv` | One process video per job: file, what the video model said, and the unusual signal it saw | 240 |
| `csv/knowledge.csv` | Manual facts: defect → caused by → cause, cause → fixed by → remedy, with the manual section as source | 25 |
| `csv/alarm_causes.csv`, `csv/component_causes.csv` | Which alarm code points to which cause, and which machine part can cause it | 3 + 4 |
| `media/photos`, `media/videos` | The photo and video files themselves (synthetic) | 240 + 240 |
| `load_graph.cypher` | Builds the graph in Neo4j | |
| `example_questions.cypher` | Six questions to ask the graph | |
| `make_example_data.py` | The script that made all of this, if you want to change the story. It needs the pipeline demo data, so run `python pipeline/run_pipeline.py` once first | |

## The story hidden in the data

The graph should let you discover these four things:

1. **Nozzle wear.** Dross and rough cuts rise from 13% of jobs just after a nozzle change to 65% after 60–70 jobs, and drop again after each replacement.
2. **Gas supply fault.** On 5 Sep the gas pressure drops, eight E_GAS alarms fire and dross appears, until the regulator is repaired on 8 Sep.
3. **Dirty protective glass.** From 11 Sep incomplete cuts appear until the glass is cleaned on 12 Sep.
4. **Head collision.** An E_AXIS alarm on 16 Sep is followed by bevel deviations until the bevel axis is recalibrated on 18 Sep.

## How to try it in Neo4j (about 20 minutes)

1. Download and install **Neo4j Desktop** (free) from neo4j.com/download.
2. Create a new project, then **Add → Local DBMS**, give it a password, and start it. Use version 5.13 or newer.
3. Click the **⋯** next to the database → **Open folder → Import**. Copy every file from `csv/` into that folder.
4. Click **Open** to start Neo4j Browser. Paste the whole of `load_graph.cypher` into the box at the top and press the run button. It takes a few seconds.
5. Run `MATCH (n) RETURN labels(n), count(*)` to check. You should see about 240 Job, 240 Inspection, 240 Photo, 240 VideoClip, 9 Alarm and 5 Maintenance nodes, plus the knowledge nodes.
6. Paste the questions from `example_questions.cypher` one at a time. Q1 and Q4 draw pictures you can drag around.

## What each question shows (the "functions" of the MMKG)

| Question | Function from the plan |
|---|---|
| Q1 One dross case with its photo, video, causes and fixes | Linking all data types around one event |
| Q2 Alarms in the 2 hours before each dross inspection | Root-cause tracing (finds the E_GAS → low gas pressure link for 11 of the 44 dross cases) |
| Q3 Defect rate by jobs since the nozzle change | Using maintenance history to explain defects |
| Q4 The six events before the first bevel deviation | Seeing the event chain (collision alarm → bad jobs) |
| Q5 The five most similar past photos | Multimodal similar-case retrieval |
| Q6 The evidence pack for one job | What graph RAG would hand to the LLM |

## Limits to know about

- The photo "embedding" is just the photo shrunk to 8×8 grey values. It finds photos of the same defect 76% of the time, but only 16% for rough striations. The real pipeline should use the image model's features.
- The model labels in `photos.csv` and `videos.csv` are simulated, not produced by the trained models.
- The Cypher files were checked by reading them and against the data in Python, but could not be run in a real Neo4j here. If a line gives an error, paste the message in the thread.
