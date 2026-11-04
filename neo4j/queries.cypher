// Handy queries for Neo4j Browser

// one bad job and everything it links to (drag the circles around)
MATCH (j:Job {name: 'JOB-00391'})-[r]-(n) WHERE type(r) <> 'NEXT' RETURN j, r, n;

// the explanation path: job -> recent alarm -> code -> cause -> the job's defect
MATCH (j:Job {name: 'JOB-00391'})-[la:LAST_ALARM]->(:AlarmEvent)-[:INSTANCE_OF]->(c:AlarmCode)-[:INDICATES]->(cause:Cause)-[:CAUSES]->(d:Defect)<-[:HAS_DEFECT]-(j)
WHERE la.hours_before <= 24
RETURN c.name AS alarm, la.hours_before AS hours_before, la.count_24h AS in_last_24h, cause.name AS cause, d.name AS defect;

// the schema itself (one circle per node type)
CALL db.schema.visualization();
