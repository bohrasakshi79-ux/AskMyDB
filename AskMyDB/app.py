import sqlite3
from pathlib import Path
from contextlib import closing

import pandas as pd
import streamlit as st

from rules import get_query


st.set_page_config(
    page_title="AskMyDB",
    page_icon="🔎",
    layout="wide"
)

DATABASE = Path(__file__).resolve().parent / "academic.db"


def connect_database():
    return sqlite3.connect(
        DATABASE.as_uri() + "?mode=ro",
        uri=True
    )


def choose_example(question):
    st.session_state["question"] = question


# Peach, cream, navy and rose theme
st.markdown("""
<style>
/* Main page */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #EEE2DC !important;
    color: #123C69 !important;
    color-scheme: light;
}

/* Top toolbar */
[data-testid="stHeader"] {
    background-color: #EEE2DC !important;
}

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background-color: #EDC7B7 !important;
}

/* Layout */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #123C69 !important;
}

/* Text and labels */
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"] {
    color: #123C69 !important;
}

[data-testid="stCaptionContainer"] {
    color: #4E5265 !important;
}

/* Summary cards */
[data-testid="stMetric"] {
    background-color: #F8F1ED !important;
    border: 1px solid #BAB2B5 !important;
    border-top: 4px solid #AC3B61 !important;
    border-radius: 10px;
    padding: 18px;
}

/* Question form */
[data-testid="stForm"] {
    background-color: #F8F1ED !important;
    border: 1px solid #BAB2B5 !important;
    border-radius: 10px;
    padding: 22px;
}

/* Input field */
[data-testid="stTextInput"] [data-baseweb="input"],
[data-testid="stTextInput"] [data-baseweb="base-input"] {
    background-color: #FFFAF7 !important;
    border-color: #BAB2B5 !important;
}

[data-testid="stTextInput"] input {
    background-color: #FFFAF7 !important;
    color: #123C69 !important;
    -webkit-text-fill-color: #123C69 !important;
    caret-color: #AC3B61;
}

[data-testid="stTextInput"] input::placeholder {
    color: #626579 !important;
    -webkit-text-fill-color: #626579 !important;
    opacity: 1;
}

/* Example and download buttons */
div.stButton > button,
div.stDownloadButton > button {
    background-color: #EDC7B7 !important;
    color: #123C69 !important;
    border: 1px solid #C99F90 !important;
    border-radius: 7px;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background-color: #F5D8CC !important;
    border-color: #AC3B61 !important;
}

/* Run query button */
[data-testid="stFormSubmitButton"] > button {
    background-color: #AC3B61 !important;
    color: #FFFFFF !important;
    border: 1px solid #AC3B61 !important;
    border-radius: 7px;
}

[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #922F51 !important;
    border-color: #922F51 !important;
}

[data-testid="stFormSubmitButton"] > button p,
[data-testid="stFormSubmitButton"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}

/* Expandable sections */
[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background-color: #F8F1ED !important;
    color: #123C69 !important;
    border-radius: 8px;
}

[data-testid="stExpander"] {
    border: 1px solid #BAB2B5 !important;
}

/* Results tabs */
button[role="tab"] {
    color: #123C69 !important;
}

button[role="tab"][aria-selected="true"] {
    color: #AC3B61 !important;
}

[data-baseweb="tab-highlight"] {
    background-color: #AC3B61 !important;
}

/* SQL display */
[data-testid="stCode"],
[data-testid="stCode"] pre,
[data-testid="stCode"] code {
    background-color: #F8F1ED !important;
    color: #123C69 !important;
}

/* Dividers */
hr {
    border-color: #BAB2B5 !important;
}
</style>
""", unsafe_allow_html=True)


# Check that the database exists
if not DATABASE.exists():
    st.error(
        "academic.db was not found. "
        "Run setup_database.py first."
    )
    st.stop()


# Sidebar
with st.sidebar:
    st.title("AskMyDB")
    st.caption("DBMS Mini Project • Semester 3")

    st.markdown("**Created by:**")
    st.write("Sakshi Bohra")
    st.caption("Enrollment no. A25ARIU0062")

    st.write("Anya Maurya")
    st.caption("Enrollment no. A25ARIU0066")

    st.divider()

    st.subheader("Database details")
    st.write("Database: academic.db")
    st.write("Type: SQLite")
    st.write("Access: Read only")

    with st.expander("Table structure"):
        st.markdown("""
**Students**
- student_id
- name
- department
- year

**Courses**
- course_id
- course_name
- credits

**Enrollments**
- enrollment_id
- student_id
- course_id

**Marks**
- marks_id
- student_id
- course_id
- marks
- grade
        """)

    st.divider()

    st.subheader("How to use")
    st.write("1. Type a supported question or select an example.")
    st.write("2. Click Run query.")
    st.write("3. View the results and the SQL query.")

    st.caption(
        "The app supports predefined English question patterns."
    )


# Header
st.title("AskMyDB")
st.subheader("Search student records using simple English")

st.write(
    "We built AskMyDB as a DBMS mini project to make it easier "
    "to find information about students, courses and marks "
    "without writing SQL manually."
)

st.caption(
    "Type a supported question below. The app uses predefined "
    "rules to select an SQL query and display the results."
)

st.divider()


# Database summary
try:
    with closing(connect_database()) as connection:
        student_count = connection.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        course_count = connection.execute(
            "SELECT COUNT(*) FROM courses"
        ).fetchone()[0]

        enrollment_count = connection.execute(
            "SELECT COUNT(*) FROM enrollments"
        ).fetchone()[0]

        average_mark = connection.execute(
            "SELECT AVG(marks) FROM marks"
        ).fetchone()[0]

except sqlite3.Error as error:
    st.error(f"Unable to read database: {error}")
    st.stop()


column1, column2, column3, column4 = st.columns(4)

column1.metric("Students", student_count)
column2.metric("Courses", course_count)
column3.metric("Enrollments", enrollment_count)
column4.metric(
    "Average mark",
    f"{average_mark:.2f}" if average_mark is not None else "—"
)

st.write("")


# Example questions
st.subheader("Try a question")

examples = [
    ("All students", "show all students"),
    ("Highest marks", "show the 3 highest marks"),
    ("Course averages", "find the average marks for each course"),
    ("Department totals", "count students in each department"),
]

example_columns = st.columns(4)

for column, (label, example_question) in zip(
    example_columns, examples
):
    column.button(
        label,
        on_click=choose_example,
        args=(example_question,)
    )

st.caption(
    "Click an example, or type your own supported question below. "
    "Then click Run query."
)


# Question form
with st.form("query_form"):
    question = st.text_input(
        "Enter your question",
        key="question",
        placeholder="Show students with marks above 80"
    )

    submitted = st.form_submit_button(
        "Run query",
        type="primary"
    )


# Process the question
if submitted:
    st.session_state.pop("result", None)

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        query = get_query(question.strip())

        if query is None:
            st.warning(
                "This question is not supported yet. "
                "Open Supported questions below to see examples."
            )
        else:
            sql, parameters = query

            try:
                with closing(connect_database()) as connection:
                    cursor = connection.execute(sql, parameters)
                    rows = cursor.fetchall()

                    columns = [
                        item[0] for item in cursor.description
                    ]

                st.session_state["result"] = {
                    "question": question.strip(),
                    "sql": sql.strip(),
                    "parameters": parameters,
                    "data": pd.DataFrame(rows, columns=columns)
                }

            except sqlite3.Error as error:
                st.error(f"Database error: {error}")


# Display results
if "result" in st.session_state:
    result = st.session_state["result"]
    data = result["data"]

    st.divider()

    st.subheader("Query results")
    st.caption(f"Question: {result['question']}")

    results_tab, sql_tab = st.tabs(
        ["Results", "SQL query"]
    )

    with results_tab:
        if data.empty:
            st.info("No matching records found.")
        else:
            st.caption(f"Rows returned: {len(data)}")

            st.dataframe(
                data,
                hide_index=True
            )

            st.download_button(
                label="Download CSV",
                data=data.to_csv(index=False).encode("utf-8"),
                file_name="query_results.csv",
                mime="text/csv"
            )

    with sql_tab:
        st.code(result["sql"], language="sql")

        if result["parameters"]:
            st.write(
                "Parameters:",
                list(result["parameters"])
            )
        else:
            st.caption("No parameters required.")


# Supported questions
with st.expander("Supported questions"):
    st.markdown("""
- Show all students
- Show all courses
- Count students
- Show students with marks above 80
- Show students from the AI department
- Show the highest mark
- What is the average mark?
- Sort students by name
- Count students in each department
- Show the 3 highest marks
- Find the average marks for each course
    """)

    st.caption(
        "You can change the marks threshold, "
        "the number of highest marks and the department name."
    )


# Footer
st.divider()
st.caption(
    "Made by Sakshi Bohra and Anya Maurya • "
    "Semester 3 • DBMS Mini Project"
)
