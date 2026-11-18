import sqlite3
from pathlib import Path

database = Path(__file__).resolve().parent / "academic.db"

if not database.exists():
    raise FileNotFoundError("Run setup_database.py first.")

connection = sqlite3.connect(database)
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

# student_id, name, department, year, course_id, marks, grade
records = [
    (6, "Aditi", "AI", 1, 101, 91, "A"),
    (7, "Arjun", "CSE", 2, 102, 78, "B"),
    (8, "Ananya", "ECE", 1, 103, 86, "A"),
    (9, "Dev", "AI", 2, 101, 69, "C"),
    (10, "Ishita", "CSE", 1, 102, 95, "A"),
    (11, "Karan", "ECE", 2, 103, 73, "B"),
    (12, "Kavya", "AI", 1, 101, 88, "A"),
    (13, "Manav", "CSE", 2, 102, 62, "C"),
    (14, "Nisha", "ECE", 1, 103, 81, "A"),
    (15, "Pranav", "AI", 2, 101, 54, "D"),
    (16, "Priya", "CSE", 1, 102, 90, "A"),
    (17, "Rahul", "ECE", 2, 103, 47, "E"),
    (18, "Sanya", "AI", 1, 101, 76, "B"),
    (19, "Rohan", "CSE", 2, 102, 84, "A"),
    (20, "Sneha", "ECE", 1, 103, 67, "C"),
    (21, "Tanvi", "AI", 2, 101, 93, "A"),
    (22, "Varun", "CSE", 1, 102, 58, "D"),
    (23, "Vidhi", "ECE", 2, 103, 72, "B"),
    (24, "Yash", "AI", 1, 101, 39, "F"),
    (25, "Zoya", "CSE", 2, 102, 87, "A"),
]

try:
    for student_id, name, department, year, course_id, marks, grade in records:

        cursor.execute("""
            INSERT OR IGNORE INTO students
            (student_id, name, department, year)
            VALUES (?, ?, ?, ?)
        """, (student_id, name, department, year))

        cursor.execute("""
            INSERT OR IGNORE INTO enrollments
            (student_id, course_id)
            VALUES (?, ?)
        """, (student_id, course_id))

        cursor.execute("""
            INSERT OR IGNORE INTO marks
            (student_id, course_id, marks, grade)
            VALUES (?, ?, ?, ?)
        """, (student_id, course_id, marks, grade))

    connection.commit()

    print("Additional sample records saved successfully!")

    for table in ("students", "courses", "enrollments", "marks"):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]}")

except sqlite3.Error:
    connection.rollback()
    raise

finally:
    connection.close()