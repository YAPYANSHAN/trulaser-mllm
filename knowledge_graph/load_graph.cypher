// Build the example event-centric multimodal knowledge graph in Neo4j.
// Copy the files in csv/ into your database's "import" folder first (see README).
// Paste this whole file into Neo4j Browser and run it (or run it block by block).

// ---------- 0. Start clean and add uniqueness rules
MATCH (n) DETACH DELETE n;
CREATE CONSTRAINT job_id IF NOT EXISTS FOR (j:Job) REQUIRE j.job_id IS UNIQUE;
CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.event_id IS UNIQUE;
CREATE CONSTRAINT defect_name IF NOT EXISTS FOR (d:DefectType) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT cause_name IF NOT EXISTS FOR (c:Cause) REQUIRE c.name IS UNIQUE;
CREATE CONSTRAINT remedy_name IF NOT EXISTS FOR (r:Remedy) REQUIRE r.name IS UNIQUE;

// ---------- 1. Knowledge layer: defect -> cause -> remedy, with the manual section as source
LOAD CSV WITH HEADERS FROM 'file:///knowledge.csv' AS row
WITH row WHERE row.relation = 'CAUSED_BY'
MERGE (d:DefectType {name: row.subject})
MERGE (c:Cause {name: row.object})
MERGE (d)-[:CAUSED_BY {source: row.source}]->(c);

LOAD CSV WITH HEADERS FROM 'file:///knowledge.csv' AS row
WITH row WHERE row.relation = 'FIXED_BY'
MERGE (c:Cause {name: row.subject})
MERGE (r:Remedy {name: row.object})
MERGE (c)-[:FIXED_BY {source: row.source}]->(r);

LOAD CSV WITH HEADERS FROM 'file:///alarm_causes.csv' AS row
MERGE (a:AlarmCode {code: row.code})
MERGE (c:Cause {name: row.cause})
MERGE (a)-[:POINTS_TO]->(c);

LOAD CSV WITH HEADERS FROM 'file:///component_causes.csv' AS row
MERGE (m:Component {name: row.component})
MERGE (c:Cause {name: row.cause})
MERGE (m)-[:CAN_CAUSE]->(c);

// ---------- 2. Event layer: every event gets the :Event label plus its own type
LOAD CSV WITH HEADERS FROM 'file:///jobs.csv' AS row
MERGE (j:Job:Event {job_id: row.job_id})
SET j.timestamp = datetime(row.start), j.material = row.material,
    j.thickness_mm = toFloat(row.thickness_mm), j.laser_power_w = toFloat(row.laser_power_w),
    j.cutting_speed_mm_min = toFloat(row.cutting_speed_mm_min), j.gas_pressure_bar = toFloat(row.gas_pressure_bar),
    j.bevel_angle_deg = toFloat(row.bevel_angle_deg),
    j.nozzle_jobs_since_change = toInteger(row.nozzle_jobs_since_change),
    j.glass_jobs_since_clean = toInteger(row.glass_jobs_since_clean);

LOAD CSV WITH HEADERS FROM 'file:///events.csv' AS row
WITH row WHERE row.type = 'Job'
MATCH (j:Job {job_id: row.job_id})
SET j.event_id = row.event_id;

LOAD CSV WITH HEADERS FROM 'file:///events.csv' AS row
WITH row WHERE row.type = 'Inspection'
MATCH (j:Job {job_id: row.job_id})
CREATE (i:Inspection:Event {event_id: row.event_id, timestamp: datetime(row.timestamp), result: row.result})
CREATE (i)-[:OF_JOB]->(j)
WITH i, row WHERE row.result <> 'ok'
MATCH (d:DefectType {name: row.result})
CREATE (i)-[:IS_A]->(d);

LOAD CSV WITH HEADERS FROM 'file:///events.csv' AS row
WITH row WHERE row.type = 'Alarm'
CREATE (a:Alarm:Event {event_id: row.event_id, timestamp: datetime(row.timestamp), code: row.code, text: row.text})
WITH a, row
MATCH (ac:AlarmCode {code: row.code})
CREATE (a)-[:INSTANCE_OF]->(ac)
WITH a, row WHERE row.job_id IS NOT NULL
MATCH (j:Job {job_id: row.job_id})
CREATE (a)-[:DURING]->(j);

LOAD CSV WITH HEADERS FROM 'file:///events.csv' AS row
WITH row WHERE row.type = 'Maintenance'
CREATE (m:Maintenance:Event {event_id: row.event_id, timestamp: datetime(row.timestamp), action: row.action})
WITH m, row
MATCH (c:Component {name: row.component})
CREATE (m)-[:ON_COMPONENT]->(c);

// link all events in time order with NEXT
MATCH (e:Event)
WITH e ORDER BY e.timestamp, e.event_id
WITH collect(e) AS es
UNWIND range(0, size(es) - 2) AS k
WITH es[k] AS a, es[k + 1] AS b
CREATE (a)-[:NEXT]->(b);

// ---------- 3. Media nodes: photos and video clips captured during each job
LOAD CSV WITH HEADERS FROM 'file:///photos.csv' AS row
MATCH (j:Job {job_id: row.job_id})
CREATE (p:Photo {photo_id: row.photo_id, file: row.file, model_label: row.model_label,
                 confidence: toFloat(row.confidence),
                 embedding: [x IN split(row.embedding, ';') | toFloat(x)]})
CREATE (j)-[:CAPTURED]->(p);

LOAD CSV WITH HEADERS FROM 'file:///videos.csv' AS row
MATCH (j:Job {job_id: row.job_id})
CREATE (v:VideoClip {video_id: row.video_id, file: row.file, model_label: row.model_label,
                     unusual_signal: row.unusual_signal})
CREATE (j)-[:CAPTURED]->(v);

// vector index so a photo can find similar photos (needs Neo4j 5.13 or newer)
CREATE VECTOR INDEX photo_embedding IF NOT EXISTS
FOR (p:Photo) ON (p.embedding)
OPTIONS {indexConfig: {`vector.dimensions`: 64, `vector.similarity_function`: 'cosine'}};
