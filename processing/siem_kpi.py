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


def get_kpi_date_range(df, date_column='alert_time'):
    if df.empty or date_column not in df.columns:
        today = date.today()
        return today, today

    dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
    if dates.empty:
        today = date.today()
        return today, today

    return dates.min().date(), dates.max().date()


# ------------------ FETCH ------------------

def get_siem_data(upload_id):
    conn = get_connection()

    query = "SELECT * FROM raw_siem WHERE upload_id = %s"
    df = pd.read_sql(query, conn, params=[upload_id])

    conn.close()
    return df


# ------------------ KPI COMPUTATION ------------------

def compute_siem_kpis(upload_id):
    df = get_siem_data(upload_id)

    if df.empty:
        return []

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # Total alerts
    kpis.append({
        "tool_name": "SIEM",
        "kpi_name": "Total Alerts",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # Alerts by severity
    for severity, count in df['severity'].value_counts().items():
        kpis.append({
            "tool_name": "SIEM",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "severity",
            "dimension_value": str(severity),
            "start_date": start_date,
            "end_date": end_date
        })

    # Alerts by alert type
    for alert_type, count in df['alert_type'].value_counts().items():
        kpis.append({
            "tool_name": "SIEM",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "alert_type",
            "dimension_value": str(alert_type),
            "start_date": start_date,
            "end_date": end_date
        })

    # Alerts by validation status
    for status, count in df['validation_status'].value_counts().items():
        kpis.append({
            "tool_name": "SIEM",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "validation_status",
            "dimension_value": str(status),
            "start_date": start_date,
            "end_date": end_date
        })

    # True Positive vs False Positive
    if 'validation_status' in df.columns:
        tp = len(df[df['validation_status'] == 'TRUE_POSITIVE'])
        fp = len(df[df['validation_status'] == 'FALSE_POSITIVE'])

        kpis.append({
            "tool_name": "SIEM",
            "kpi_name": "True Positives",
            "kpi_value": safe_float(tp),
            "kpi_dimension": None,
            "dimension_value": None,
            "start_date": start_date,
            "end_date": end_date
        })

        kpis.append({
            "tool_name": "SIEM",
            "kpi_name": "False Positives",
            "kpi_value": safe_float(fp),
            "kpi_dimension": None,
            "dimension_value": None,
            "start_date": start_date,
            "end_date": end_date
        })

    return kpis
