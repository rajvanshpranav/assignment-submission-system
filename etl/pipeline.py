import pandas as pd
from utils.db_connection import get_connection

def extract():
    conn = get_connection()
    
    query = """
    SELECT s.submission_id, s.student_id, s.assignment_id,
           s.submission_time, a.deadline
    FROM submissions s
    JOIN assignments a ON s.assignment_id = a.assignment_id
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    return df


def transform(df):
    df['submission_time'] = pd.to_datetime(df['submission_time'])
    df['deadline'] = pd.to_datetime(df['deadline'])

    df['submission_delay_minutes'] = (
        (df['submission_time'] - df['deadline'])
        .dt.total_seconds() / 60
    )

    df['is_late'] = df['submission_delay_minutes'].apply(
        lambda x: 1 if x > 0 else 0
    )

    return df


def load_processed(df):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM processed_submissions")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO processed_submissions (
                submission_id, student_id, assignment_id,
                submission_time, deadline,
                submission_delay_minutes, is_late
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row['submission_id'],
            row['student_id'],
            row['assignment_id'],
            row['submission_time'],
            row['deadline'],
            int(row['submission_delay_minutes']),
            int(row['is_late'])
        ))

    conn.commit()
    conn.close()


def load_daily_summary(df):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM daily_submission_summary")

    df['date'] = df['submission_time'].dt.date

    summary = df.groupby('date').agg(
        total_submissions=('submission_id', 'count'),
        late_submissions=('is_late', 'sum')
    ).reset_index()

    summary['on_time_submissions'] = (
        summary['total_submissions'] - summary['late_submissions']
    )

    summary['late_percentage'] = (
        summary['late_submissions'] / summary['total_submissions'] * 100
    )

    for _, row in summary.iterrows():
        cursor.execute("""
            INSERT INTO daily_submission_summary (
                date, total_submissions,
                on_time_submissions, late_submissions, late_percentage
            )
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['date'],
            int(row['total_submissions']),
            int(row['on_time_submissions']),
            int(row['late_submissions']),
            float(row['late_percentage'])
        ))

    conn.commit()
    conn.close()


def run_pipeline():
    df = extract()
    df = transform(df)
    
    load_processed(df)
    load_daily_summary(df)
    
    print("✅ ETL Pipeline executed successfully!")


if __name__ == "__main__":
    run_pipeline()