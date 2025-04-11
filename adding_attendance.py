import pandas as pd
import mysql.connector

# Load the CSV file
df = pd.read_csv("student_performance_dataset.csv")

# Keep only Student_ID and Name columns
attendance_df = df[["Student_ID", "Name"]]

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="220905@Ig",
    database="students"
)
cursor = conn.cursor()

# Prepare SQL insert query
insert_query = """
INSERT INTO attendance (id, name) VALUES (%s, %s)
ON DUPLICATE KEY UPDATE name = VALUES(name)
"""

# Insert each row
for _, row in attendance_df.iterrows():
    cursor.execute(insert_query, (row["Student_ID"], row["Name"]))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("✅ Student_ID and Name inserted into 'attendance' table.")