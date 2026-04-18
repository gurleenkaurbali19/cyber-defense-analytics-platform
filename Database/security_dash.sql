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
delete from kpi_master;
delete from upload_master;
delete from raw_falcon;