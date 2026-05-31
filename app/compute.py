import streamlit as st
import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.db_utils import (
    get_upload_ids_by_tool,
    insert_kpis,
    update_processing_status,
    fetch_kpis
)
from config.tool_registry import TOOL_REGISTRY


def show_compute_kpi():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

    .pg-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem; font-weight: 700;
        color: #0F172A; letter-spacing: -0.02em;
        border-left: 4px solid #7C3AED;
        padding-left: 14px; margin-bottom: 4px;
    }
    .pg-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem; color: #64748B;
        margin-bottom: 24px; padding-left: 18px;
    }
    .kpi-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem; font-weight: 700;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: #94A3B8; margin: 18px 0 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="pg-title">KPI Computation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Select a tool and an upload ID to compute and store KPIs into kpi_master.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        tool = st.selectbox("Security Tool", list(TOOL_REGISTRY.keys()))

    upload_ids = get_upload_ids_by_tool(tool)

    if not upload_ids:
        st.warning("No uploads found for this tool. Upload data first.")
        return

    with col2:
        upload_id = st.selectbox("Upload ID", upload_ids)

    st.markdown("---")

    existing_kpis = fetch_kpis(upload_id)
    has_kpis = existing_kpis is not None and not existing_kpis.empty

    if has_kpis:
        st.success("KPIs already computed for this upload. Ready for dashboard.")
        st.markdown('<div class="kpi-label">Stored KPIs</div>', unsafe_allow_html=True)
        st.dataframe(existing_kpis, use_container_width=True)
        return

    if st.button("Run KPI Engine", type="primary"):
        progress = st.progress(0, text="Initializing engine...")
        time.sleep(0.5)
        progress.progress(20, text="Processing raw logs...")
        time.sleep(0.7)
        progress.progress(50, text="Computing KPIs...")

        update_processing_status(upload_id, "processing")

        kpi_func = TOOL_REGISTRY[tool]["kpi_func"]
        kpis = kpi_func(upload_id)
        insert_kpis(upload_id, kpis)

        time.sleep(0.5)
        progress.progress(90, text="Saving to kpi_master...")
        update_processing_status(upload_id, "completed")
        progress.progress(100, text="Done.")

        st.success("KPI computation complete. Head to Dashboard to visualize.")

        fresh_kpis = fetch_kpis(upload_id)
        if fresh_kpis is not None and not fresh_kpis.empty:
            st.markdown('<div class="kpi-label">Computed KPIs</div>', unsafe_allow_html=True)
            st.dataframe(fresh_kpis, use_container_width=True)