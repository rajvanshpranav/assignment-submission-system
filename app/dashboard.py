import streamlit as st
import pandas as pd
from utils.db_connection import get_connection

st.set_page_config(page_title="Assignment Dashboard", layout="wide")

st.title("📊 Online Assignment Submission Dashboard")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    conn = get_connection()
    
    processed = pd.read_sql("SELECT * FROM processed_submissions", conn)
    daily = pd.read_sql("SELECT * FROM daily_submission_summary", conn)
    student = pd.read_sql("SELECT * FROM student_activity_summary", conn)
    
    conn.close()
    return processed, daily, student

processed, daily, student = load_data()

# -----------------------------
# Overview Metrics
# -----------------------------
st.subheader("📈 Overview")

col1, col2, col3 = st.columns(3)

total = len(processed)
late = processed['is_late'].sum()
on_time = total - late

col1.metric("Total Submissions", total)
col2.metric("Late Submissions", int(late))
col3.metric("On-Time Submissions", int(on_time))

# -----------------------------
# Daily Trends
# -----------------------------
st.subheader("📅 Daily Submission Trends")

if not daily.empty:
    st.line_chart(daily.set_index('date')['total_submissions'])

# -----------------------------
# Late vs On-time
# -----------------------------
st.subheader("⏱️ Submission Behavior")

behavior_df = pd.DataFrame({
    'Type': ['On-Time', 'Late'],
    'Count': [on_time, late]
})

st.bar_chart(behavior_df.set_index('Type'))

# -----------------------------
# Student Activity
# -----------------------------
st.subheader("👤 Student Activity")

if not student.empty:
    st.dataframe(student)

# -----------------------------
# Processed Data
# -----------------------------
st.subheader("📂 Processed Submissions")

st.dataframe(processed)