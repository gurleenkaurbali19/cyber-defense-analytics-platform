import pandas as pd
from Database.database_connection import get_connection


def upload_cyble(file, upload_id):
    """
    Reads Cyble Excel file and inserts data into raw_cyble table
    """

    df = pd.read_excel(file)

    # Standardize column names
    df.columns = [col.strip().lower() for col in df.columns]

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO raw_cyble (
        upload_id,
        data_source,
        record_date,
        alert_severity,
        alert_id,
        alert_generated_date,
        alert_status,
        keyword
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            upload_id,
            row.get("data_source"),
            pd.to_datetime(row.get("record_date"), errors="coerce"),
            row.get("alert_severity"),
            row.get("alert_id"),
            pd.to_datetime(row.get("alert_generated_date"), errors="coerce"),
            row.get("alert_status"),
            row.get("keyword"),
        )

        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
