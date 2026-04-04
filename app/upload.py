import streamlit as st
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.hash_utils import generate_file_hash
from Database.db_utils import check_file_exists, insert_upload
from ingestion.falcon_upload import upload_falcon


def show_upload():
    st.title("📤 Upload Security Tool Data")

    tool = st.selectbox(
        "Select Tool",
        ["Falcon"]  # later expand
    )

    uploaded_file = st.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"]
    )

    if uploaded_file is None:
        return

    # Preview
    import pandas as pd
    df_preview = pd.read_excel(uploaded_file)
    st.subheader("Preview")
    st.dataframe(df_preview.head(5))

    # Reset pointer after preview
    uploaded_file.seek(0)

    if st.button("🚀 Upload Data"):
        try:
            # Step 1: Generate hash
            file_hash = generate_file_hash(uploaded_file)

            # Step 2: Check duplicate
            existing = check_file_exists(file_hash)

            if existing:
                st.warning(f"⚠️ File already uploaded (Upload ID: {existing})")
                return

            # Step 3: Insert upload record
            upload_id = insert_upload("FALCON", uploaded_file.name, file_hash)

            # Step 4: Insert raw data
            upload_falcon(uploaded_file, upload_id)

            st.success(f"✅ Upload successful! Upload ID: {upload_id}")

        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
