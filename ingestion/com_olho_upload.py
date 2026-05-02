import pandas as pd
from Database.database_connection import get_connection


def upload_com_olho(file, upload_id):
    """
    Reads Com Olho Excel file and inserts into raw_com_olho
    """

    df = pd.read_excel(file)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO raw_com_olho (
        upload_id,
        submission_date,
        technical_severity,
        status,
        sla_status,
        age_of_vulnerability_days,
        vulnerability_type,
        reward_amount,
        report_status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            upload_id,
            pd.to_datetime(row.get("submission_date"), errors="coerce"),
            row.get("technical_severity"),
            row.get("status"),
            row.get("sla_status"),
            row.get("age_of_vulnerability_days"),
            row.get("vulnerability_type"),
            row.get("reward_amount"),
            row.get("report_status"),
        )

        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
