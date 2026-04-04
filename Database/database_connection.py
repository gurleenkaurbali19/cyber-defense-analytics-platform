import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def test_connection():
    conn = get_connection()
    if conn and conn.is_connected():
        print(f"Connected to {os.getenv('DB_NAME')} successfully!")
        conn.close()
    else:
        print("Connection failed")
