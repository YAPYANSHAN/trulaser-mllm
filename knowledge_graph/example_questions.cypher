// Example questions for the event-centric multimodal knowledge graph.
// Run them one at a time in Neo4j Browser after load_graph.cypher.

// Q1. Look at the graph: one dross inspection with its job, photo, video,
//     the defect type, its causes and their fixes.
MATCH (i:Inspection {result: 'dross'})-[:OF_JOB]->(j:Job)
WITH i, j LIMIT 1
MATCH (j)-[:CAPTURED]->(media)
MATCH (i)-[:IS_A]->(d:DefectType)-[:CAUSED_BY]->(c:Cause)-[:FIXED_BY]->(r:Remedy)
RETURN i, j, media, d, c, r;

// Q2. Root-cause tracing: for each dross inspection, which alarms happened in the
//     2 hours before it, and which known cause of dross do they point to?
MATCH (i:Inspection {result: 'dross'})-[:IS_A]->(d:DefectType)-[:CAUSED_BY]->(c:Cause)
MATCH (a:Alarm)-[:INSTANCE_OF]->(:AlarmCode)-[:POINTS_TO]->(c)
WHERE a.timestamp <= i.timestamp AND a.timestamp >= i.timestamp - duration('PT2H')
RETURN i.event_id AS inspection, toString(i.timestamp) AS time, c.name AS likely_cause,
       collect(DISTINCT a.code) AS alarms_before
ORDER BY time;

// Q3. Maintenance effect: share of dross or rough cuts, grouped by how many jobs
//     the nozzle had done since it was last replaced.
MATCH (i:Inspection)-[:OF_JOB]->(j:Job)
WITH j.nozzle_jobs_since_change / 20 * 20 AS since_nozzle_change,
     i.result IN ['dross', 'rough_striations'] AS worn_nozzle_defect
RETURN since_nozzle_change, count(*) AS jobs,
       round(100.0 * sum(CASE WHEN worn_nozzle_defect THEN 1 ELSE 0 END) / count(*)) AS percent_dross_or_rough
ORDER BY since_nozzle_change;

// Q4. What happened just before a defect? Walk back 6 events along NEXT.
MATCH (i:Inspection {result: 'bevel_deviation'})
WITH i ORDER BY i.timestamp LIMIT 1
MATCH path = (before:Event)-[:NEXT*1..6]->(i)
RETURN path ORDER BY length(path) DESC LIMIT 1;

// Q5. Multimodal similar-case search: the 5 past photos most like the photo of
//     one dross job, and the defects and fixes recorded for those jobs.
//     (Needs the vector index, Neo4j 5.13 or newer.)
MATCH (:Job {job_id: 'J0072'})-[:CAPTURED]->(p:Photo)
CALL db.index.vector.queryNodes('photo_embedding', 6, p.embedding) YIELD node, score
WHERE node <> p
MATCH (other:Job)-[:CAPTURED]->(node)
MATCH (ins:Inspection)-[:OF_JOB]->(other)
OPTIONAL MATCH (ins)-[:IS_A]->(:DefectType)-[:CAUSED_BY]->(:Cause)-[:FIXED_BY]->(r:Remedy)
RETURN other.job_id AS similar_job, round(score, 3) AS similarity, ins.result AS defect,
       collect(DISTINCT r.name) AS fixes;

// Q6. The evidence pack the LLM would receive for one job (graph RAG):
//     its defect, the video signal, recent alarms and maintenance, and the
//     causes and fixes with their manual sources.
MATCH (i:Inspection)-[:OF_JOB]->(j:Job {job_id: 'J0072'})
OPTIONAL MATCH (j)-[:CAPTURED]->(v:VideoClip)
OPTIONAL MATCH (e:Event) WHERE (e:Alarm OR e:Maintenance)
  AND e.timestamp <= i.timestamp AND e.timestamp >= i.timestamp - duration('P3D')
OPTIONAL MATCH (i)-[:IS_A]->(d:DefectType)-[cb:CAUSED_BY]->(c:Cause)-[:FIXED_BY]->(r:Remedy)
RETURN j.job_id AS job, i.result AS defect, v.unusual_signal AS video_signal,
       collect(DISTINCT coalesce(e.code, e.action)) AS recent_events,
       collect(DISTINCT {cause: c.name, fix: r.name, source: cb.source}) AS knowledge;
