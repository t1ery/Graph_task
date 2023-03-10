from neo4j import GraphDatabase
from data_loader import read_from_YD

# Подключение к базе данных Neo4j
uri = "bolt://localhost:7687"
username = "neo4j"
password = "neo4j"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Загрузка данных из файла на Яндекс.Диске
folder_url = input("Введите ссылку на файл: ")
file_url = 'data_test.csv'
df = read_from_YD(folder_url, file_url)

# Загрузка Cypher-запросов из файла
with open('cypher_queries.cypher') as f:
    cypher_queries = f.read()

with driver.session() as session:
    # Загрузка данных в Neo4j и запуск алгоритма Лувена
    tx = session.begin_transaction()
    for query in cypher_queries.split(";"):
        if query.strip() != "":
            tx.run(query)
    tx.commit()

    # Вывод результатов
    result = session.run("MATCH (p:Person) RETURN p.name, p.communityId")
    for record in result:
        print(record['p.name'], record['p.communityId'])

# Закрытие соединения с базой данных
driver.close()

