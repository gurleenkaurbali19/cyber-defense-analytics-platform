import pandas as pd
from Database.database_connection import get_connection


def upload_falcon(file, upload_id):
    """
    Reads Falcon Excel file and inserts data into raw_falcon table
    """

    # Read file (Streamlit file object)
    df = pd.read_excel(file)

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO raw_falcon (
        upload_id,
        hostname,
        username,
        severity_name,
        status,
        first_detect,
        first_assign,
        resolved_time,
        tactic,
        resolution
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        values = (
            upload_id,
            row.get("hostname"),
            row.get("username"),
            row.get("severity_name"),
            row.get("status"),
            pd.to_datetime(row.get("first_detect"), errors="coerce"),
            pd.to_datetime(row.get("first_assign"), errors="coerce"),
            pd.to_datetime(row.get("resolved_time"), errors="coerce"),
            row.get("tactic"),
            row.get("resolution"),
        )

        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
