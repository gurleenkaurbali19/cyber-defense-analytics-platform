import streamlit as st
import os
import sys
import pandas as pd
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.hash_utils import generate_file_hash
from Database.db_utils import check_file_exists, insert_upload
from config.tool_registry import TOOL_REGISTRY


# Expected columns for each tool based on database schema
# Keys are UPPERCASE to match TOOL_REGISTRY
TOOL_EXPECTED_COLUMNS = {
    "FALCON": {
        "required": ["hostname", "username", "severity_name", "status", "first_detect", "tactic"],
        "optional": ["first_assign", "resolved_time", "resolution"]
    },
    "CYBLE": {
        "required": ["data_source", "record_date", "alert_severity", "alert_id", "alert_status"],
        "optional": ["alert_generated_date", "keyword"]
    },
    "SIEM": {
        "required": ["alert_type", "severity", "alert_time", "validation_status"],
        "optional": []
    },
    "TREND_VISION": {
        "required": ["detected", "threat_type", "status"],
        "optional": ["security_filter", "protection_mode", "affected_user", "sender", "recipient"]
    },
    "COM_OLHO": {
        "required": ["submission_date", "technical_severity", "status"],
        "optional": ["sla_status", "age_of_vulnerability_days", "vulnerability_type", "reward_amount", "report_status"]
    },
    "NETSKOPE": {
        "required": ["hostname", "user"],
        "optional": ["os_platform", "internet_security_status", "last_event"]
    }
}


def normalize_column_name(col):
    """Normalize column name for comparison - lowercase, remove spaces/underscores/hyphens"""
    return col.lower().strip().replace("_", "").replace(" ", "").replace("-", "")


def validate_file_columns(df, tool_name):
    """
    Validate that the uploaded file has the expected columns for the selected tool.
    Uses STRICT matching - file must have ALL required columns for the selected tool.
    Returns (is_valid, error_message, missing_cols, extra_cols)
    """
    # Case-insensitive lookup
    tool_key = tool_name.upper()
    
    if tool_key not in TOOL_EXPECTED_COLUMNS:
        return True, None, [], []  # If tool not in validation list, allow upload
    
    expected = TOOL_EXPECTED_COLUMNS[tool_key]
    required_cols = expected["required"]
    
    # Normalize all file columns
    file_cols_normalized = {normalize_column_name(col): col for col in df.columns}
    
    # Check for missing required columns (STRICT matching - exact match only)
    missing_required = []
    for req_col in required_cols:
        req_normalized = normalize_column_name(req_col)
        
        # Check for exact match only (after normalization)
        if req_normalized not in file_cols_normalized:
            missing_required.append(req_col)
    
    if missing_required:
        error_msg = f"This file does not appear to be {tool_name} data. Missing required columns: {', '.join(missing_required)}"
        return False, error_msg, missing_required, []
    
    return True, None, [], []


def show_upload():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ===== DARK THEME BASE ===== */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f1a 100%) !important;
    }

    /* ===== ANIMATED BACKGROUNDS ===== */
    .bg-grid {
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
        0% { background-position: 0 0; }
        100% { background-position: 0 100px; }
    }

    /* Floating particles */
    .particles {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        overflow: hidden;
        pointer-events: none;
        z-index: 0;
    }
    .particle {
        position: absolute;
        width: 4px; height: 4px;
        background: rgba(0, 255, 255, 0.6);
        border-radius: 50%;
        animation: float 15s infinite ease-in-out;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    .particle:nth-child(1) { left: 10%; animation-delay: 0s; animation-duration: 18s; }
    .particle:nth-child(2) { left: 25%; animation-delay: 2s; animation-duration: 22s; }
    .particle:nth-child(3) { left: 45%; animation-delay: 4s; animation-duration: 16s; }
    .particle:nth-child(4) { left: 65%; animation-delay: 1s; animation-duration: 20s; }
    .particle:nth-child(5) { left: 85%; animation-delay: 3s; animation-duration: 17s; }
    @keyframes float {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(720deg); opacity: 0; }
    }

    /* ===== PAGE TITLE ===== */
    .pg-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #00d4ff 50%, #00ff88 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.02em;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 12px;
        position: relative;
        z-index: 10;
    }
    .pg-title::before {
        content: '';
        width: 4px;
        height: 100%;
        min-height: 36px;
        background: linear-gradient(180deg, #00d4ff, #00ff88);
        border-radius: 2px;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
    }

    .pg-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 28px;
        padding-left: 18px;
        position: relative;
        z-index: 10;
    }
    .pg-sub::before {
        content: '//';
        color: #00d4ff;
        margin-right: 8px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ===== UPLOAD CONTAINER ===== */
    .upload-zone {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 15, 25, 0.95));
        border: 2px dashed rgba(0, 212, 255, 0.3);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        z-index: 10;
    }
    .upload-zone:hover {
        border-color: rgba(0, 212, 255, 0.6);
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.15), inset 0 0 60px rgba(0, 212, 255, 0.05);
        transform: translateY(-2px);
    }
    .upload-zone::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at center, rgba(0, 212, 255, 0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    .upload-zone:hover::before {
        opacity: 1;
    }

    .upload-icon {
        font-size: 3rem;
        margin-bottom: 16px;
        animation: uploadBounce 2s ease-in-out infinite;
    }
    @keyframes uploadBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    .upload-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .upload-hint {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #475569;
    }

    /* ===== TOOL SELECTOR CARD ===== */
    .tool-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 25, 0.98));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        z-index: 10;
        backdrop-filter: blur(10px);
    }
    .tool-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    }
    .tool-card-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #00d4ff;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .tool-card-label::before {
        content: '';
        width: 6px; height: 6px;
        background: #00d4ff;
        border-radius: 50%;
        box-shadow: 0 0 8px #00d4ff;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
    }

    /* ===== INFO CARD ===== */
    .info-card {
        background: linear-gradient(145deg, rgba(0, 212, 255, 0.1), rgba(0, 212, 255, 0.05));
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #00d4ff;
        margin: 16px 0;
        display: flex;
        align-items: center;
        gap: 12px;
        position: relative;
        z-index: 10;
        backdrop-filter: blur(10px);
    }
    .info-card::before {
        content: 'i';
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px; height: 24px;
        background: rgba(0, 212, 255, 0.2);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 50%;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        flex-shrink: 0;
    }

    /* ===== PREVIEW SECTION ===== */
    .preview-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #00d4ff;
        margin: 24px 0 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        position: relative;
        z-index: 10;
    }
    .preview-label::before {
        content: '//';
        color: #475569;
    }
    .preview-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.3), transparent);
    }

    /* ===== DATAFRAME STYLING ===== */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
    }
    [data-testid="stDataFrame"] > div {
        background: rgba(15, 23, 42, 0.9) !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #00a8cc) !important;
        color: #0a0a0f !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3) !important;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ===== SELECT BOX ===== */
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.9) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }
    .stSelectbox > div > div:hover {
        border-color: rgba(0, 212, 255, 0.5) !important;
    }
    .stSelectbox [data-baseweb="select"] {
        background: transparent !important;
    }
    .stSelectbox svg {
        fill: #00d4ff !important;
    }

    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 15, 25, 0.95)) !important;
        border: 2px dashed rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(0, 212, 255, 0.5) !important;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.1) !important;
    }
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        padding: 0 !important;
    }
    [data-testid="stFileUploader"] section > div {
        color: #94A3B8 !important;
    }
    [data-testid="stFileUploader"] button {
        background: rgba(0, 212, 255, 0.1) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        color: #00d4ff !important;
    }

    /* ===== ALERTS ===== */
    .stAlert {
        border-radius: 12px !important;
        border: none !important;
    }
    [data-testid="stAlert"] {
        background: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Success alert */
    .element-container:has([data-testid="stAlert"]) [data-baseweb="notification"] {
        background: linear-gradient(145deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 136, 0.05)) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
    }

    /* Warning alert */
    .stWarning {
        background: linear-gradient(145deg, rgba(255, 193, 7, 0.15), rgba(255, 193, 7, 0.05)) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
    }

    /* ===== SUCCESS ANIMATION ===== */
    .success-container {
        background: linear-gradient(145deg, rgba(0, 255, 136, 0.1), rgba(0, 255, 136, 0.05));
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: successPop 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        z-index: 10;
    }
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    .success-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: radial-gradient(circle at center, rgba(0, 255, 136, 0.1) 0%, transparent 70%);
    }
    .success-icon {
        font-size: 3.5rem;
        margin-bottom: 16px;
        animation: successBounce 0.6s ease-out 0.2s both;
    }
    @keyframes successBounce {
        0% { transform: scale(0) rotate(-45deg); }
        50% { transform: scale(1.2) rotate(10deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
    .success-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #00ff88;
        margin-bottom: 8px;
    }
    .success-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #94A3B8;
    }
    .success-id {
        display: inline-block;
        background: rgba(0, 255, 136, 0.2);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 6px;
        padding: 4px 12px;
        margin-top: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #00ff88;
    }

    /* ===== DUPLICATE WARNING ===== */
    .duplicate-container {
        background: linear-gradient(145deg, rgba(255, 193, 7, 0.1), rgba(255, 193, 7, 0.05));
        border: 1px solid rgba(255, 193, 7, 0.3);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        position: relative;
        z-index: 10;
    }
    .duplicate-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
    }
    .duplicate-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffc107;
        margin-bottom: 8px;
    }
    .duplicate-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #94A3B8;
    }

    /* ===== VALIDATION ERROR ===== */
    .validation-error-container {
        background: linear-gradient(145deg, rgba(255, 71, 87, 0.1), rgba(255, 71, 87, 0.05));
        border: 1px solid rgba(255, 71, 87, 0.3);
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        position: relative;
        z-index: 10;
        animation: errorShake 0.5s ease-in-out;
    }
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        20%, 60% { transform: translateX(-5px); }
        40%, 80% { transform: translateX(5px); }
    }
    .validation-error-icon {
        font-size: 2.5rem;
        margin-bottom: 12px;
        color: #ff4757;
    }
    .validation-error-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: #ff4757;
        margin-bottom: 12px;
    }
    .validation-error-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #94A3B8;
        margin-bottom: 16px;
    }
    .missing-cols-list {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        justify-content: center;
        margin-top: 12px;
    }
    .missing-col-tag {
        background: rgba(255, 71, 87, 0.2);
        border: 1px solid rgba(255, 71, 87, 0.4);
        border-radius: 6px;
        padding: 4px 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #ff6b7a;
    }
    .expected-cols-hint {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #64748B;
        margin-top: 16px;
        padding: 12px;
        background: rgba(71, 85, 105, 0.1);
        border-radius: 8px;
        text-align: left;
    }
    .expected-cols-hint strong {
        color: #00d4ff;
    }

    /* ===== LABELS ===== */
    .stSelectbox label, .stFileUploader label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #64748B !important;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent) !important;
        margin: 24px 0 !important;
    }

    /* ===== SPINNER / LOADER ===== */
    .stSpinner > div {
        border-color: #00d4ff !important;
    }
    .stSpinner > div > div {
        border-top-color: #00d4ff !important;
    }

    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div {
        background: linear-gradient(90deg, #00d4ff, #00ff88) !important;
        border-radius: 10px !important;
    }
    .stProgress > div {
        background: rgba(0, 212, 255, 0.1) !important;
        border-radius: 10px !important;
    }

    /* ===== PROCESSING CARD ===== */
    .processing-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 25, 0.98));
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 16px;
        padding: 28px;
        position: relative;
        overflow: hidden;
        z-index: 10;
    }
    .processing-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00d4ff, #00ff88, #00d4ff);
        background-size: 200% 100%;
        animation: shimmer 2s linear infinite;
    }
    @keyframes shimmer {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    .processing-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: #e6edf3;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .processing-title::before {
        content: '';
        width: 10px;
        height: 10px;
        background: #00d4ff;
        border-radius: 50%;
        box-shadow: 0 0 15px #00d4ff;
        animation: processingPulse 1s ease-in-out infinite;
    }
    @keyframes processingPulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.3); opacity: 0.7; }
    }

    /* ===== STEP ITEM ===== */
    .step-item {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 18px;
        margin: 8px 0;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    .step-item.pending {
        background: rgba(71, 85, 105, 0.1);
        border: 1px solid rgba(71, 85, 105, 0.2);
    }
    .step-item.active {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.1);
    }
    .step-item.complete {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    .step-item.error {
        background: rgba(255, 71, 87, 0.1);
        border: 1px solid rgba(255, 71, 87, 0.3);
    }
    .step-icon-box {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .step-item.pending .step-icon-box {
        background: rgba(71, 85, 105, 0.3);
        border: 2px solid #475569;
        color: #475569;
    }
    .step-item.active .step-icon-box {
        background: rgba(0, 212, 255, 0.2);
        border: 2px solid #00d4ff;
        color: #00d4ff;
        animation: iconPulse 1s ease-in-out infinite;
    }
    @keyframes iconPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(0, 212, 255, 0); }
    }
    .step-item.complete .step-icon-box {
        background: rgba(0, 255, 136, 0.2);
        border: 2px solid #00ff88;
        color: #00ff88;
    }
    .step-item.error .step-icon-box {
        background: rgba(255, 71, 87, 0.2);
        border: 2px solid #ff4757;
        color: #ff4757;
    }
    .step-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    .step-item.pending .step-text { color: #64748B; }
    .step-item.active .step-text { color: #00d4ff; font-weight: 500; }
    .step-item.complete .step-text { color: #00ff88; }
    .step-item.error .step-text { color: #ff4757; }

    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu, footer, header {visibility: hidden;}
    </style>

    <!-- Background Effects -->
    <div class="bg-grid"></div>
    <div class="scanlines"></div>
    <div class="particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="pg-title">Upload Security Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Upload exported logs from any integrated security tool. Duplicates are detected automatically.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-card-label">Security Tool</div>
        </div>
        """, unsafe_allow_html=True)
        tool = st.selectbox("Security Tool", list(TOOL_REGISTRY.keys()), label_visibility="collapsed")

    with col2:
        uploaded_file = st.file_uploader("Excel File (.xlsx / .xls)", type=["xlsx", "xls"])

    if uploaded_file is None:
        st.markdown("""
        <div class="info-card">
            Select a tool and upload an Excel export to begin processing.
        </div>
        """, unsafe_allow_html=True)
        return

    df_preview = pd.read_excel(uploaded_file)

    st.markdown('<div class="preview-label">File Preview (first 5 rows)</div>', unsafe_allow_html=True)
    st.dataframe(df_preview.head(5), use_container_width=True)

    uploaded_file.seek(0)

    st.markdown("---")

    if st.button("Start Upload Pipeline", type="primary", use_container_width=False):
        # Create container for progress
        progress_container = st.container()
        
        with progress_container:
            st.markdown('<div class="processing-card"><div class="processing-title">Upload Pipeline Status</div>', unsafe_allow_html=True)
            
            # Create placeholders for each step
            step_placeholders = {}
            step_names = [
                'Validating file format',
                'Generating file hash',
                'Checking for duplicates',
                'Initializing upload record',
                'Processing data ingestion',
                'Finalizing upload'
            ]
            
            for step_name in step_names:
                step_placeholders[step_name] = st.empty()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        def render_step(placeholder, step_name, status):
            """Render a single step with given status"""
            icons = {
                'pending': '&#9675;',  # Circle
                'active': '&#9678;',   # Bullseye
                'complete': '&#10003;', # Checkmark
                'error': '&#10007;'    # X mark
            }
            icon = icons.get(status, '&#9675;')
            placeholder.markdown(f'''
                <div class="step-item {status}">
                    <div class="step-icon-box">{icon}</div>
                    <div class="step-text">{step_name}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # Initialize all steps as pending
        steps_status = {name: 'pending' for name in step_names}
        for step_name in step_names:
            render_step(step_placeholders[step_name], step_name, 'pending')
        
        result_placeholder = st.empty()
        
        try:
            # Step 1: Validating file format and columns
            steps_status['Validating file format'] = 'active'
            render_step(step_placeholders['Validating file format'], 'Validating file format', 'active')
            time.sleep(0.3)
            
            # Validate columns match the selected tool
            is_valid, error_msg, missing_cols, _ = validate_file_columns(df_preview, tool)
            
            if not is_valid:
                steps_status['Validating file format'] = 'error'
                render_step(step_placeholders['Validating file format'], 'Validating file format', 'error')
                time.sleep(0.3)
                
                # Build missing columns tags
                missing_tags = ''.join([f'<span class="missing-col-tag">{col}</span>' for col in missing_cols])
                
                # Get expected columns for hint
                expected_cols = TOOL_EXPECTED_COLUMNS.get(tool.upper(), {})
                required = expected_cols.get("required", [])
                optional = expected_cols.get("optional", [])
                
                result_placeholder.markdown(f"""
                <div class="validation-error-container">
                    <div class="validation-error-icon">&#10060;</div>
                    <div class="validation-error-title">Invalid File Format</div>
                    <div class="validation-error-text">
                        This file does not match the expected format for <strong style="color: #00d4ff;">{tool}</strong> data.
                    </div>
                    <div style="color: #ff6b7a; font-size: 0.85rem; margin-bottom: 8px;">Missing Required Columns:</div>
                    <div class="missing-cols-list">{missing_tags}</div>
                    <div class="expected-cols-hint">
                        <strong>Expected columns for {tool}:</strong><br/>
                        Required: {', '.join(required)}<br/>
                        {'Optional: ' + ', '.join(optional) if optional else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                return
            
            steps_status['Validating file format'] = 'complete'
            render_step(step_placeholders['Validating file format'], 'Validating file format', 'complete')
            
            # Step 2: Generate hash
            steps_status['Generating file hash'] = 'active'
            render_step(step_placeholders['Generating file hash'], 'Generating file hash', 'active')
            file_hash = generate_file_hash(uploaded_file)
            time.sleep(0.3)
            steps_status['Generating file hash'] = 'complete'
            render_step(step_placeholders['Generating file hash'], 'Generating file hash', 'complete')
            
            # Step 3: Check duplicates
            steps_status['Checking for duplicates'] = 'active'
            render_step(step_placeholders['Checking for duplicates'], 'Checking for duplicates', 'active')
            existing = check_file_exists(file_hash)
            time.sleep(0.4)
            
            if existing:
                steps_status['Checking for duplicates'] = 'error'
                render_step(step_placeholders['Checking for duplicates'], 'Checking for duplicates', 'error')
                time.sleep(0.3)
                
                result_placeholder.markdown(f"""
                <div class="duplicate-container">
                    <div class="duplicate-icon">&#9888;</div>
                    <div class="duplicate-title">Duplicate File Detected</div>
                    <div class="duplicate-text">This file has already been uploaded.<br/>Upload ID: <strong>{existing}</strong></div>
                </div>
                """, unsafe_allow_html=True)
                return
            
            steps_status['Checking for duplicates'] = 'complete'
            render_step(step_placeholders['Checking for duplicates'], 'Checking for duplicates', 'complete')
            
            # Step 4: Initialize upload
            steps_status['Initializing upload record'] = 'active'
            render_step(step_placeholders['Initializing upload record'], 'Initializing upload record', 'active')
            upload_id = insert_upload(tool, uploaded_file.name, file_hash)
            time.sleep(0.4)
            steps_status['Initializing upload record'] = 'complete'
            render_step(step_placeholders['Initializing upload record'], 'Initializing upload record', 'complete')
            
            # Step 5: Process data
            steps_status['Processing data ingestion'] = 'active'
            render_step(step_placeholders['Processing data ingestion'], 'Processing data ingestion', 'active')
            upload_func = TOOL_REGISTRY[tool]["upload_func"]
            upload_func(uploaded_file, upload_id)
            time.sleep(0.5)
            steps_status['Processing data ingestion'] = 'complete'
            render_step(step_placeholders['Processing data ingestion'], 'Processing data ingestion', 'complete')
            
            # Step 6: Finalize
            steps_status['Finalizing upload'] = 'active'
            render_step(step_placeholders['Finalizing upload'], 'Finalizing upload', 'active')
            time.sleep(0.3)
            steps_status['Finalizing upload'] = 'complete'
            render_step(step_placeholders['Finalizing upload'], 'Finalizing upload', 'complete')
            
            time.sleep(0.5)
            
            # Show success
            result_placeholder.markdown(f"""
            <div class="success-container">
                <div class="success-icon">&#10003;</div>
                <div class="success-title">Upload Complete</div>
                <div class="success-text">Data has been successfully ingested into raw tables</div>
                <div class="success-id">Upload ID: {upload_id}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Confetti-like celebration effect
            st.balloons()
            
        except Exception as e:
            # Mark current step as error
            for step_name, status in steps_status.items():
                if status == 'active':
                    steps_status[step_name] = 'error'
                    render_step(step_placeholders[step_name], step_name, 'error')
                    break
            st.error(f"Upload failed: {str(e)}")
