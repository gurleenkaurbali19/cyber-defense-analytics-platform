from ingestion.falcon_upload import upload_falcon
from processing.falcon_kpi import compute_falcon_kpis

from ingestion.cyble_upload import upload_cyble
from processing.cyble_kpi import compute_cyble_kpis


TOOL_REGISTRY = {
    "FALCON": {
        "upload_func": upload_falcon,
        "kpi_func": compute_falcon_kpis,
        "raw_table": "raw_falcon"
    },
    "CYBLE": {
        "upload_func": upload_cyble,
        "kpi_func": compute_cyble_kpis,
        "raw_table": "raw_cyble"
    }
}

