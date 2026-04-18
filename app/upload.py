import streamlit as st
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.hash_utils import generate_file_hash
from Database.db_utils import check_file_exists, insert_upload
from Database.database_connection import get_connection
from config.tool_registry import TOOL_REGISTRY


def show_upload():
    st.title("📤 Upload Security Tool Data")

    # -------------------------------
    # Tool Selection
    # -------------------------------
    tool = st.selectbox(
        "Select Tool",
        list(TOOL_REGISTRY.keys())
    )

    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"]
    )

    if uploaded_file is None:
        return

    # -------------------------------
    # Preview
    # -------------------------------
    import pandas as pd
    df_preview = pd.read_excel(uploaded_file)
    st.subheader("Preview")
    st.dataframe(df_preview.head(5))

    # Reset pointer after preview
    uploaded_file.seek(0)

    # -------------------------------
    # Upload Logic 
    # -------------------------------
    if st.button("🚀 Upload Data"):
        conn = None
        try:
            # Step 1: Generate hash
            file_hash = generate_file_hash(uploaded_file)

            # Step 2: Check duplicate
            existing = check_file_exists(file_hash)
            if existing:
                st.warning(f"⚠️ File already uploaded (Upload ID: {existing})")
                return

            # Step 3: Insert upload record
            upload_id = insert_upload(tool, uploaded_file.name, file_hash)

            # Step 4: Get tool-specific upload function
            upload_func = TOOL_REGISTRY[tool]["upload_func"]

            # Step 5: Perform ingestion
            upload_func(uploaded_file, upload_id)

            st.success(f"✅ Upload successful! Upload ID: {upload_id}")

        except Exception as e:
            # CRITICAL FIX: rollback upload_master entry if ingestion fails
            try:
                if 'upload_id' in locals():
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute(
                        "DELETE FROM upload_master WHERE upload_id = %s",
                        (upload_id,)
                    )
                    conn.commit()
                    conn.close()
            except Exception as cleanup_error:
                st.error(f"⚠️ Cleanup failed: {cleanup_error}")

            st.error(f"❌ Upload failed: {e}")
