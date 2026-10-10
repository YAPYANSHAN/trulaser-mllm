# How the code in your repo works (plain-language guide)

You do not need to read the code to understand the project. This guide explains **what each file is for**, then follows **one part (job J0071) through the code** step by step.

---

## 1. The big idea in one picture

```
   ┌──────────── pipeline/ ────────────┐        ┌──────── knowledge_graph/ ────────┐
   │  the "eyes and brain"             │        │  the "memory"                    │
   │  trained models look at ONE part  │        │  the factory's history: alarms,  │
   │  and decide what is wrong with it │        │  repairs, past parts, manual     │
   └────────────────┬──────────────────┘        └───────────────┬──────────────────┘
                    │                                           │
                    └──────────► diagnose_from_graph.py ◄───────┘
                                 joins the two and writes
                                 the diagnosis report
```

There are **two folders** and **one script that connects them**:

- `pipeline/` looks at one part and says what is wrong (*what*).
- `knowledge_graph/` remembers everything that happened around that part (*why*).
- `diagnose_from_graph.py` asks both and writes the report.

---

## 2. What each file does

### The `pipeline/` folder: looking at one part

Think of a production line with stations. Each file is one station.

| File | Station | What it does, in plain words |
|---|---|---|
| `run_pipeline.py` | **Start button** | Runs everything on the pipeline's own practice data: trains the models, tests them and writes `outputs/evaluation.md` |
| `fyp_pipeline/pipeline.py` | **Manager** | Calls every other station in the right order. Its `diagnose()` function handles one part from start to finish |
| `fyp_pipeline/schema.py` | **Rule book** | Lists the column names, the 6 possible results (ok, dross…) and the only actions the report may recommend. **This is the first file to edit when your real data arrives** |
| `fyp_pipeline/synthetic.py` | **Practice data maker** | Makes 1,500 fake parts, with photos and videos, so the code can run before you have real data |
| `fyp_pipeline/ingest.py` | **Receiving desk** | Opens the files (CSV/Excel table, photos, PDF manuals) and checks that nothing is missing |
| `fyp_pipeline/tabular_model.py` | **Model 1: numbers** | Learns from the settings table (power, speed, gas pressure…) which settings lead to which defect |
| `fyp_pipeline/vision_model.py` | **Model 2: photo** | A small neural network (CNN) that looks at the photo of the cut edge and names the defect |
| `fyp_pipeline/video.py` | **Model 3: video** | Watches the cutting video in short clips (CNN + GRU) and notes anything unusual, such as "sparks fall below the cut" |
| `fyp_pipeline/fusion.py` | **Judge** | Combines the 3 models' votes. It trusts the more confident ones more. If they disagree too much it answers **"unknown"** instead of guessing |
| `fyp_pipeline/evidence.py` | **Measuring tape** | Compares each setting with the normal value for that material and thickness and says LOW, NORMAL or HIGH. Example: "gas pressure is LOW" |
| `fyp_pipeline/knowledge.py` | **Library** | Looks up the defect in the manual's defect → cause → fix list (`knowledge_base/laser_kg.json`) and searches the manual text |
| `fyp_pipeline/optimiser.py` | **Tuner** | Suggests better settings, such as "raise gas pressure from 8.25 to 10.71 bar" |
| `fyp_pipeline/reasoner.py` | **Report form** | Collects all the evidence into one packet, gives every piece an id (E1, D1, G1…), and checks the finished report follows the rules |
| `fyp_pipeline/llm.py` | **Writer** | Writes the report. `offline` uses simple rules with no AI, `ollama` uses a real local LLM such as Qwen |
| `fyp_pipeline/evaluate.py` | **Exam marker** | Scores the models: accuracy, how often they answer "unknown", whether the reports follow the rules |

### The `knowledge_graph/` folder: the factory's memory

| File | What it does |
|---|---|
| `csv/*.csv` | The made-up factory history (see `CSV_GUIDE.md`) |
| `media/` | The photo and video of every part |
| `make_example_data.py` | The script that **made** the CSV files and media. You don't need to run it again |
| `load_graph.cypher` | Instructions that tell Neo4j how to **build the graph** from the CSV files |
| `example_questions.cypher` | 6 example **questions** to ask the graph in Neo4j (Q1–Q6) |
| `diagnose_from_graph.py` | **The connector.** Takes a part from the graph, runs the pipeline on it, adds facts from the graph and writes the report |
| `CSV_GUIDE.md` | What every CSV column means |

---

## 3. Following job J0071 through the code

This is exactly what happens when you run `python diagnose_from_graph.py`, using the real output for J0071.

### Step 0: Train the models (first run only)

`diagnose_from_graph.py` → `train_or_load()`

The 3 models have to learn before they can judge. They study the 1,500 practice parts from `synthetic.py`, which takes a few minutes. The trained models are saved to `outputs/pipeline.pkl`, so later runs skip this step.

> Like a new inspector studying 1,500 old inspection reports before starting work.

### Step 1: Fetch the part from the graph

`diagnose_from_graph.py` → `graph.jobs()` and `to_pipeline_row()`

The script gets J0071's settings from Neo4j (or from `jobs.csv` if you didn't give a password): 12 mm stainless steel, 4754 W, 1354 mm/min, gas pressure 8.25 bar. It also finds J0071's photo and video in `media/`.

### Step 2: Detect, where the 3 models vote

`pipeline.py` → `diagnose()` → `probas()` → `fusion.py`

| Model | Its answer | How much the judge trusted it |
|---|---|---|
| Table model (settings) | dross | 20% |
| Image model (photo) | dross | 39% |
| Video model (video) | dross | 40% |

The judge combines the votes: **dross, 95% confident**, and the models agree (conflict only 0.14). Because confidence is high, the answer is not "unknown".

### Step 3: Retrieve, part A: what the pipeline itself can find

`evidence.py`, `knowledge.py`, `optimiser.py`

- The measuring tape says **gas pressure is LOW**: 8.25 bar, where stainless normally uses about 15.
- The library says dross can be caused by low gas pressure, high speed, wrong focus or a worn nozzle.
- The tuner suggests raising gas pressure from 8.25 to 10.71 bar.

These become evidence **E1, E2…** and manual excerpts **D1, D2**.

### Step 4: Retrieve, part B: what the graph adds

`diagnose_from_graph.py` → `graph_evidence()`

The script asks the graph 4 questions about J0071 and turns each answer into evidence **G1, G2…**:

| Question to the graph | Answer for J0071 | Evidence |
|---|---|---|
| Any alarms or repairs in the 3 days before? | Two E_GAS alarms at 10:28 and 10:51, and E_GAS points to low gas pressure | G1, G2 |
| How worn are the nozzle and glass? | The nozzle has cut 70 parts since it was replaced | G3, G4 |
| Has this defect happened recently? | 3 of the last 10 parts had dross | G5 |
| What did similar-looking parts have? | The 5 most similar earlier photos all show dross | G6 |

Then `add_graph_to_packet()` **moves causes up the list** when the graph supports them. Low gas pressure gets support from G1 and G2, and worn nozzle gets support from G3.

### Step 5: Explain, where the report is written

`reasoner.py` → `reason()` → `llm.py`

All the evidence goes to the writer, offline rules or a real LLM. It must follow the rules in `reasoner.py`:
- keep the judge's decision (dross) and not change it;
- give the evidence ids behind every cause;
- recommend only actions from the list in `schema.py`.

The report for J0071:

```
Diagnosis:  dross
Causes:     low_gas_pressure   (evidence E2, E5, G1, G2)   high confidence
            worn_nozzle        (evidence E3, G3)           high confidence
Actions:    adjust_gas_pressure, inspect_or_replace_nozzle
Settings:   gas pressure 8.25 → 10.71 bar
```

`validate_report()` then checks the report. If it cites evidence that doesn't exist, or recommends an action that isn't allowed, the writer is asked to fix it.

### Step 6: Learn (only with `--write-back`)

`diagnose_from_graph.py` → `write_back()`

The report is saved in Neo4j as a new `Diagnosis` node, linked to J0071's inspection, the causes it blames and the alarms it used. Next time, the graph also knows this diagnosis.

### Step 7: The summary

The script writes `outputs/summary.md`. It compares, for each part, the top cause found **by the pipeline alone** with the top cause found **with the graph**. This comparison is the evidence for your research question: *what does the knowledge graph add?*

---

## 4. Which files you will actually touch

| When | File |
|---|---|
| Real data arrives: rename columns, set your defect names | `pipeline/fyp_pipeline/schema.py` |
| Real manual facts | `pipeline/knowledge_base/laser_kg.json` and `knowledge_graph/csv/knowledge.csv` |
| Use a real LLM instead of rules | add `--llm ollama --model qwen2.5:7b-instruct` when you run it |
| Look at results | `knowledge_graph/outputs/summary.md` and `outputs/reports/J0071.json` |

Everything else can stay as it is.
