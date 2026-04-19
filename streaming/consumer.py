from kafka import KafkaConsumer
import json
import mysql.connector

# -------------------------------
# DB CONNECTION
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="OASIS"
)
cursor = conn.cursor()

# -------------------------------
# KAFKA CONSUMER
# -------------------------------
consumer = KafkaConsumer(
    'submission_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: x.decode('utf-8')   # SAFE
)

print("🚀 Listening and inserting into MySQL...")

for msg in consumer:
    raw = msg.value

    try:
        # Parse JSON safely
        data = json.loads(raw)

        # Insert query
        query = """
        INSERT INTO submissions 
        (student_id, assignment_id, file_path, submission_time, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            data.get('student_id'),
            data.get('assignment_id', 1),  # default if missing
            data.get('file_path'),
            data.get('submission_time'),
            data.get('status'),
            data.get('created_at')
        )

        cursor.execute(query, values)
        conn.commit()

        print("✅ Inserted:", data)

    except Exception as e:
        print("⚠️ Skipped invalid message:", raw)
        print("Error:", e)