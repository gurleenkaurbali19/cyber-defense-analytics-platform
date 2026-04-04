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
