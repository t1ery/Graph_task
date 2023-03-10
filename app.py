from neo4j import GraphDatabase, basic_auth
from flask import Flask, request, jsonify, render_template

# Создаем экземпляр приложения
app = Flask(__name__)

# Устанавливаем параметры для подключения к базе данных
uri = "bolt://localhost:7687"
username = "neo4j"
password = "neo4j"

# Создаем экземпляр драйвера для работы с базой данных
driver = GraphDatabase.driver(uri, auth=basic_auth(username, password))

# Определяем функцию обработки корневой страницы
@app.route('/')
def index():
    return render_template('index.html')

# Определяем функцию обработки запроса к базе данных
@app.route('/graph', methods=['POST'])
def get_data():
    # Проверяем метод запроса
    if request.method == 'POST':
        # Проверяем, что в запросе есть параметр fio и он не пустой
        if 'fio' in request.form and request.form['fio']:
            fio = request.form['fio']
            # Проверяем, что ФИО состоит только из букв и пробелов
            if all(c.isalpha() or c.isspace() for c in fio):
                cypher_query = """
                MATCH (p:Person {name: $fio})-[:PARTICIPATED_IN]->(e:Event)<-[:PARTICIPATED_IN]-(p2:Person)
                RETURN p.name, e.id, p2.name
                """
                with driver.session() as session:
                    result = session.run(cypher_query, fio=fio)
                    nodes = []
                    edges = []
                    # Формируем список узлов и ребер в формате JSON
                    for record in result:
                        nodes.append({'id': record[0], 'label': record[0]})
                        nodes.append({'id': record[2], 'label': record[2]})
                        edges.append(
                            {'from': record[0], 'to': record[2], 'label': 'Событие номер: ' + str(record[1])})
                    # Возвращаем ответ в формате JSON
                    return jsonify({'nodes': nodes, 'edges': edges})
            else:
                # Возвращаем сообщение об ошибке, если ФИО имеет неверный формат
                return 'Invalid format of fio parameter'
        else:
            # Возвращаем сообщение об ошибке, если не передан параметр fio
            return 'Missing fio parameter'
    else:
        # Возвращаем сообщение об ошибке, если метод запроса неверный
        return 'Invalid request method'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

