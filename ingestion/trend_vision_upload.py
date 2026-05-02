import pandas as pd
from Database.database_connection import get_connection


def upload_trend_vision(file, upload_id):
    """
    Reads Trend Vision Excel file and inserts into raw_trend_vision
    """

    df = pd.read_excel(file)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO raw_trend_vision (
        upload_id,
        detected,
        threat_type,
        security_filter,
        protection_mode,
        affected_user,
        sender,
        recipient,
        status
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            upload_id,
            pd.to_datetime(row.get("detected"), errors="coerce"),
            row.get("threat_type"),
            row.get("security_filter"),
            row.get("protection_mode"),
            row.get("affected_user"),
            row.get("sender"),
            row.get("recipient"),
            row.get("status"),
        )

        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
