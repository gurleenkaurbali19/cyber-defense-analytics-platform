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

    # ------------------ DATA CLEANING ------------------

    df['status'] = df['status'].astype(str).str.upper()
    df['severity_name'] = df['severity_name'].astype(str).str.upper()
    df['resolution'] = df['resolution'].astype(str)

    df['first_detect'] = pd.to_datetime(df['first_detect'], errors='coerce')
    df['resolved_time'] = pd.to_datetime(df['resolved_time'], errors='coerce')
    df['first_assign'] = pd.to_datetime(df['first_assign'], errors='coerce')

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # ------------------ BASIC KPIs ------------------

    # Total Alerts
    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "Total Alerts",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # Alerts by Severity
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

    # Alerts by Status
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

    # Alerts by Resolution
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

    # ------------------ ADVANCED KPIs ------------------

    # 🔹 Daily Alerts Trend
    df_valid = df.dropna(subset=['first_detect'])
    trend = df_valid.groupby(df_valid['first_detect'].dt.date).size()

    for date_val, count in trend.items():
        kpis.append({
            "tool_name": "FALCON",
            "kpi_name": "Daily Alerts",
            "kpi_value": safe_float(count),
            "kpi_dimension": "date",
            "dimension_value": str(date_val),
            "start_date": start_date,
            "end_date": end_date
        })

    # 🔹 Open Alerts
    open_count = len(df[df['status'] == 'OPEN'])

    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "Open Alerts",
        "kpi_value": safe_float(open_count),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # 🔹 MTTR (Hours)
    resolved_df = df.dropna(subset=['resolved_time', 'first_detect'])

    if not resolved_df.empty:
        mttr = (
            (resolved_df['resolved_time'] - resolved_df['first_detect'])
            .dt.total_seconds()
            .mean()
        ) / 3600
    else:
        mttr = 0

    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "MTTR (Hours)",
        "kpi_value": safe_float(mttr),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # 🔹 Assigned & Resolved Counts
    assigned_count = df['first_assign'].notna().sum() if 'first_assign' in df.columns else 0
    resolved_count = df['resolved_time'].notna().sum() if 'resolved_time' in df.columns else 0

    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "Assigned Alerts",
        "kpi_value": safe_float(assigned_count),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "Resolved Alerts",
        "kpi_value": safe_float(resolved_count),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # 🔹 Resolution Rate
    resolution_rate = (resolved_count / len(df)) if len(df) != 0 else 0

    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "Resolution Rate",
        "kpi_value": safe_float(resolution_rate),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # 🔹 High Severity Alerts
    high_sev_count = len(df[df['severity_name'] == 'HIGH'])

    kpis.append({
        "tool_name": "FALCON",
        "kpi_name": "High Severity Alerts",
        "kpi_value": safe_float(high_sev_count),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    return kpis
