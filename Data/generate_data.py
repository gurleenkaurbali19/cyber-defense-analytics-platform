import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# ----------------------------
# Helper
# ----------------------------
def random_dates(start, end, n):
    return [start + timedelta(days=random.randint(0, (end-start).days)) for _ in range(n)]

# ----------------------------
# FALCON DATA
# ----------------------------
def generate_falcon_data(start, end, rows):
    return pd.DataFrame({
        "hostname": [fake.hostname() for _ in range(rows)],
        "username": [fake.user_name() for _ in range(rows)],
        "severity_name": np.random.choice(["High", "Medium", "Low"], rows, p=[0.3,0.5,0.2]),
        "status": np.random.choice(["open","closed","in_progress"], rows),
        "first_detect": random_dates(start, end, rows),
        "first_assign": random_dates(start, end, rows),
        "resolved_time": random_dates(start, end, rows),
        "tactic": np.random.choice(["Execution","Persistence","Privilege Escalation"], rows),
        "resolution": np.random.choice(["TRUE_POSITIVE","FALSE_POSITIVE"], rows)
    })

# ----------------------------
# CYBLE DATA
# ----------------------------
def generate_cyble_data(start, end, rows):
    return pd.DataFrame({
        "data_source": np.random.choice(["dark_web","forum","leak_db"], rows),
        "record_date": random_dates(start, end, rows),
        "alert_severity": np.random.choice(["HIGH","MEDIUM","LOW"], rows),
        "alert_id": [fake.uuid4() for _ in range(rows)],
        "alert_generated_date": random_dates(start, end, rows),
        "alert_status": np.random.choice(["OPEN","RESOLVED"], rows),
        "keyword": np.random.choice(["ransomware","leak","credentials","phishing"], rows)
    })

# ----------------------------
# SIEM DATA
# ----------------------------
def generate_siem_data(start, end, rows):
    return pd.DataFrame({
        "alert_type": np.random.choice(["Malware","Credential Theft","Policy Violation"], rows),
        "severity": np.random.choice(["Critical","Major","Minor"], rows),
        "alert_time": random_dates(start, end, rows),
        "validation_status": np.random.choice(["TRUE_POSITIVE","FALSE_POSITIVE"], rows)
    })

# ----------------------------
# TREND VISION DATA
# ----------------------------
def generate_trend_data(start, end, rows):
    return pd.DataFrame({
        "detected": random_dates(start, end, rows),
        "threat_type": np.random.choice(["Spam","Phishing","Malware"], rows),
        "security_filter": np.random.choice(["Advanced Spam","Malware Scan"], rows),
        "protection_mode": np.random.choice(["INLINE","API"], rows),
        "affected_user": [fake.email() for _ in range(rows)],
        "sender": [fake.email() for _ in range(rows)],
        "recipient": [fake.email() for _ in range(rows)],
        "status": np.random.choice(["Quarantined","Delivered"], rows)
    })

# ----------------------------
# COM OLHO DATA
# ----------------------------
def generate_comolho_data(start, end, rows):
    return pd.DataFrame({
        "submission_date": random_dates(start, end, rows),
        "technical_severity": np.random.choice(["High (P2)","Medium (P3)","Low (P4)"], rows),
        "status": np.random.choice(["Open Vulnerability","Closed"], rows),
        "sla_status": np.random.choice(["On Time","Breached"], rows),
        "age_of_vulnerability_days": np.random.randint(1,30,rows),
        "vulnerability_type": np.random.choice(["dos_attack","phishing","xss"], rows),
        "reward_amount": np.random.randint(0,5000,rows),
        "report_status": np.random.choice(["Triaged","Reviewed"], rows)
    })

# ----------------------------
# NETSKOPE DATA
# ----------------------------
def generate_netskope_data(rows):
    return pd.DataFrame({
        "hostname": [fake.hostname() for _ in range(rows)],
        "os_platform": np.random.choice(["Windows","Linux"], rows),
        "user": [fake.email() for _ in range(rows)],
        "internet_security_status": np.random.choice(["Enabled","Disabled"], rows),
        "last_event": np.random.choice(["Tunnel Up","Tunnel Down"], rows)
    })

# ----------------------------
# GENERATE FILES
# ----------------------------
def generate_all():
    ranges = [
        ("jan", datetime(2025,1,1), datetime(2025,1,31)),
        ("feb", datetime(2025,2,1), datetime(2025,2,28))
    ]

    for name, start, end in ranges:
        generate_falcon_data(start,end,200).to_excel(f"falcon_{name}.xlsx", index=False)
        generate_cyble_data(start,end,150).to_excel(f"cyble_{name}.xlsx", index=False)
        generate_siem_data(start,end,180).to_excel(f"siem_{name}.xlsx", index=False)
        generate_trend_data(start,end,150).to_excel(f"trend_{name}.xlsx", index=False)
        generate_comolho_data(start,end,120).to_excel(f"comolho_{name}.xlsx", index=False)
        generate_netskope_data(50).to_excel(f"netskope_{name}.xlsx", index=False)

    print("All dummy Excel files generated!")

generate_all()
