import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.database_connection import get_connection


def check_file_exists(file_hash):
    """
    Returns upload_id if file exists, else None
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT upload_id FROM upload_master WHERE file_hash = %s"
    cursor.execute(query, (file_hash,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def insert_upload(tool_name, file_name, file_hash):
    """
    Inserts new upload record and returns upload_id
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO upload_master (tool_name, file_name, file_hash)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (tool_name, file_name, file_hash))
    conn.commit()

    upload_id = cursor.lastrowid

    conn.close()

    return upload_id


def update_processing_status(upload_id, status):
    """
    Updates processing status
    """
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE upload_master
    SET processing_status = %s
    WHERE upload_id = %s
    """

    cursor.execute(query, (status, upload_id))
    conn.commit()

    conn.close()


#Funtion to insert the computed KPIs in the KPI table
def insert_kpis(upload_id, kpis):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO kpi_master (
        upload_id, tool_name, kpi_name, kpi_value,
        kpi_dimension, dimension_value, start_date, end_date
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    for kpi in kpis:
        cursor.execute(query, (
            upload_id,
            kpi["tool_name"],
            kpi["kpi_name"],
            kpi["kpi_value"],
            kpi["kpi_dimension"],
            kpi["dimension_value"],
            kpi["start_date"],
            kpi["end_date"]
        ))

    conn.commit()
    conn.close()

def get_upload_ids_by_tool(tool_name):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT upload_id FROM upload_master WHERE tool_name = %s"
    cursor.execute(query, (tool_name,))

    results = cursor.fetchall()
    conn.close()

    return [row[0] for row in results]


def fetch_raw_falcon(upload_id):
    import pandas as pd

    conn = get_connection()
    query = "SELECT * FROM raw_falcon WHERE upload_id = %s"

    df = pd.read_sql(query, conn, params=[upload_id])
    conn.close()

    return df

def get_processing_status(upload_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT processing_status FROM upload_master WHERE upload_id = %s"
    cursor.execute(query, (upload_id,))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def fetch_kpis(upload_id):
    import pandas as pd

    conn = get_connection()
    query = "SELECT * FROM kpi_master WHERE upload_id = %s"

    df = pd.read_sql(query, conn, params=[upload_id])
    conn.close()

    return df
