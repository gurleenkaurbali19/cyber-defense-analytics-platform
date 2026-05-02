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


def get_kpi_date_range(df, date_column='ingestion_timestamp'):
    if df.empty or date_column not in df.columns:
        today = date.today()
        return today, today

    dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
    if dates.empty:
        today = date.today()
        return today, today

    return dates.min().date(), dates.max().date()


# ------------------ FETCH ------------------

def get_netskope_data(upload_id):
    conn = get_connection()

    query = "SELECT * FROM raw_netskope WHERE upload_id = %s"
    df = pd.read_sql(query, conn, params=[upload_id])

    conn.close()
    return df


# ------------------ KPI COMPUTATION ------------------

def compute_netskope_kpis(upload_id):
    df = get_netskope_data(upload_id)

    if df.empty:
        return []

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # Total devices
    kpis.append({
        "tool_name": "NETSKOPE",
        "kpi_name": "Total Devices",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # By OS
    for os_type, count in df['os_platform'].value_counts().items():
        kpis.append({
            "tool_name": "NETSKOPE",
            "kpi_name": "Devices",
            "kpi_value": safe_float(count),
            "kpi_dimension": "os_platform",
            "dimension_value": str(os_type),
            "start_date": start_date,
            "end_date": end_date
        })

    # Security status
    for sec, count in df['internet_security_status'].value_counts().items():
        kpis.append({
            "tool_name": "NETSKOPE",
            "kpi_name": "Security Status",
            "kpi_value": safe_float(count),
            "kpi_dimension": "internet_security_status",
            "dimension_value": str(sec),
            "start_date": start_date,
            "end_date": end_date
        })

    # Tunnel status
    for event, count in df['last_event'].value_counts().items():
        kpis.append({
            "tool_name": "NETSKOPE",
            "kpi_name": "Tunnel Status",
            "kpi_value": safe_float(count),
            "kpi_dimension": "last_event",
            "dimension_value": str(event),
            "start_date": start_date,
            "end_date": end_date
        })

    return kpis
