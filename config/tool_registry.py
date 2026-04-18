from ingestion.falcon_upload import upload_falcon
from processing.falcon_kpi import compute_falcon_kpis
from Database.db_utils import fetch_raw_falcon

TOOL_REGISTRY = {
    "FALCON": {
        "upload_func": upload_falcon,
        "kpi_func": compute_falcon_kpis,
        "fetch_raw": fetch_raw_falcon
    }
}
