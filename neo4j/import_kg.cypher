// TruLaser knowledge graph -> Neo4j 5 (no plugins needed)
// Needs kg_nodes.csv and kg_edges.csv from notebook 04 (data/processed/).
// Copy both files into the database's import folder, then paste this whole file into Neo4j Browser and run.

// 0. start empty (only on a database used for this project)
MATCH (n) DETACH DELETE n;

// 1. one index so edges find their nodes fast
CREATE CONSTRAINT node_id IF NOT EXISTS FOR (n:Node) REQUIRE n.id IS UNIQUE;

// 2. nodes: every row becomes a :Node with all its columns, then gets its own label from 'kind'
LOAD CSV WITH HEADERS FROM 'file:///kg_nodes.csv' AS r CREATE (n:Node) SET n = r;
MATCH (n:Node {kind: 'Job'}) SET n:Job;
MATCH (n:Node {kind: 'Inspection'}) SET n:Inspection;
MATCH (n:Node {kind: 'AlarmEvent'}) SET n:AlarmEvent;
MATCH (n:Node {kind: 'Maintenance'}) SET n:Maintenance;
MATCH (n:Node {kind: 'Cause'}) SET n:Cause;
MATCH (n:Node {kind: 'Fix'}) SET n:Fix;
MATCH (n:Node {kind: 'AlarmCode'}) SET n:AlarmCode;
MATCH (n:Node {kind: 'Defect'}) SET n:Defect;

// numbers and times as real types (CSV gives text)
MATCH (n:Job) SET n.nozzle_hours = toFloat(n.nozzle_hours), n.feed_vs_table = toFloat(n.feed_vs_table), n.feed = toFloat(n.feed), n.thickness = toFloat(n.thickness), n.start = datetime(replace(n.start, ' ', 'T')), n.end = datetime(replace(n.end, ' ', 'T'));
MATCH (n) WHERE n:AlarmEvent OR n:Maintenance OR n:Inspection SET n.time = datetime(replace(n.time, ' ', 'T'));

// 3. edges, one statement per type from the schema in notebook 04
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'CAUSES' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:CAUSES {rank: toInteger(toFloat(r.rank)), gas: r.gas, source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'FIXED_BY' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:FIXED_BY {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'INDICATES' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:INDICATES {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'NEXT' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:NEXT {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'INSPECTED_IN' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:INSPECTED_IN {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'FOUND' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:FOUND {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'HAS_DEFECT' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:HAS_DEFECT {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'INSTANCE_OF' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:INSTANCE_OF {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'DURING' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:DURING {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'LAST_ALARM' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:LAST_ALARM {code: r.code, hours_before: toFloat(r.hours_before), count_24h: toInteger(toFloat(r.count_24h)), source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'RESETS' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:RESETS {source: r.source}]->(b);
LOAD CSV WITH HEADERS FROM 'file:///kg_edges.csv' AS r WITH r WHERE r.type = 'AFTER_REPAIR' MATCH (a:Node {id: r.from_id}), (b:Node {id: r.to_id}) CREATE (a)-[:AFTER_REPAIR {cause: r.cause, hours_since: toFloat(r.hours_since), source: r.source}]->(b);

// 4. check: should match notebook 04 (1,239 nodes, 5,221 edges)
MATCH (n) RETURN count(n) AS nodes;
MATCH ()-[r]->() RETURN count(r) AS edges;
