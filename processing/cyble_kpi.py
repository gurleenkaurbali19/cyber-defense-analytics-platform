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


def get_kpi_date_range(df, date_column='record_date'):
    if df.empty or date_column not in df.columns:
        today = date.today()
        return today, today

    dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
    if dates.empty:
        today = date.today()
        return today, today

    return dates.min().date(), dates.max().date()


# ------------------ FETCH DATA ------------------

def get_cyble_data(upload_id):
    conn = get_connection()

    query = "SELECT * FROM raw_cyble WHERE upload_id = %s"
    df = pd.read_sql(query, conn, params=[upload_id])

    conn.close()
    return df


# ------------------ KPI COMPUTATION ------------------

def compute_cyble_kpis(upload_id):
    df = get_cyble_data(upload_id)

    if df.empty:
        return []

    # Standardize (important for consistency)
    df['alert_severity'] = df['alert_severity'].str.upper()
    df['alert_status'] = df['alert_status'].str.upper()
    df['data_source'] = df['data_source'].str.lower()
    df['keyword'] = df['keyword'].str.lower()

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # ------------------ BASIC KPIs ------------------

    kpis.append({
        "tool_name": "CYBLE",
        "kpi_name": "Total Alerts",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # Severity
    for severity, count in df['alert_severity'].value_counts().items():
        kpis.append({
            "tool_name": "CYBLE",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "severity",
            "dimension_value": str(severity),
            "start_date": start_date,
            "end_date": end_date
        })

    # Status
    for status, count in df['alert_status'].value_counts().items():
        kpis.append({
            "tool_name": "CYBLE",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "status",
            "dimension_value": str(status),
            "start_date": start_date,
            "end_date": end_date
        })

    # Source
    for source, count in df['data_source'].value_counts().items():
        kpis.append({
            "tool_name": "CYBLE",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "source",
            "dimension_value": str(source),
            "start_date": start_date,
            "end_date": end_date
        })

    # Keyword
    for keyword, count in df['keyword'].value_counts().items():
        kpis.append({
            "tool_name": "CYBLE",
            "kpi_name": "Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "keyword",
            "dimension_value": str(keyword),
            "start_date": start_date,
            "end_date": end_date
        })

    # ------------------ ADVANCED KPIs ------------------

    # 🔹 Daily Trend
    df['record_date'] = pd.to_datetime(df['record_date'], errors='coerce')
    df_valid = df.dropna(subset=['record_date'])

    trend = df_valid.groupby(df_valid['record_date'].dt.date).size()

    for date_val, count in trend.items():
        kpis.append({
            "tool_name": "CYBLE",
            "kpi_name": "Daily Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "date",
            "dimension_value": str(date_val),
            "start_date": start_date,
            "end_date": end_date
        })

    # 🔹 Open vs Resolved Ratio
    open_count = len(df[df['alert_status'] == 'OPEN'])
    resolved_count = len(df[df['alert_status'] == 'RESOLVED'])

    ratio = (open_count / resolved_count) if resolved_count != 0 else 0

    kpis.append({
        "tool_name": "CYBLE",
        "kpi_name": "Open/Resolved Ratio",
        "kpi_value": safe_float(ratio),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    return kpis
