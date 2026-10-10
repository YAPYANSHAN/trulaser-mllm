# Example data: event-centric multimodal knowledge graph

This folder lets you try the working principle in your research plan (section "Event-centric multimodal knowledge graph") before you have real TruLaser data. **Everything here is made up.** It imitates three weeks of one laser cutter so the graph has something to find.

## What is in it

| File | What it holds | Rows |
|---|---|---|
| `CSV_GUIDE.md` | Plain-language guide to every CSV file, following one job through all of them | |
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
| `diagnose_from_graph.py` | Runs the pipeline on jobs from this graph and adds graph evidence to the report (see "Run the pipeline on the graph") | |

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

## Run the pipeline on the graph

`diagnose_from_graph.py` joins the two halves of the project. For a job in the graph:

1. **Detect.** The pipeline's table, image and video models decide the defect from the job's settings, photo and video.
2. **Retrieve.** The script asks the graph what a single table row cannot show: alarms and maintenance in the 3 days before, how many jobs the nozzle and protective glass have done, how often the same defect appeared in the last 10 inspections, and the most similar earlier photos. Each fact becomes a piece of evidence with an id (G1, G2 …), and causes the graph supports move up the ranking.
3. **Explain.** The report writer (offline rules, or a local LLM through Ollama) cites those ids.
4. **Learn (optional).** With `--write-back`, each diagnosis is saved in Neo4j as a `Diagnosis` node linked to the inspection, the causes it blames and the events it used.

By default it diagnoses one job for each problem in the story and writes `outputs/summary.md`, which compares the top cause found by the pipeline alone with the top cause found with the graph.

```bash
conda activate fyp
pip install -r ../pipeline/requirements.txt
cd knowledge_graph
python diagnose_from_graph.py                                  # reads the graph from csv/, no Neo4j needed
python diagnose_from_graph.py --password YOUR_NEO4J_PASSWORD   # reads it from Neo4j (database must be running)
python diagnose_from_graph.py --password YOUR_NEO4J_PASSWORD --write-back
python diagnose_from_graph.py --jobs J0072 J0150 --llm ollama --model qwen2.5:7b-instruct
```

The first run trains the pipeline on its own synthetic demo data, which takes a few minutes on a laptop CPU, and saves it as `outputs/pipeline.pkl`. Delete that file to retrain.

After `--write-back`, run `MATCH p=(d:Diagnosis)-[]->() RETURN p` in Neo4j to see the stored diagnoses.

What it showed on the example data (CSV mode, offline rules):

| Job | Problem in the story | Pipeline decision | Top cause, pipeline alone | Top cause, with the graph |
|---|---|---|---|---|
| J0071 | gas fault | dross | low gas pressure | low gas pressure |
| J0133 | dirty protective glass | unknown (models disagree) | dirty protective glass | dirty protective glass |
| J0184 | head collision | bevel deviation | bevel axis drift | bevel axis drift |
| J0062 | worn nozzle | unknown (models disagree) | none | worn nozzle |

The graph added evidence to every report, and found the cause for J0062 that the pipeline alone missed. In the other three, the job's own row already pointed to the cause, so this made-up data is too easy to show a big difference. Real data, where a row rarely tells the whole story, is the real test.

## Limits to know about

- The photo "embedding" is just the photo shrunk to 8×8 grey values. It finds photos of the same defect 76% of the time, but only 16% for rough striations. The real pipeline should use the image model's features.
- The model labels in `photos.csv` and `videos.csv` are simulated, not produced by the trained models.
- The graph table has fewer columns than the pipeline expects, so `diagnose_from_graph.py` fills focus, standoff and assist gas from the made-up cutting table, and counts 1.6 hours per job for nozzle and glass wear.
- The photos and videos in the graph are copies of the pipeline's demo data, which the models were also trained on, so the model decisions here look better than they would on new data.
- The Cypher files were checked by reading them and against the data in Python, but could not be run in a real Neo4j here. If a line gives an error, paste the message in the thread.
