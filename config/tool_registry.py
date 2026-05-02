from ingestion.falcon_upload import upload_falcon
from processing.falcon_kpi import compute_falcon_kpis

from ingestion.cyble_upload import upload_cyble
from processing.cyble_kpi import compute_cyble_kpis

from ingestion.siem_upload import upload_siem
from processing.siem_kpi import compute_siem_kpis

from ingestion.trend_vision_upload import upload_trend_vision
from processing.trend_vision_kpi import compute_trend_vision_kpis

from ingestion.com_olho_upload import upload_com_olho
from processing.com_olho_kpi import compute_com_olho_kpis

from ingestion.netskope_upload import upload_netskope
from processing.netskope_kpi import compute_netskope_kpis



TOOL_REGISTRY = {
    "FALCON": {
        "upload_func": upload_falcon,
        "kpi_func": compute_falcon_kpis,
        "table_name": "raw_falcon"
    },
    "CYBLE": {
        "upload_func": upload_cyble,
        "kpi_func": compute_cyble_kpis,
        "table_name": "raw_cyble"
    },
    "SIEM": {
        "upload_func": upload_siem,
        "kpi_func": compute_siem_kpis,
        "table_name": "raw_siem"
    },
    "TREND_VISION": {
        "upload_func": upload_trend_vision,
        "kpi_func": compute_trend_vision_kpis,
        "table_name": "raw_trend_vision"        
    },
    "COM_OLHO": {
        "upload_func": upload_com_olho,
        "kpi_func": compute_com_olho_kpis,
        "table_name": "raw_com_olho"
    },
    "NETSKOPE": {
        "upload_func": upload_netskope,
        "kpi_func": compute_netskope_kpis,
        "table_name": "raw_netskope"
    }

}