import sqlite3

connection = sqlite3.connect("academic.db")
connection.execute("PRAGMA foreign_keys = ON")

cursor = connection.cursor()

#Students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    year INTEGER NOT NULL
)
""")

#Courses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY,
    course_name TEXT NOT NULL,
    credits INTEGER NOT NULL
)
""")

#Enrollments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    UNIQUE (student_id, course_id)
)
""")

#Marks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    marks_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    marks INTEGER NOT NULL CHECK (marks BETWEEN 0 AND 100),
    grade TEXT NOT NULL,
    FOREIGN KEY (student_id, course_id)
        REFERENCES enrollments(student_id, course_id),
    UNIQUE (student_id, course_id)
)
""")

#adding records
#for students
cursor.executemany("""
INSERT OR IGNORE INTO students
(student_id, name, department, year)
VALUES (?, ?, ?, ?)
""", [
    (1, "Aarav", "AI", 2),
    (2, "Meera", "CSE", 2),
    (3, "Riya", "AI", 1),
    (4, "Kabir", "ECE", 2),
    (5, "Neha", "CSE", 1)
])

#for courses
cursor.executemany("""
INSERT OR IGNORE INTO courses
(course_id, course_name, credits)
VALUES (?, ?, ?)
""", [
    (101, "DBMS", 4),
    (102, "Python", 3),
    (103, "Mathematics", 4)
])

#connecting students to courses
cursor.executemany("""
INSERT OR IGNORE INTO enrollments
(enrollment_id, student_id, course_id)
VALUES (?, ?, ?)
""", [
    (1, 1, 101),
    (2, 2, 101),
    (3, 3, 102),
    (4, 4, 103),
    (5, 5, 102),
    (6, 1, 102)
])

#adding marks for the enrollment
cursor.executemany("""
INSERT OR IGNORE INTO marks
(marks_id, student_id, course_id, marks, grade)
VALUES (?, ?, ?, ?, ?)
""", [
    (1, 1, 101, 85, "A"),
    (2, 2, 101, 76, "B"),
    (3, 3, 102, 92, "A"),
    (4, 4, 103, 65, "C"),
    (5, 5, 102, 88, "A"),
    (6, 1, 102, 90, "A")
])

connection.commit()


#show student values
cursor.execute("SELECT * FROM students")

print("Students: ")
for row in cursor.fetchall():
    print(row)


connection.close()