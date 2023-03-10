# Здесь представлены запросы к БД, с помощью которых тестил работоспособность
# Это первый запрос на участников события под номером 189
# event_id = 189
# result = session.run(
#     "MATCH (p:Person)-[:PARTICIPATED_IN]->(e:Event) "
#     "WHERE e.id = $event_id "
#     "RETURN p.name",
#     {"event_id": event_id})
# for record in result:
#     print(record['p.name'])
#
# Это второй запрос, здесь уже предлагается ввести имена двух участников и найти объединяет ли их какие-либо событие
# participant1_name = input("Введите ФИО первого участника: ")
# participant2_name = input("Введите ФИО второго участника: ")
#
# result3 = session.run(
#     "MATCH (p1:Person)-[:PARTICIPATED_IN]->(e:Event)<-[:PARTICIPATED_IN]-(p2:Person) "
#     "WHERE p1.name = $participant1_name AND p2.name = $participant2_name "
#     "RETURN e.event_id",
#     {"participant1_name": participant1_name, "participant2_name": participant2_name})
# for record in result3:
#     print(record['e.event_id'])
#
# driver.close()


