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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ===== DARK THEME BASE ===== */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f1a 100%) !important;
    }

    /* ===== ANIMATED BACKGROUND EFFECTS ===== */
    .cyber-grid {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
        animation: gridPulse 4s ease-in-out infinite;
    }

    @keyframes gridPulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }

    .scanlines {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 255, 0.01) 2px,
            rgba(0, 255, 255, 0.01) 4px
        );
        pointer-events: none;
        z-index: 1;
        animation: scanMove 8s linear infinite;
    }

    @keyframes scanMove {
        0% { transform: translateY(0); }
        100% { transform: translateY(20px); }
    }

    .floating-particles {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }

    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: radial-gradient(circle, rgba(0, 255, 255, 0.8), transparent);
        border-radius: 50%;
        animation: floatUp 15s infinite linear;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }

    @keyframes floatUp {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }

    /* ===== PAGE TITLE ===== */
    .pg-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #00ffff 50%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        border-left: 4px solid #00ffff;
        padding-left: 16px;
        margin-bottom: 6px;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.3);
        position: relative;
    }

    .pg-title::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #00ffff, #00ff88);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.4);
    }

    .pg-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 28px;
        padding-left: 20px;
        border-left: 2px solid rgba(100, 116, 139, 0.3);
    }

    /* ===== KPI LABEL ===== */
    .kpi-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #00ffff;
        margin: 24px 0 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .kpi-label::before {
        content: '//';
        color: #00ff88;
        font-weight: 700;
    }

    /* ===== GLASSMORPHISM CARDS ===== */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ffff, transparent);
    }

    .glass-card:hover {
        border-color: rgba(0, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.15);
        transform: translateY(-2px);
    }

    /* ===== SELECT BOX STYLING ===== */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(0, 255, 255, 0.4) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.1) !important;
    }

    .stSelectbox label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
    }

    .stSelectbox label::before {
        content: '// ';
        color: #00ffff;
    }

    /* ===== BUTTON STYLING ===== */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 255, 136, 0.2)) !important;
        border: 1px solid rgba(0, 255, 255, 0.4) !important;
        border-radius: 10px !important;
        color: #00ffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        padding: 12px 32px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 255, 136, 0.3)) !important;
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.1) !important;
        transform: translateY(-2px) !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00ffff, #00ff88, #00ffff) !important;
        background-size: 200% 100% !important;
        animation: progressGlow 2s linear infinite !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
    }

    @keyframes progressGlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }

    /* ===== DATAFRAME STYLING ===== */
    .stDataFrame {
        background: rgba(15, 23, 42, 0.6) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 255, 255, 0.15) !important;
        overflow: hidden !important;
    }

    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: rgba(10, 15, 25, 0.8) !important;
    }

    /* ===== ALERT STYLING ===== */
    .stAlert {
        background: rgba(15, 23, 42, 0.8) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stAlert"] > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }

    /* Success alert */
    div[data-baseweb="notification"][kind="positive"],
    .element-container div[data-testid="stAlert"]:has([data-testid="stMarkdownContainer"]) {
        background: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
    }

    /* Warning alert */
    div[data-baseweb="notification"][kind="warning"] {
        background: rgba(255, 170, 0, 0.1) !important;
        border: 1px solid rgba(255, 170, 0, 0.3) !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3), transparent) !important;
        margin: 24px 0 !important;
    }

    /* ===== ENGINE STATUS CARD ===== */
    .engine-status {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px 24px;
        margin: 20px 0;
        display: flex;
        align-items: center;
        gap: 16px;
        position: relative;
        overflow: hidden;
    }

    .engine-status::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00ffff, #00ff88);
    }

    .engine-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 255, 136, 0.2));
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.3);
        animation: enginePulse 2s ease-in-out infinite;
    }

    @keyframes enginePulse {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 255, 0.3); }
        50% { box-shadow: 0 0 25px rgba(0, 255, 255, 0.6); }
    }

    .engine-info {
        flex: 1;
    }

    .engine-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 4px;
    }

    .engine-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: #64748b;
    }

    .engine-badge {
        background: rgba(0, 255, 136, 0.15);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 20px;
        padding: 6px 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 600;
        color: #00ff88;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .badge-dot {
        width: 6px;
        height: 6px;
        background: #00ff88;
        border-radius: 50%;
        animation: dotPulse 1.5s ease-in-out infinite;
    }

    @keyframes dotPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }

    /* ===== PROCESSING PIPELINE ===== */
    .pipeline-container {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 255, 0.15);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
    }

    .pipeline-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        color: #00ffff;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .pipeline-header::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #00ffff;
        border-radius: 50%;
        animation: headerPulse 1s ease-in-out infinite;
    }

    @keyframes headerPulse {
        0%, 100% { box-shadow: 0 0 5px #00ffff; }
        50% { box-shadow: 0 0 15px #00ffff, 0 0 25px #00ffff; }
    }

    .pipeline-steps {
        display: flex;
        justify-content: space-between;
        position: relative;
    }

    .pipeline-steps::before {
        content: '';
        position: absolute;
        top: 20px;
        left: 40px;
        right: 40px;
        height: 2px;
        background: rgba(100, 116, 139, 0.3);
    }

    .pipeline-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
        z-index: 1;
    }

    .step-icon {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .step-icon.pending {
        background: rgba(100, 116, 139, 0.2);
        border: 2px solid rgba(100, 116, 139, 0.4);
        color: #64748b;
    }

    .step-icon.active {
        background: rgba(0, 255, 255, 0.2);
        border: 2px solid #00ffff;
        color: #00ffff;
        animation: stepActive 1s ease-in-out infinite;
    }

    @keyframes stepActive {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 255, 0.5); }
        50% { box-shadow: 0 0 25px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.4); }
    }

    .step-icon.complete {
        background: rgba(0, 255, 136, 0.2);
        border: 2px solid #00ff88;
        color: #00ff88;
    }

    .step-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        text-align: center;
        max-width: 80px;
    }

    /* ===== SUCCESS CONTAINER ===== */
    .success-container {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 255, 255, 0.05));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        text-align: center;
        animation: successPop 0.5s ease-out;
    }

    @keyframes successPop {
        0% { transform: scale(0.9); opacity: 0; }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); opacity: 1; }
    }

    .success-icon {
        font-size: 3rem;
        margin-bottom: 12px;
        animation: checkBounce 0.6s ease-out 0.3s both;
    }

    @keyframes checkBounce {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }

    .success-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #00ff88;
        margin-bottom: 8px;
    }

    .success-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #94a3b8;
    }

    /* ===== COMPUTED KPI BADGE ===== */
    .kpi-ready-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 255, 136, 0.15);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 8px;
        padding: 8px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #00ff88;
        margin: 12px 0;
    }

    .kpi-ready-badge::before {
        content: '';
        width: 8px;
        height: 8px;
        background: #00ff88;
        border-radius: 50%;
        animation: dotPulse 1.5s ease-in-out infinite;
    }

    /* ===== COLUMN STYLING ===== */
    [data-testid="column"] {
        background: transparent !important;
    }

    /* ===== WARNING CONTAINER ===== */
    .warning-container {
        background: rgba(255, 170, 0, 0.1);
        border: 1px solid rgba(255, 170, 0, 0.3);
        border-radius: 12px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .warning-icon {
        font-size: 1.5rem;
    }

    .warning-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #fbbf24;
    }
    </style>

    <!-- Background Effects -->
    <div class="cyber-grid"></div>
    <div class="scanlines"></div>
    <div class="floating-particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 35%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 65%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 5s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 2.5s;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Page Title
    st.markdown('<div class="pg-title">KPI Computation Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Select a security tool and upload ID to compute metrics and store KPIs into the master database.</div>', unsafe_allow_html=True)

    # Engine Status Card
    st.markdown("""
    <div class="engine-status">
        <div class="engine-icon">&#9881;</div>
        <div class="engine-info">
            <div class="engine-title">KPI Processing Engine</div>
            <div class="engine-desc">Automated metric computation and aggregation system</div>
        </div>
        <div class="engine-badge">
            <div class="badge-dot"></div>
            Ready
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        tool = st.selectbox("Security Tool", list(TOOL_REGISTRY.keys()))

    upload_ids = get_upload_ids_by_tool(tool)

    if not upload_ids:
        st.markdown("""
        <div class="warning-container">
            <div class="warning-icon">&#9888;</div>
            <div class="warning-text">No uploads found for this tool. Please upload data first.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    with col2:
        upload_id = st.selectbox("Upload ID", upload_ids)

    st.markdown("---")

    existing_kpis = fetch_kpis(upload_id)
    has_kpis = existing_kpis is not None and not existing_kpis.empty

    if has_kpis:
        st.markdown("""
        <div class="success-container">
            <div class="success-icon">&#10004;</div>
            <div class="success-title">KPIs Already Computed</div>
            <div class="success-desc">This upload has been processed. Ready for dashboard visualization.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="kpi-ready-badge">Stored KPIs Available</div>', unsafe_allow_html=True)
        st.markdown('<div class="kpi-label">Stored KPIs</div>', unsafe_allow_html=True)
        st.dataframe(existing_kpis, use_container_width=True)
        return

    # Processing Pipeline Visualization
    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-header">Processing Pipeline</div>
        <div class="pipeline-steps">
            <div class="pipeline-step">
                <div class="step-icon pending" id="step-1">&#128196;</div>
                <div class="step-label">Load Data</div>
            </div>
            <div class="pipeline-step">
                <div class="step-icon pending" id="step-2">&#128269;</div>
                <div class="step-label">Parse Logs</div>
            </div>
            <div class="pipeline-step">
                <div class="step-icon pending" id="step-3">&#9881;</div>
                <div class="step-label">Compute</div>
            </div>
            <div class="pipeline-step">
                <div class="step-icon pending" id="step-4">&#128202;</div>
                <div class="step-label">Aggregate</div>
            </div>
            <div class="pipeline-step">
                <div class="step-icon pending" id="step-5">&#128190;</div>
                <div class="step-label">Store</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Run KPI Engine", type="primary", use_container_width=True):
        progress = st.progress(0, text="Initializing engine...")
        time.sleep(0.5)
        progress.progress(20, text="Loading raw data...")
        time.sleep(0.5)
        progress.progress(35, text="Parsing security logs...")
        time.sleep(0.7)
        progress.progress(50, text="Computing KPI metrics...")

        update_processing_status(upload_id, "processing")

        kpi_func = TOOL_REGISTRY[tool]["kpi_func"]
        kpis = kpi_func(upload_id)
        insert_kpis(upload_id, kpis)

        progress.progress(70, text="Aggregating results...")
        time.sleep(0.5)
        progress.progress(90, text="Saving to kpi_master...")
        update_processing_status(upload_id, "completed")
        time.sleep(0.3)
        progress.progress(100, text="Complete!")

        st.balloons()
        
        st.markdown("""
        <div class="success-container">
            <div class="success-icon">&#10004;</div>
            <div class="success-title">KPI Computation Complete</div>
            <div class="success-desc">All metrics have been calculated and stored. Head to Dashboard to visualize.</div>
        </div>
        """, unsafe_allow_html=True)

        fresh_kpis = fetch_kpis(upload_id)
        if fresh_kpis is not None and not fresh_kpis.empty:
            st.markdown('<div class="kpi-label">Computed KPIs</div>', unsafe_allow_html=True)
            st.dataframe(fresh_kpis, use_container_width=True)
