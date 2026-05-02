#------------------------CREATING DATABASE------------------------
CREATE DATABASE security_dash;
USE security_dash;

#CREATING UPLOAD_MATER TABLE: The upload_master table stores metadata for every uploaded file and tracks it using a unique upload_id
#to enable data lineage, duplicate detection, and pipeline status monitoring.
CREATE TABLE upload_master (
    upload_id INT AUTO_INCREMENT PRIMARY KEY,
    tool_name VARCHAR(50),
    file_name VARCHAR(255),
    file_hash VARCHAR(64),
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(20) DEFAULT 'pending'
);

# For speeding duplicate checks:
CREATE INDEX idx_file_hash ON upload_master(file_hash);
# For speeding up querying per uplaod:
CREATE INDEX idx_falcon_upload ON raw_falcon(upload_id);


#------------------------CREATING RAW TABLES---------------------

# ------FALCON--------
CREATE TABLE raw_falcon (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,

    hostname VARCHAR(255),
    username VARCHAR(255),
    severity_name VARCHAR(20),
    status VARCHAR(20),

    first_detect DATETIME,
    first_assign DATETIME,
    resolved_time DATETIME,

    tactic VARCHAR(50),
    resolution VARCHAR(50),

    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (upload_id) REFERENCES upload_master(upload_id)
);

#------Cyble------
CREATE TABLE raw_cyble (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,
    data_source VARCHAR(50),
    record_date DATETIME,
    alert_severity VARCHAR(20),
    alert_id VARCHAR(100),
    alert_generated_date DATETIME,
    alert_status VARCHAR(20),
    keyword VARCHAR(100)
);

#------SIEM-------
CREATE TABLE raw_siem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,

    alert_type VARCHAR(100),
    severity VARCHAR(50),
    alert_time DATETIME,
    validation_status VARCHAR(50),

    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (upload_id) REFERENCES upload_master(upload_id)
);

CREATE INDEX idx_siem_upload ON raw_siem(upload_id);

#---------Trend Vision------
CREATE TABLE raw_trend_vision (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,

    detected DATETIME,
    threat_type VARCHAR(50),
    security_filter VARCHAR(100),
    protection_mode VARCHAR(50),

    affected_user VARCHAR(255),
    sender VARCHAR(255),
    recipient VARCHAR(255),

    status VARCHAR(50),

    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (upload_id) REFERENCES upload_master(upload_id)
);

CREATE INDEX idx_trend_upload ON raw_trend_vision(upload_id);

#------COM OLHO ------
CREATE TABLE raw_com_olho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,

    submission_date DATETIME,
    technical_severity VARCHAR(50),
    status VARCHAR(100),
    sla_status VARCHAR(50),

    age_of_vulnerability_days INT,
    vulnerability_type VARCHAR(100),
    reward_amount FLOAT,

    report_status VARCHAR(50),

    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (upload_id) REFERENCES upload_master(upload_id)
);

CREATE INDEX idx_com_olho_upload ON raw_com_olho(upload_id);

#------Netskope-----
CREATE TABLE raw_netskope (
    id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,

    hostname VARCHAR(255),
    os_platform VARCHAR(50),
    user VARCHAR(255),
    internet_security_status VARCHAR(50),
    last_event VARCHAR(50),

    ingestion_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (upload_id) REFERENCES upload_master(upload_id)
);

CREATE INDEX idx_netskope_upload ON raw_netskope(upload_id);


# -----------------------------CREATING KPI TABLE--------------------------------------
CREATE TABLE kpi_master (
    kpi_id INT AUTO_INCREMENT PRIMARY KEY,
    upload_id INT,

    tool_name VARCHAR(50),
    kpi_name VARCHAR(100),
    kpi_value FLOAT,

    kpi_dimension VARCHAR(50),
    dimension_value VARCHAR(50),

    start_date DATE,
    end_date DATE,

    FOREIGN KEY (upload_id) REFERENCES upload_master(upload_id)
);

# Adding indexes for faster querying for dashboard:
CREATE INDEX idx_kpi_tool ON kpi_master(tool_name);
CREATE INDEX idx_kpi_name ON kpi_master(kpi_name);
CREATE INDEX idx_kpi_date ON kpi_master(start_date, end_date);





#Testing
Select * from kpi_master;
SELECT * FROM upload_master;
SELECT * FROM raw_falcon;
select * from raw_cyble;
select * from kpi_master;
select * from raw_siem;
select * from raw_trend_vision;
select * from raw_com_olho;