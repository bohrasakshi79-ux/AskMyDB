import sqlite3

connection = sqlite3.connect("academic.db")
cursor = connection.cursor()

print("\nStudents: ")
cursor.execute("SELECT * FROM students")
for row in cursor.fetchall():
    print(row)


print("\nCourses: ")
cursor.execute("SELECT * FROM courses")
for row in cursor.fetchall():
    print(row)


print("\nENROLLMENTS: ")
cursor.execute("SELECT * FROM enrollments")
for row in cursor.fetchall():
    print(row)

print("\nMARKS: ")
cursor.execute("SELECT * FROM marks")
for row in cursor.fetchall():
    print(row)


connection.close()