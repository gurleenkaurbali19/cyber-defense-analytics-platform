<div align="center">

# 🛡️ CyberPulse
### Centralized Security Operations Analytics Platform

*Upload security exports → Compute KPIs → Explore executive dashboards*

[![Live Project](https://img.shields.io/badge/Live%20Project-CyberPulse-00ffff?style=for-the-badge&logo=streamlit&logoColor=white)](https://cyberrpulse.streamlit.app/)

</div>

---

## 📽️ Demo

### 🏠 Home & Info Page
![Home & Info](Demos/home_info.gif)

### 📤 Upload Pipeline
![Upload](Demos/upload.gif)

### ⚙️ KPI Computation
![Compute](Demos/compute.gif)

### 📊 Security Dashboard
![Dashboard](Demos/dashboard.gif)

---

## 🔍 Overview

**CyberPulse** is a full-stack security analytics platform built for SOC (Security Operations Center) teams. It centralizes data from **6 different cybersecurity tools** into a single reporting solution — eliminating the need to context-switch between platforms for security visibility.

The platform follows a clean 4-stage pipeline:

```
Upload Excel Export  →  Ingest to Raw Tables  →  Compute KPIs  →  Visualize Dashboard
```

> **Key design principle:** The dashboard reads **exclusively** from a single centralized `kpi_master` table — never from raw data tables. This keeps queries fast, the codebase clean, and the architecture scalable.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📁 **Multi-tool ingestion** | Upload Excel exports from 6 security platforms |
| 🔐 **Duplicate detection** | file hashing prevents re-processing |
| 🗄️ **Centralized KPI layer** | All metrics stored in a single `kpi_master` table |
| 📊 **Rich visualizations** | Donut charts, area trends, gauges, funnels, treemaps, bullet charts |
| 📅 **Date range filtering** | Filter all dashboards by any date window |
| 🧩 **Modular architecture** | Adding a new tool requires only 3 files |
| 📋 **Upload audit trail** | Every file tracked with full status lifecycle |
| 🔄 **Live KPI refresh** | Recompute and refresh metrics at any time |

---

## 🔐 Integrated Security Tools

| # | Tool | Category | Visualizations |
|---|---|---|---|
| 1 | 🛡️ **CrowdStrike Falcon** | EDR · Endpoint Detection | Severity donut, Status funnel, TP/FP donut, MTTR gauge, Daily trend |
| 2 | 🌐 **Cyble** | Threat Intel · Dark Web | Severity donut, Status bar, Sources treemap, Keywords bar, Daily trend |
| 3 | 🔒 **SIEM** | Security Event Management | Severity donut, Alert type bar, FP rate gauge, TP/FP bullet charts |
| 4 | 📧 **Trend Vision** | Email · Cloud Protection | Threat type donut, Delivery status donut, Protection mode bar, Quarantine gauge |
| 5 | 🔗 **Netskope** | Endpoint · Network Security | OS donut, Security status donut, Tunnel bar, Coverage gauge |
| 6 | 🛠️ **Com Olho** | Vuln Mgmt · Bug Bounty | Severity donut, SLA donut, Vuln type treemap, Breach gauge, Age bullet |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        STREAMLIT FRONTEND                         │
│                                                                    │
│   home.py    upload.py    compute.py    dashboard.py    info.py   │
└────────┬──────────┬───────────┬──────────────┬────────────────────┘
         │          │           │              │
         │    ┌─────▼──────┐   │    ┌─────────▼────────┐
         │    │tool_registry│  │    │    kpi_master     │
         │    │  (config)  │  │    │  (read only)      │
         │    └─────┬──────┘  │    └──────────────────-┘
         │          │          │              ▲
         │   ┌──────▼──────┐  │    ┌─────────┴──────────┐
         │   │ ingestion/  │  │    │    processing/      │
         │   │ *_upload.py │  │    │    *_kpi.py         │
         │   └──────┬──────┘  │    └────────────────────┘
         │          │          │              ▲
         │   ┌──────▼──────────▼──────────────┴──────────┐
         │   │                MySQL Database               │
         │   │  upload_master   (audit + deduplication)   │
         │   │  raw_falcon      (raw EDR data)             │
         │   │  raw_cyble       (raw threat intel)         │
         │   │  raw_siem        (raw SIEM events)          │
         │   │  raw_trend_vision(raw email threats)        │
         │   │  raw_netskope    (raw endpoint data)        │
         │   │  raw_com_olho    (raw vuln data)            │
         │   │  kpi_master      ← SINGLE SOURCE OF TRUTH  │
         │   └─────────────────────────────────────────────┘
         │
    hash_utils.py (deduplication)
    db_utils.py   (shared DB helpers)
```

### Why `kpi_master` as single source of truth?

Instead of running complex aggregation queries on raw tables every time the dashboard loads, all metrics are **pre-computed and stored** in `kpi_master`. The dashboard just reads from one table with simple filters — making it fast, consistent, and easy to extend.

---

## 🗄️ Database Design

Three logical layers:

### Layer 1 — Upload Tracking
**`upload_master`** tracks every uploaded file before any data is processed.

| Column | Type | Description |
|---|---|---|
| `upload_id` | INT PK AUTO | Unique identifier |
| `tool_name` | VARCHAR(50) | e.g. FALCON, CYBLE |
| `file_hash` | VARCHAR(64) | SHA-256 for deduplication |
| `processing_status` | VARCHAR(20) | `pending` → `processing` → `completed` / `failed` |

### Layer 2 — Raw Tables
One table per tool, stores original ingested data exactly as received (`raw_falcon`, `raw_cyble`, `raw_siem`, `raw_trend_vision`, `raw_netskope`, `raw_com_olho`).

### Layer 3 — KPI Master
**`kpi_master`** — the only table the dashboard reads from.

```
# Scalar KPI (no breakdown)
tool_name  kpi_name        kpi_value  kpi_dimension  dimension_value
FALCON     Total Alerts    200        (null)         (null)

# Dimension KPI (breakdown by category)
tool_name  kpi_name   kpi_value  kpi_dimension  dimension_value
FALCON     Alerts     92         severity       MEDIUM
FALCON     Alerts     63         severity       HIGH
```

---

## 🔄 Data Flow

```
User uploads Excel
       │
       ▼
SHA-256 hash check ──── DUPLICATE ──→ Reject + warn
       │ NEW
       ▼
Insert into upload_master (status = pending)
       │
       ▼
tool_registry maps tool → upload function
       │
       ▼
*_upload.py: reads Excel → cleans → inserts raw rows
       │
       ▼
User triggers KPI computation
       │
       ▼
*_kpi.py: reads raw table → calculates KPIs → returns KPI list
       │
       ▼
insert_kpis() → kpi_master (status = completed)
       │
       ▼
Dashboard: SELECT from kpi_master only (overlap date filter)
       │
       ▼
Plotly charts render in tabs
```

---

## 📂 Project Structure

```
cyberpulse/
│
├── app/
│   ├── app.py               # Entry point — navigation & routing
│   ├── home.py              # Landing page
│   ├── upload.py            # File upload & ingestion UI
│   ├── compute.py           # KPI computation UI
│   ├── dashboard.py         # Analytics dashboard
│   └── info.py              # Platform info & sample downloads
│
├── config/
│   └── tool_registry.py     # Maps tools → upload/KPI functions
│
├── Database/
│   ├── database_connection.py
│   ├── db_utils.py
│   └── security_dash.sql    # Full schema (DDL)
│
├── ingestion/               # One script per tool
│   ├── falcon_upload.py
│   ├── cyble_upload.py
│   ├── siem_upload.py
│   ├── trend_vision_upload.py
│   ├── netskope_upload.py
│   └── com_olho_upload.py
│
├── processing/              # One KPI script per tool
│   ├── falcon_kpi.py
│   ├── cyble_kpi.py
│   ├── siem_kpi.py
│   ├── trend_vision_kpi.py
│   ├── netskope_kpi.py
│   └── com_olho_kpi.py
│
├── utils/
│   └── hash_utils.py        # file hashing
│
├── Data/SampleFiles/        # Sample Excel files for testing
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | Streamlit | UI, navigation, page rendering |
| Charts | Plotly | Interactive visualizations |
| Data | Pandas | Excel parsing, data manipulation |
| Database | MySQL 8.0 | Persistent storage (hosted on Aiven) |
| DB Driver | mysql-connector-python | Python ↔ MySQL |
| File Parsing | openpyxl (via pandas) | Reading `.xlsx` files |
| Deduplication | hashlib | SHA-256 file fingerprinting |
| Hosting | Streamlit Community Cloud | App deployment |
| Language | Python 3.10+ | Everything |

---

## 📖 Usage

```
1. Info page      → Download a sample Excel file
2. Upload page    → Select tool, upload file, start pipeline
3. Compute page   → Select tool + upload ID, compute KPIs
4. Dashboard      → Set date range, explore charts per tool
```

### Adding a new security tool
```
1. Create raw table       →  Database/security_dash.sql
2. Ingestion script       →  ingestion/newtool_upload.py
3. KPI script             →  processing/newtool_kpi.py
4. Register               →  config/tool_registry.py
```
The dashboard, upload, and compute pages pick it up automatically.

---

## 👩‍💻 Author

<div>

**Gurleen Kaur Bali**

[![GitHub](https://img.shields.io/badge/GitHub-gurleenkaurbali19-181717?style=for-the-badge&logo=github)](https://github.com/gurleenkaurbali19)

*CyberPulse — Security Analytics Platform*

</div>

---

<div>

⭐ **Star this repo if you found it useful!**

</div>


© 2026 Gurleen Kaur Bali. All rights reserved.
