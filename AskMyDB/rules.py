import re


def get_query(question):
    question = question.lower().strip()
    question = question.rstrip("?.!")
    question = " ".join(question.split())

    if question in ("show all students", "list all students"):
        return "SELECT * FROM students", ()

    elif question in ("show all courses", "list all courses"):
        return "SELECT * FROM courses", ()

    elif question == "count students":
        return "SELECT COUNT(*) AS total_students FROM students", ()

    elif question in ("show the highest mark", "highest mark"):
        return "SELECT MAX(marks) AS highest_mark FROM marks", ()

    elif question in ("what is the average mark", "average mark"):
        return "SELECT AVG(marks) AS average_mark FROM marks", ()

    elif question in ("sort students by name", "list students by name"):
        return "SELECT * FROM students ORDER BY name", ()

    elif question == "count students in each department":
        sql = """
        SELECT department, COUNT(*) AS total_students
        FROM students
        GROUP BY department
        ORDER BY department
        """

        return sql, ()
    
    # Marks filtering
    match = re.fullmatch(
        r"show students with marks above (\d+)",
        question
    )

    if match:
        number = int(match.group(1))

        sql = """
        SELECT s.name, c.course_name, m.marks
        FROM marks AS m
        JOIN students AS s ON s.student_id = m.student_id
        JOIN courses AS c ON c.course_id = m.course_id
        WHERE m.marks > ?
        """

        return sql, (number,)

    # Department filtering
    match = re.fullmatch(
        r"show students from the ([a-z]+) department",
        question
    )

    if match:
        department = match.group(1).upper()

        sql = "SELECT * FROM students WHERE department = ?"

        return sql, (department,)

    # Show the top N marks
    match = re.fullmatch(
        r"show the (\d+) highest marks",
        question
    )

    if match:
        number = int(match.group(1))

        if number < 1:
            return None

        sql = """
        SELECT s.name, c.course_name, m.marks
        FROM marks AS m
        JOIN students AS s ON s.student_id = m.student_id
        JOIN courses AS c ON c.course_id = m.course_id
        ORDER BY m.marks DESC, s.student_id, c.course_id
        LIMIT ?
        """

        return sql, (number,)
    
    if question == "find the average marks for each course":
        sql = """
        SELECT c.course_name,
               ROUND(AVG(m.marks), 2) AS average_marks
        FROM marks AS m
        JOIN courses AS c ON c.course_id = m.course_id
        GROUP BY c.course_id, c.course_name
        ORDER BY c.course_name
        """

        return sql, ()
    return None