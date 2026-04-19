import streamlit as st
import pandas as pd
import mysql.connector

# -------------------------------
# 🔌 DB CONNECTION
# -------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2003",
    database="OASIS"
)
cursor = conn.cursor()

# -------------------------------
# 🎨 PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Assignment Portal", layout="wide")

# -------------------------------
# 🧠 SESSION INIT
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# -------------------------------
# 🔐 LOGIN
# -------------------------------
def login():
    st.title("🔐 Assignment Portal Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.session_state.user_id = user[0]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------------------------------
# 🎨 STATUS COLOR FUNCTION
# -------------------------------
def status_badge(status):
    if status == "on-time":
        return "🟢 On-Time"
    elif status == "late":
        return "🔴 Late"
    else:
        return status

# -------------------------------
# 📊 DASHBOARD
# -------------------------------
def dashboard():

    st.title("📊 Assignment Submission System")

    # Sidebar
    st.sidebar.title(f"👋 {st.session_state.username}")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Submit (Student)", "Logout"])

    # Load data
    df = pd.read_sql("SELECT * FROM submissions ORDER BY created_at DESC", conn)
    df['file_name'] = df['file_path'].apply(lambda x: x.split('/')[-1])

    # -------------------------------
    # 🏠 DASHBOARD VIEW
    # -------------------------------
    if menu == "Dashboard":

        if st.session_state.role == "admin":
            st.subheader("👑 Admin View")

        else:
            st.subheader("👨‍🎓 My Submissions")
            df = df[df['student_id'] == st.session_state.user_id]

        # KPI
        col1, col2 = st.columns(2)
        col1.metric("On-Time", len(df[df['status']=="on-time"]))
        col2.metric("Late", len(df[df['status']=="late"]))

        # Clean display
        display_df = df.copy()
        display_df['status'] = display_df['status'].apply(status_badge)
        display_df = display_df.drop(columns=['file_path'])
        display_df = display_df.rename(columns={'file_name': 'File Name'})

        st.dataframe(display_df, use_container_width=True)

        # -------------------------------
        # ✏️ ADMIN UPDATE SECTION
        # -------------------------------
        if st.session_state.role == "admin":
            st.markdown("---")
            st.subheader("✏️ Update Status")

            selected_file = st.selectbox("Select Submission", df['file_name'])
            selected_row = df[df['file_name'] == selected_file].iloc[0]

            new_status = st.radio(
                "Change Status",
                ["on-time", "late"],
                index=["on-time", "late"].index(selected_row['status'])
            )

            if st.button("Update Status"):
                cursor.execute(
                    "UPDATE submissions SET status=%s WHERE submission_id=%s",
                    (new_status, int(selected_row['submission_id']))
                )
                conn.commit()
                st.success("Updated successfully")

    # -------------------------------
    # 📤 STUDENT SUBMISSION
    # -------------------------------
    elif menu == "Submit (Student)":

        if st.session_state.role != "student":
            st.warning("Only students can submit assignments")
            return

        st.subheader("📤 Submit Assignment")

        file_name = st.text_input("Enter File Name (example.pdf)")

        if st.button("Submit"):
            if file_name.strip() == "":
                st.error("File name cannot be empty")
            else:
                status = "on-time"

                cursor.execute("""
                    INSERT INTO submissions
                    (student_id, file_path, submission_time, status, created_at)
                    VALUES (%s, %s, NOW(), %s, NOW())
                """, (
                    st.session_state.user_id,
                    f"/data/raw/{file_name}",
                    status
                ))

                conn.commit()
                st.success("✅ Assignment submitted!")

    # -------------------------------
    # 🚪 LOGOUT
    # -------------------------------
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.rerun()

# -------------------------------
# 🚀 MAIN
# -------------------------------
if st.session_state.logged_in:
    dashboard()
else:
    login()