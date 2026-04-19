# Assignment Submission System

## 📌 Overview
A real-time assignment submission system using:
- Kafka (streaming)
- MySQL (database)
- Streamlit (dashboard)

## 🚀 Features
- User login (admin + student)
- Real-time submission via Kafka
- Dashboard to track submissions
- Status update (on-time / late)

## 🛠️ Tech Stack
- Python
- Apache Kafka
- MySQL
- Streamlit

## ▶️ How to Run

### 1. Start Zookeeper
bin\windows\zookeeper-server-start.bat config\zookeeper.properties

### 2. Start Kafka
bin\windows\kafka-server-start.bat config\server.properties

### 3. Run Consumer
python streaming/consumer.py

### 4. Run Producer
python streaming/producer.py

### 5. Run Dashboard
streamlit run dashboard.py

## 📊 Project Structure
