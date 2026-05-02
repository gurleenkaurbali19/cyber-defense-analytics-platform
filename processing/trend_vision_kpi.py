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


def get_kpi_date_range(df, date_column='detected'):
    if df.empty or date_column not in df.columns:
        today = date.today()
        return today, today

    dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
    if dates.empty:
        today = date.today()
        return today, today

    return dates.min().date(), dates.max().date()


# ------------------ FETCH ------------------

def get_trend_data(upload_id):
    conn = get_connection()

    query = "SELECT * FROM raw_trend_vision WHERE upload_id = %s"
    df = pd.read_sql(query, conn, params=[upload_id])

    conn.close()
    return df


# ------------------ KPI COMPUTATION ------------------

def compute_trend_vision_kpis(upload_id):
    df = get_trend_data(upload_id)

    if df.empty:
        return []

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # Total threats
    kpis.append({
        "tool_name": "TREND_VISION",
        "kpi_name": "Total Threats",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # Threats by type
    for ttype, count in df['threat_type'].value_counts().items():
        kpis.append({
            "tool_name": "TREND_VISION",
            "kpi_name": "Threats",
            "kpi_value": safe_float(count),
            "kpi_dimension": "threat_type",
            "dimension_value": str(ttype),
            "start_date": start_date,
            "end_date": end_date
        })

    # By status (Delivered vs Quarantined)
    for status, count in df['status'].value_counts().items():
        kpis.append({
            "tool_name": "TREND_VISION",
            "kpi_name": "Threats",
            "kpi_value": safe_float(count),
            "kpi_dimension": "status",
            "dimension_value": str(status),
            "start_date": start_date,
            "end_date": end_date
        })

    # By protection mode (API / INLINE)
    for mode, count in df['protection_mode'].value_counts().items():
        kpis.append({
            "tool_name": "TREND_VISION",
            "kpi_name": "Threats",
            "kpi_value": safe_float(count),
            "kpi_dimension": "protection_mode",
            "dimension_value": str(mode),
            "start_date": start_date,
            "end_date": end_date
        })

    # By security filter
    for filt, count in df['security_filter'].value_counts().items():
        kpis.append({
            "tool_name": "TREND_VISION",
            "kpi_name": "Threats",
            "kpi_value": safe_float(count),
            "kpi_dimension": "security_filter",
            "dimension_value": str(filt),
            "start_date": start_date,
            "end_date": end_date
        })

    return kpis
