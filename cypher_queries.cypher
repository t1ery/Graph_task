// Загружаем данные из CSV файла, создаем узлы Person и Event и отношения PARTICIPATED_IN
LOAD CSV WITH HEADERS FROM "file:///data_test.csv" AS row
WITH row
MERGE (p1:Person {name: row.`ФИО участника события 1`})
MERGE (p2:Person {name: row.`ФИО участника события 2`})
MERGE (e:Event {id: toInteger(row.`id события`)})
MERGE (p1)-[:PARTICIPATED_IN {event_id: toInteger(row.`id события`)}]->(e)
MERGE (p2)-[:PARTICIPATED_IN {event_id: toInteger(row.`id события`)}]->(e)
WITH *

// Проверяем, существует ли уже граф с именем 'my-graph'
CALL gds.graph.exists('my-graph')
YIELD exists AS graph_exists
WITH graph_exists
WHERE NOT graph_exists // если граф не существует, то создаем его
CALL gds.graph.CREATE(
  'my-graph',
  'Person',
  {
    PARTICIPATED_IN:{
      orientation: 'UNDIRECTED',
      properties:{
        event_id:{
          property: 'event_id',
          defaultValue:0.0
        }
      }
    }
  }
) YIELD graphName, nodeCount, relationshipCount, createMillis
WITH *

// Запускаем алгоритм Лувена для поиска сообществ в графе
// Сохраняем результаты в свойство communityId каждого узла Person
CALL gds.louvain.stream('my-graph')
YIELD nodeId, communityId
MATCH (p:Person) WHERE id(p) = nodeId
SET p.communityId = communityId;


