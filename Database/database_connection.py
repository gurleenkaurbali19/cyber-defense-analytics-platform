import mysql.connector
from mysql.connector import Error
import os

def get_connection():
    try:
        import streamlit as st
        # Check if secrets are actually configured
        if "db" in st.secrets:
            connection = mysql.connector.connect(
                host=st.secrets["db"]["host"],
                user=st.secrets["db"]["user"],
                password=st.secrets["db"]["password"],
                database=st.secrets["db"]["database"],
                port=int(st.secrets["db"]["port"]),
                ssl_disabled=False
            )
        else:
            # Fallback to .env for local development
            from dotenv import load_dotenv
            load_dotenv()
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                port=int(os.getenv("DB_PORT")),
                ssl_disabled=False
            )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def test_connection():
    conn = get_connection()
    if conn and conn.is_connected():
        print("Connected successfully!")
        conn.close()
    else:
        print("Connection failed")