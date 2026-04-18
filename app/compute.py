import streamlit as st
import pandas as pd
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.db_utils import (
    get_upload_ids_by_tool,
    insert_kpis,
    update_processing_status,
    get_processing_status,
    fetch_kpis
)

from config.tool_registry import TOOL_REGISTRY


def show_compute_kpi():
    st.title("⚙️ Compute KPIs")

    # -------------------------------
    # Step 1: Select Tool
    # -------------------------------
    tool = st.selectbox(
        "Select Tool",
        list(TOOL_REGISTRY.keys())
    )

    # -------------------------------
    # Step 2: Fetch Upload IDs
    # -------------------------------
    upload_ids = get_upload_ids_by_tool(tool)

    if not upload_ids:
        st.warning("No uploads found for this tool.")
        return

    upload_id = st.selectbox(
        "Select Upload ID",
        upload_ids
    )

    # -------------------------------
    # Step 3: Check KPI Status
    # -------------------------------
    status = get_processing_status(upload_id)

    if status == "completed":
        st.success("✅ KPIs already computed for this upload")

        if st.button("📊 View KPIs"):
            kpi_df = fetch_kpis(upload_id)

            if kpi_df.empty:
                st.warning("No KPIs found.")
            else:
                st.subheader("Computed KPIs")
                st.dataframe(kpi_df)

        return

    # -------------------------------
    # Step 4: Preview Raw Data
    # -------------------------------
    if st.button("🔍 Preview Raw Data"):
        fetch_func = TOOL_REGISTRY[tool]["fetch_raw"]
        df = fetch_func(upload_id)

        if df.empty:
            st.warning("No data found for this upload.")
        else:
            st.subheader("Raw Data Preview")
            st.dataframe(df.head(10))

    # -------------------------------
    # Step 5: Compute KPI
    # -------------------------------
    if st.button("🚀 Compute KPI"):
        try:
            # Update status → processing
            update_processing_status(upload_id, "processing")

            # Call tool-specific KPI function
            kpi_func = TOOL_REGISTRY[tool]["kpi_func"]
            kpis = kpi_func(upload_id)

            if not kpis:
                st.warning("No KPI data generated.")
                update_processing_status(upload_id, "failed")
                return

            # Insert KPIs into DB
            insert_kpis(upload_id, kpis)

            # Update status → completed
            update_processing_status(upload_id, "completed")

            st.success("✅ KPIs computed and stored successfully!")

            # -------------------------------
            # Step 6: Show Computed KPIs
            # -------------------------------
            kpi_df = fetch_kpis(upload_id)

            if not kpi_df.empty:
                st.subheader("Computed KPIs")
                st.dataframe(kpi_df)

        except Exception as e:
            update_processing_status(upload_id, "failed")
            st.error(f"❌ KPI computation failed: {e}")
