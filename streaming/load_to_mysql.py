import pandas as pd
import mysql.connector
import os

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="OASIS"
)

cursor = conn.cursor()

folder = "data/processed_stream/"

for file in os.listdir(folder):
    if file.endswith(".csv"):
        df = pd.read_csv(os.path.join(folder, file))

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO processed_submissions
                (submission_id, student_id, assignment_id, is_late)
                VALUES (%s, %s, %s, %s)
            """, (
                row['submission_id'],
                row['student_id'],
                row['assignment_id'],
                row['is_late']
            ))

conn.commit()
conn.close()

print("✅ Data loaded into MySQL")