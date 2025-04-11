import pandas as pd
import mysql.connector

# Load CSV
df = pd.read_csv("student_performance_dataset.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="220905@Ig",
    database="students"
)
cursor = conn.cursor()

# Prepare SQL INSERT query
insert_query = """
INSERT INTO details (
    Student_ID, Name, Gender, Age, Attendance_Percent,
    Test1_Score, Test2_Score, Assignment_Score, Study_Hours_Per_Week,
    Parent_Education, Internet_Access, Extra_Coaching, Behavior_Rating,
    Participation, Absences, Final_Exam_Score, Final_Result
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Insert all rows
for _, row in df.iterrows():
    values = tuple(row)
    cursor.execute(insert_query, values)

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ All data inserted into 'details' table.")
