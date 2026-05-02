import pandas as pd
from Database.database_connection import get_connection


def upload_netskope(file, upload_id):
    """
    Reads Netskope Excel file and inserts into raw_netskope
    """

    df = pd.read_excel(file)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO raw_netskope (
        upload_id,
        hostname,
        os_platform,
        user,
        internet_security_status,
        last_event
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            upload_id,
            row.get("hostname"),
            row.get("os_platform"),
            row.get("user"),
            row.get("internet_security_status"),
            row.get("last_event"),
        )

        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
