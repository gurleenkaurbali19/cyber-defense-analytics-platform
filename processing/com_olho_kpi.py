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


def get_kpi_date_range(df, date_column='submission_date'):
    if df.empty or date_column not in df.columns:
        today = date.today()
        return today, today

    dates = pd.to_datetime(df[date_column], errors='coerce').dropna()
    if dates.empty:
        today = date.today()
        return today, today

    return dates.min().date(), dates.max().date()


# ------------------ FETCH ------------------

def get_com_olho_data(upload_id):
    conn = get_connection()

    query = "SELECT * FROM raw_com_olho WHERE upload_id = %s"
    df = pd.read_sql(query, conn, params=[upload_id])

    conn.close()
    return df


# ------------------ KPI COMPUTATION ------------------

def compute_com_olho_kpis(upload_id):
    df = get_com_olho_data(upload_id)

    if df.empty:
        return []

    start_date, end_date = get_kpi_date_range(df)

    kpis = []

    # Total vulnerabilities
    kpis.append({
        "tool_name": "COM_OLHO",
        "kpi_name": "Total Vulnerabilities",
        "kpi_value": safe_float(len(df)),
        "kpi_dimension": None,
        "dimension_value": None,
        "start_date": start_date,
        "end_date": end_date
    })

    # By severity
    for sev, count in df['technical_severity'].value_counts().items():
        kpis.append({
            "tool_name": "COM_OLHO",
            "kpi_name": "Vulnerabilities",
            "kpi_value": safe_float(count),
            "kpi_dimension": "severity",
            "dimension_value": str(sev),
            "start_date": start_date,
            "end_date": end_date
        })

    # By vulnerability type
    for vtype, count in df['vulnerability_type'].value_counts().items():
        kpis.append({
            "tool_name": "COM_OLHO",
            "kpi_name": "Vulnerabilities",
            "kpi_value": safe_float(count),
            "kpi_dimension": "vulnerability_type",
            "dimension_value": str(vtype),
            "start_date": start_date,
            "end_date": end_date
        })

    # SLA performance
    for sla, count in df['sla_status'].value_counts().items():
        kpis.append({
            "tool_name": "COM_OLHO",
            "kpi_name": "SLA Status",
            "kpi_value": safe_float(count),
            "kpi_dimension": "sla_status",
            "dimension_value": str(sla),
            "start_date": start_date,
            "end_date": end_date
        })

    # Open vs Closed
    for status, count in df['status'].value_counts().items():
        kpis.append({
            "tool_name": "COM_OLHO",
            "kpi_name": "Vulnerability Status",
            "kpi_value": safe_float(count),
            "kpi_dimension": "status",
            "dimension_value": str(status),
            "start_date": start_date,
            "end_date": end_date
        })

    # Average age of vulnerabilities
    if 'age_of_vulnerability_days' in df.columns:
        avg_age = df['age_of_vulnerability_days'].mean()

        kpis.append({
            "tool_name": "COM_OLHO",
            "kpi_name": "Average Vulnerability Age",
            "kpi_value": safe_float(avg_age),
            "kpi_dimension": None,
            "dimension_value": None,
            "start_date": start_date,
            "end_date": end_date
        })

    # Total reward payout
    if 'reward_amount' in df.columns:
        total_reward = df['reward_amount'].sum()

        kpis.append({
            "tool_name": "COM_OLHO",
            "kpi_name": "Total Reward Amount",
            "kpi_value": safe_float(total_reward),
            "kpi_dimension": None,
            "dimension_value": None,
            "start_date": start_date,
            "end_date": end_date
        })

    return kpis
