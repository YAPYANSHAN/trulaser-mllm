"""Run the FYP pipeline on jobs from the example knowledge graph (graph RAG).

This is the workflow from the research plan, end to end:
  1 Load     the example graph is already in Neo4j (load_graph.cypher)
  2 Detect   the pipeline's table, image and video models diagnose a job from the graph
  3 Retrieve the event graph adds what one table row cannot show: alarms and
             maintenance in the days before, how worn the nozzle and glass are,
             whether the defect keeps coming back, and similar past photos
  4 Explain  the LLM (offline rules or Ollama) writes the report, citing graph evidence (G ids)
  5 Learn    optionally write the diagnosis back into Neo4j as a Diagnosis node

Examples
  python diagnose_from_graph.py                        # read the graph from the CSV files, no Neo4j needed
  python diagnose_from_graph.py --password YOUR_PASS   # read the graph from Neo4j
  python diagnose_from_graph.py --password YOUR_PASS --write-back
  python diagnose_from_graph.py --jobs J0072 J0150 --llm ollama --model qwen2.5:7b-instruct

The first run trains the pipeline on its synthetic demo data (a few minutes on CPU)
and saves it in outputs/pipeline.pkl, so later runs start straight away.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PIPE = os.path.join(HERE, "..", "pipeline")
sys.path.insert(0, PIPE)

from fyp_pipeline.ingest import load_machine_table  # noqa: E402
from fyp_pipeline.llm import get_llm  # noqa: E402
from fyp_pipeline.pipeline import FaultDiagnosisPipeline  # noqa: E402
from fyp_pipeline.reasoner import reason  # noqa: E402
from fyp_pipeline.synthetic import nominal_recipe, write_demo_dataset  # noqa: E402

WINDOW_DAYS = 3          # how far back to look for alarms and maintenance
NOZZLE_WORN_AFTER = 50   # jobs since nozzle change counted as "worn"
GLASS_DIRTY_AFTER = 100  # jobs since glass cleaning counted as "dirty"


# --------------------------------------------------------------- 3 Retrieve: two ways to read the graph
class Neo4jGraph:
    """Reads the event graph from Neo4j with Cypher (the real set-up)."""

    def __init__(self, uri: str, user: str, password: str, database: str):
        from neo4j import GraphDatabase
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()
        self.database = database
        self.name = f"Neo4j ({uri})"

    def run(self, cypher: str, **params) -> list[dict]:
        records, _, _ = self.driver.execute_query(cypher, params, database_=self.database)
        return [r.data() for r in records]

    def jobs(self) -> pd.DataFrame:
        rows = self.run("""
            MATCH (i:Inspection)-[:OF_JOB]->(j:Job)
            OPTIONAL MATCH (a:Alarm)-[:DURING]->(j)
            WITH i, j, collect(a.code)[0] AS alarm
            RETURN j.job_id AS job_id, toString(j.timestamp) AS start, j.material AS material,
                   j.thickness_mm AS thickness_mm, j.laser_power_w AS laser_power_w,
                   j.cutting_speed_mm_min AS cutting_speed_mm_min, j.gas_pressure_bar AS gas_pressure_bar,
                   j.bevel_angle_deg AS bevel_angle_deg, j.nozzle_jobs_since_change AS nozzle_jobs_since_change,
                   j.glass_jobs_since_clean AS glass_jobs_since_clean, i.result AS defect,
                   coalesce(alarm, 'none') AS alarm_code
            ORDER BY job_id""")
        return pd.DataFrame(rows)

    def recent_events(self, job_id: str, days: int) -> list[dict]:
        return self.run("""
            MATCH (i:Inspection)-[:OF_JOB]->(:Job {job_id: $job})
            MATCH (e:Event) WHERE (e:Alarm OR e:Maintenance)
              AND e.timestamp <= i.timestamp AND e.timestamp >= i.timestamp - duration({days: $days})
            OPTIONAL MATCH (e)-[:INSTANCE_OF]->(:AlarmCode)-[:POINTS_TO]->(c:Cause)
            OPTIONAL MATCH (e)-[:ON_COMPONENT]->(:Component)-[:CAN_CAUSE]->(m:Cause)
            RETURN e.event_id AS event_id, toString(e.timestamp) AS time,
                   CASE WHEN e:Alarm THEN 'Alarm' ELSE 'Maintenance' END AS type,
                   e.code AS code, e.action AS action, c.name AS points_to, m.name AS repairs,
                   duration.inSeconds(e.timestamp, i.timestamp).minutes AS minutes_before
            ORDER BY e.timestamp""", job=job_id, days=days)

    def previous_results(self, job_id: str, n: int) -> list[str]:
        rows = self.run("""
            MATCH (i:Inspection)-[:OF_JOB]->(:Job {job_id: $job})
            MATCH (p:Inspection) WHERE p.timestamp < i.timestamp
            RETURN p.result AS result ORDER BY p.timestamp DESC LIMIT $n""", job=job_id, n=n)
        return [r["result"] for r in rows]

    def similar_cases(self, job_id: str, k: int) -> list[dict]:
        # only earlier jobs count: the system must not look into the future
        return self.run("""
            MATCH (i:Inspection)-[:OF_JOB]->(j:Job {job_id: $job})-[:CAPTURED]->(p:Photo)
            CALL db.index.vector.queryNodes('photo_embedding', 40, p.embedding) YIELD node, score
            MATCH (other:Job)-[:CAPTURED]->(node) WHERE node <> p
            MATCH (ins:Inspection)-[:OF_JOB]->(other) WHERE ins.timestamp < i.timestamp
            RETURN other.job_id AS job_id, ins.result AS result, score
            ORDER BY score DESC LIMIT $k""", job=job_id, k=k)

    def write_back(self, job_id: str, report: dict, decision: dict, cited_events: list[str]):
        """5 Learn: store the diagnosis as a node linked to the inspection, causes and events."""
        causes = [c["cause"] for c in report.get("root_causes", [])]
        self.run("""
            MATCH (i:Inspection)-[:OF_JOB]->(:Job {job_id: $job})
            MERGE (d:Diagnosis {job_id: $job})
            SET d.label = $label, d.confidence = $conf, d.causes = $causes,
                d.report = $report, d.created = datetime()
            MERGE (d)-[:EXPLAINS]->(i)""",
                 job=job_id, label=decision["label"], conf=float(decision["confidence"]), causes=causes,
                 report=json.dumps(report))
        if causes:
            self.run("""MATCH (d:Diagnosis {job_id: $job}) UNWIND $causes AS name
                        MATCH (c:Cause {name: name}) MERGE (d)-[:BLAMES]->(c)""", job=job_id, causes=causes)
        if cited_events:
            self.run("""MATCH (d:Diagnosis {job_id: $job}) UNWIND $ids AS id
                        MATCH (e:Event {event_id: id}) MERGE (d)-[:CITES]->(e)""", job=job_id, ids=cited_events)


class CsvGraph:
    """Answers the same questions straight from the CSV files, for trying it without Neo4j."""

    name = "CSV files (no Neo4j)"

    def __init__(self, folder: str):
        r = lambda f: pd.read_csv(os.path.join(folder, f))  # noqa: E731
        self.events = r("events.csv")
        self.events["timestamp"] = pd.to_datetime(self.events["timestamp"])
        self.photos = r("photos.csv").set_index("job_id")
        self.alarm_causes = dict(r("alarm_causes.csv").values)
        self.component_causes = dict(r("component_causes.csv").values)
        self.insp = self.events[self.events.type == "Inspection"].set_index("job_id")
        alarms = self.events[(self.events.type == "Alarm") & self.events.job_id.notna()]
        self._jobs = r("jobs.csv").merge(alarms.groupby("job_id").code.first().rename("alarm_code"),
                                         on="job_id", how="left").fillna({"alarm_code": "none"})

    def jobs(self) -> pd.DataFrame:
        return self._jobs.copy()

    def recent_events(self, job_id: str, days: int) -> list[dict]:
        t = self.insp.loc[job_id, "timestamp"]
        e = self.events[self.events.type.isin(["Alarm", "Maintenance"])
                        & (self.events.timestamp <= t) & (self.events.timestamp >= t - pd.Timedelta(days=days))]
        return [{"event_id": x.event_id, "time": x.timestamp.isoformat(), "type": x.type,
                 "code": x.code if isinstance(x.code, str) else None,
                 "action": x.action if isinstance(x.action, str) else None,
                 "points_to": self.alarm_causes.get(x.code), "repairs": self.component_causes.get(x.component),
                 "minutes_before": int((t - x.timestamp).total_seconds() // 60)} for x in e.itertuples()]

    def previous_results(self, job_id: str, n: int) -> list[str]:
        t = self.insp.loc[job_id, "timestamp"]
        return list(self.insp[self.insp.timestamp < t].sort_values("timestamp", ascending=False).result[:n])

    def similar_cases(self, job_id: str, k: int) -> list[dict]:
        emb = self.photos.embedding.map(lambda s: np.array([float(x) for x in s.split(";")]))
        q = emb[job_id]
        t = self.insp.loc[job_id, "timestamp"]
        out = []
        for other, v in emb.items():
            if other != job_id and self.insp.loc[other, "timestamp"] < t:
                cos = float(q @ v / (np.linalg.norm(q) * np.linalg.norm(v)))
                out.append({"job_id": other, "result": self.insp.loc[other, "result"], "score": (1 + cos) / 2})
        return sorted(out, key=lambda d: -d["score"])[:k]  # same score scale as Neo4j's cosine index


# --------------------------------------------------------------- 2 Detect: graph job -> pipeline input row
def to_pipeline_row(job: pd.Series) -> pd.Series:
    """The graph stores fewer columns than the pipeline expects. Fill the rest from the
    cutting table and turn 'jobs since change' into hours (about 1.6 h per job)."""
    nom = nominal_recipe(job["material"], float(job["thickness_mm"]))
    row = job.to_dict()
    row.update({
        "assist_gas": nom["assist_gas"], "focus_position_mm": nom["focus_position_mm"],
        "nozzle_standoff_mm": nom["nozzle_standoff_mm"], "nozzle_diameter_mm": 2.0,
        "nozzle_hours": 1.6 * job["nozzle_jobs_since_change"], "lens_hours": 1.6 * job["glass_jobs_since_clean"],
        "image_path": os.path.join(HERE, "media", "photos", f"{job['job_id']}.png"),
        "video_path": os.path.join(HERE, "media", "videos", f"{job['job_id']}.mp4"),
    })
    return pd.Series(row)


# --------------------------------------------------------------- 3 Retrieve: graph facts -> evidence items
def ago(minutes: int) -> str:
    return f"{minutes} min" if minutes < 120 else f"{minutes // 60} h"


def graph_evidence(graph, job: pd.Series, label: str) -> tuple[list[dict], dict, list[str]]:
    """Returns evidence items (ids G1, G2 ...), {cause: [signatures]} the graph supports,
    and the event ids that were used."""
    items, support, cited = [], {}, []

    def add(text, kind, cause=None):
        sig = f"graph:{kind}:{cause}" if cause else None
        items.append({"id": f"G{len(items) + 1}", "type": f"event_graph_{kind}", "text": text,
                      **({"signature": sig} if sig else {})})
        if cause:
            support.setdefault(cause, []).append(sig)

    repaired = set()
    for e in graph.recent_events(job["job_id"], WINDOW_DAYS):
        cited.append(e["event_id"])
        if e["type"] == "Alarm":
            link = f"; the graph links {e['code']} to cause {e['points_to']}" if e["points_to"] else ""
            add(f"alarm {e['code']} at {e['time'][:16]}, {ago(e['minutes_before'])} before the inspection{link}",
                "alarm", e["points_to"])
        else:
            add(f"maintenance '{e['action']}' at {e['time'][:16]}, {ago(e['minutes_before'])} before the inspection",
                "maintenance")
            if e["repairs"]:
                repaired.add(e["repairs"])
    # an alarm whose cause was repaired afterwards no longer supports that cause
    for c in repaired:
        support.pop(c, None)

    n_noz, n_gl = int(job["nozzle_jobs_since_change"]), int(job["glass_jobs_since_clean"])
    add(f"maintenance history: nozzle has cut {n_noz} jobs since it was replaced",
        "wear", "worn_nozzle" if n_noz >= NOZZLE_WORN_AFTER else None)
    add(f"maintenance history: protective glass has cut {n_gl} jobs since it was cleaned",
        "wear", "dirty_protective_glass" if n_gl >= GLASS_DIRTY_AFTER else None)

    prev = graph.previous_results(job["job_id"], 10)
    same = sum(r == label for r in prev)
    add(f"{same} of the previous {len(prev)} inspections also found {label}" +
        (" (a recurring problem, not a one-off)" if same >= 3 else ""), "trend")

    sim = graph.similar_cases(job["job_id"], 5)
    if sim:
        add("most similar earlier photos: " + ", ".join(f"{s['job_id']} ({s['result']}, {s['score']:.2f})" for s in sim),
            "similar_cases")
    return items, support, cited


def add_graph_to_packet(packet: dict, items: list[dict], support: dict) -> dict:
    """Graph facts become evidence, and causes they support move up the ranking."""
    p = copy.deepcopy(packet)
    p["evidence"] += items
    for path in p["knowledge_graph_paths"]:
        sigs = support.get(path["cause"], [])
        path["matched_evidence"] = path["matched_evidence"] + sigs
        path["support"] += len(sigs)
    p["knowledge_graph_paths"].sort(key=lambda d: -d["support"])
    return p


# --------------------------------------------------------------- which jobs to diagnose by default
def story_jobs(jobs: pd.DataFrame) -> dict[str, str]:
    """One job for each problem hidden in the example data, with the cause the story put there."""
    jobs = jobs.assign(day=jobs["start"].str[:10])
    pick = {}

    def first(mask, cause):
        hit = jobs[mask]
        if len(hit):
            pick[hit.iloc[0]["job_id"]] = cause

    first((jobs.day == "2026-09-05") & (jobs.defect == "dross") & (jobs.alarm_code == "E_GAS"), "low_gas_pressure")
    first(jobs.day.between("2026-09-11", "2026-09-12") & (jobs.defect == "incomplete_cut"), "dirty_protective_glass")
    first(jobs.day.between("2026-09-16", "2026-09-18") & (jobs.defect == "bevel_deviation"), "bevel_axis_drift")
    first(~jobs.day.between("2026-09-05", "2026-09-07") & jobs.defect.isin(["dross", "rough_striations"])
          & (jobs.nozzle_jobs_since_change >= 60), "worn_nozzle")
    return pick


def train_or_load(llm, epochs: int):
    cache = os.path.join(HERE, "outputs", "pipeline.pkl")
    if os.path.exists(cache):
        print(f"Loading trained pipeline from {cache}")
        with open(cache, "rb") as f:
            pipe = pickle.load(f)
        pipe.llm = llm
        return pipe
    demo = os.path.join(PIPE, "demo_data")
    data = os.path.join(demo, "jobs.csv")
    if not os.path.exists(data):
        print("Generating the pipeline's synthetic demo data ...")
        write_demo_dataset(demo, 1500)
    df = load_machine_table(data).sample(frac=1, random_state=0)
    n = int(0.85 * len(df))
    pipe = FaultDiagnosisPipeline(os.path.join(PIPE, "knowledge_base", "laser_kg.json"),
                                  os.path.join(demo, "knowledge_base"), llm)
    pipe.fit(df.iloc[:n], df.iloc[n:], image_epochs=epochs)
    os.makedirs(os.path.dirname(cache), exist_ok=True)
    pipe.llm = None
    with open(cache, "wb") as f:
        pickle.dump(pipe, f)
    pipe.llm = llm
    return pipe


def top_cause(report: dict | None) -> str:
    causes = (report or {}).get("root_causes") or []
    return causes[0]["cause"] if causes else "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", nargs="*", help="job ids to diagnose (default: one job per problem in the story)")
    ap.add_argument("--password", help="Neo4j password. Leave out to read the graph from csv/ instead")
    ap.add_argument("--uri", default="neo4j://127.0.0.1:7687")
    ap.add_argument("--user", default="neo4j")
    ap.add_argument("--database", default="neo4j")
    ap.add_argument("--write-back", action="store_true", help="store each diagnosis in Neo4j (step 5 Learn)")
    ap.add_argument("--llm", default="offline", choices=["offline", "ollama"])
    ap.add_argument("--model", default="qwen2.5:7b-instruct")
    ap.add_argument("--epochs", type=int, default=8)
    args = ap.parse_args()

    graph = Neo4jGraph(args.uri, args.user, args.password, args.database) if args.password \
        else CsvGraph(os.path.join(HERE, "csv"))
    print(f"Reading the graph from {graph.name}")
    llm = get_llm(args.llm, **({"model": args.model} if args.llm == "ollama" else {}))
    pipe = train_or_load(llm, args.epochs)

    jobs = graph.jobs().set_index("job_id", drop=False)
    expected = story_jobs(jobs.reset_index(drop=True))
    chosen = args.jobs or list(expected)
    out_dir = os.path.join(HERE, "outputs", "reports")
    os.makedirs(out_dir, exist_ok=True)

    md = ["# Pipeline on the example knowledge graph", "",
          f"Graph read from: {graph.name}. LLM: {llm.name}.", "",
          "| Job | True defect | Pipeline decision | Cause the story planted | Top cause, pipeline alone "
          "| Top cause, pipeline + event graph |", "|---|---|---|---|---|---|"]
    for job_id in chosen:
        job = jobs.loc[job_id]
        print(f"\nDiagnosing {job_id} ...")
        alone = pipe.diagnose(to_pipeline_row(job))           # 2 Detect (+ the pipeline's own KG and manual search)
        packet = alone["packet"]
        label = packet["decision"]["label"]
        if label == "unknown":
            label = packet["decision"]["best_guess"]
        items, support, cited = graph_evidence(graph, job, label)            # 3 Retrieve
        with_graph = reason(pipe.llm, add_graph_to_packet(packet, items, support))  # 4 Explain
        if args.write_back and isinstance(graph, Neo4jGraph):               # 5 Learn
            graph.write_back(job_id, with_graph["report"] or {}, packet["decision"], cited)
        result = {"job_id": job_id, "true_defect": job["defect"], "decision": packet["decision"],
                  "graph_evidence": items, "report_pipeline_alone": alone["report"],
                  "report_with_graph": with_graph["report"], "problems": with_graph["problems"]}
        with open(os.path.join(out_dir, f"{job_id}.json"), "w") as f:
            json.dump(result, f, indent=1, default=str)
        md.append(f"| {job_id} | {job['defect']} | {packet['decision']['label']} | {expected.get(job_id, '-')} "
                  f"| {top_cause(alone['report'])} | {top_cause(with_graph['report'])} |")
        for e in items:
            print(f"  {e['id']}: {e['text']}")
        print(f"  top cause alone: {top_cause(alone['report'])}   with graph: {top_cause(with_graph['report'])}")

    md += ["", "Full reports, with every piece of evidence and its id, are in `outputs/reports/`.",
           "The data is made up, so this table shows the method works, not research results."]
    with open(os.path.join(HERE, "outputs", "summary.md"), "w") as f:
        f.write("\n".join(md))
    print("\n" + "\n".join(md))
    if args.write_back and isinstance(graph, Neo4jGraph):
        print("\nIn Neo4j, see the stored diagnoses with:\n"
              "  MATCH p=(d:Diagnosis)-[]->() RETURN p")


if __name__ == "__main__":
    main()
