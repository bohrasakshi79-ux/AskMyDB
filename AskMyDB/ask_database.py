import sqlite3
from rules import get_query

question = input("Enter your question: ")
query = get_query(question)

if query is None:
    print("Question not supported.")
else:
    sql, parameters = query

    connection = sqlite3.connect("academic.db")
    cursor = connection.cursor()

    print("\nGenerated SQL:", sql)
    print("Parameters:", parameters)

    cursor.execute(sql, parameters)
    rows = cursor.fetchall()

    print("\nResults:")
    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching records found.")

    connection.close()