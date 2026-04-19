from kafka import KafkaProducer
import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="OASIS"
)

cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT * FROM submissions")

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)

for row in cursor.fetchall():
    producer.send('submission_topic', row)

producer.flush()
print("✅ Data sent to Kafka")