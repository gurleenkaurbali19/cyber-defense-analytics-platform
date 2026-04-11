import pandas as pd
from datetime import date
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database.database_connection import get_connection


# ------------------ HELPERS ------------------

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


def get_kpi_date_range(df, date_column='first_detect'):
    if df.empty or date_column not in df.columns:
        today = date.today()
        return today, today

    dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
    if dates.empty:
        today = date.today()
        return today, today

    return dates.min().date(), dates.max().date()


# ------------------ FETCH DATA ------------------

def get_falcon_data(upload_id):
    conn = get_connection()

    query = "SELECT * FROM raw_falcon WHERE upload_id = %s"
    df = pd.read_sql(query, conn, params=[upload_id])

    conn.close()
    return df


# ------------------ KPI COMPUTATION ------------------

def compute_falcon_kpis(upload_id):
    df = get_falcon_data(upload_id)

    if df.empty:
        return []

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # Total alerts
    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "Total Alerts",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # Alerts by severity
    for severity, count in df['severity_name'].value_counts().items():
        kpis.append({
            "tool_name": "FALCON",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "severity",
            "dimension_value": str(severity),
            "start_date": start_date,
            "end_date": end_date
        })

    # Alerts by status
    for status, count in df['status'].value_counts().items():
        kpis.append({
            "tool_name": "FALCON",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "status",
            "dimension_value": str(status),
            "start_date": start_date,
            "end_date": end_date
        })

    # Alerts by resolution
    for res, count in df['resolution'].value_counts().items():
        kpis.append({
            "tool_name": "FALCON",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "resolution",
            "dimension_value": str(res),
            "start_date": start_date,
            "end_date": end_date
        })

    return kpis
