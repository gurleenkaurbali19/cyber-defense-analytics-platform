import pandas as pd
from Database.database_connection import get_connection


def upload_siem(file, upload_id):
    """
    Reads SIEM Excel file and inserts data into raw_siem table
    """

    df = pd.read_excel(file)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO raw_siem (
        upload_id,
        alert_type,
        severity,
        alert_time,
        validation_status
    )
    VALUES (%s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            upload_id,
            str(row.get("alert_type")).strip(),
            str(row.get("severity")).strip(),
            pd.to_datetime(row.get("alert_time"), errors="coerce"),
            str(row.get("validation_status")).strip(),
        )

        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
