import streamlit as st
import os
import sys
import pandas as pd
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.hash_utils import generate_file_hash
from Database.db_utils import check_file_exists, insert_upload
from config.tool_registry import TOOL_REGISTRY


def show_upload():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

    .pg-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem; font-weight: 700;
        color: #0F172A; letter-spacing: -0.02em;
        border-left: 4px solid #2563EB;
        padding-left: 14px; margin-bottom: 4px;
    }
    .pg-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem; color: #64748B;
        margin-bottom: 24px; padding-left: 18px;
    }
    .info-card {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 14px 18px;
        font-family: 'Inter', sans-serif;
        font-size: 0.84rem; color: #1D4ED8;
        margin-bottom: 8px;
    }
    .preview-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem; font-weight: 700;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: #94A3B8; margin: 18px 0 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="pg-title">Upload Security Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Upload exported logs from any integrated security tool. Duplicates are detected automatically.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        tool = st.selectbox("Security Tool", list(TOOL_REGISTRY.keys()))

    with col2:
        uploaded_file = st.file_uploader("Excel File (.xlsx / .xls)", type=["xlsx", "xls"])

    if uploaded_file is None:
        st.markdown('<div class="info-card">&#8593; Select a tool and upload an Excel export to begin.</div>', unsafe_allow_html=True)
        return

    df_preview = pd.read_excel(uploaded_file)

    st.markdown('<div class="preview-label">File Preview (first 5 rows)</div>', unsafe_allow_html=True)
    st.dataframe(df_preview.head(5), use_container_width=True)

    uploaded_file.seek(0)

    st.markdown("---")

    if st.button("Start Upload Pipeline", type="primary", use_container_width=False):
        with st.spinner("Checking duplicates and ingesting data..."):
            time.sleep(0.8)
            file_hash = generate_file_hash(uploaded_file)
            existing = check_file_exists(file_hash)
            if existing:
                st.warning(f"File already uploaded (Upload ID: {existing}). Skipping.")
                return

            upload_id = insert_upload(tool, uploaded_file.name, file_hash)
            upload_func = TOOL_REGISTRY[tool]["upload_func"]
            upload_func(uploaded_file, upload_id)
            time.sleep(0.5)

        st.success(f"Upload complete. Data ingested into raw tables. Upload ID: {upload_id}")