import streamlit as st

from home import show_home
from upload import show_upload
from compute import show_compute_kpi
from dashboard import show_dashboard
from info import show_info

st.set_page_config(
    page_title="CyberPulse",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ===== DARK THEME BASE ===== */
html, body, .stApp {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%) !important;
    color: #e6edf3 !important;
}

.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
    background: transparent !important;
}

/* Hide hamburger menu and footer */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* Hide collapse button inside sidebar */
section[data-testid="stSidebar"] > div:first-child > div:first-child button {
    display: none !important;
}
[data-testid="stSidebarNav"] { display: none !important; }
button[data-testid="baseButton-headerNoPadding"] { display: none !important; }

/* ===== ENHANCED SIDEBAR STYLING ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e14 0%, #0d1117 50%, #101820 100%) !important;
    border-right: 1px solid rgba(0, 212, 255, 0.12) !important;
    position: relative;
    overflow: hidden;
}

/* Sidebar cyber grid background */
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: 0;
}

/* Sidebar glow accent at top */
section[data-testid="stSidebar"]::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 200px;
    background: radial-gradient(ellipse at top center, rgba(0, 212, 255, 0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
    background: transparent !important;
    position: relative;
    z-index: 1;
}

/* All sidebar text */
section[data-testid="stSidebar"] * {
    color: #8b949e !important;
    font-family: 'Inter', sans-serif !important;
}

/* ===== SIDEBAR BRAND ===== */
.sb-brand {
    padding: 32px 24px 28px;
    border-bottom: 1px solid rgba(0, 212, 255, 0.12);
    margin-bottom: 8px;
    background: linear-gradient(180deg, rgba(0, 212, 255, 0.06) 0%, rgba(0, 255, 136, 0.02) 50%, transparent 100%);
    position: relative;
    overflow: hidden;
}

/* Animated border glow effect */
.sb-brand::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00d4ff, #00ff88, transparent);
    animation: borderGlow 3s ease-in-out infinite;
}

@keyframes borderGlow {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.8; }
}

/* Status indicator */
.sb-status {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;
}

.sb-status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 10px #00ff88, 0 0 20px rgba(0, 255, 136, 0.4);
    animation: statusPulse 2s ease-in-out infinite;
}

@keyframes statusPulse {
    0%, 100% { box-shadow: 0 0 10px #00ff88, 0 0 20px rgba(0, 255, 136, 0.4); }
    50% { box-shadow: 0 0 15px #00ff88, 0 0 30px rgba(0, 255, 136, 0.6); }
}

.sb-status-text {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.55rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #00ff88 !important;
}

.sb-brand-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.55rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #6e7681 !important;
    margin-bottom: 10px !important;
}

.sb-brand-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #e6edf3 !important;
    letter-spacing: -0.02em !important;
    display: flex;
    align-items: center;
    gap: 10px;
}

.sb-brand-title span { 
    background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sb-brand-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(0, 255, 136, 0.1));
    border: 1px solid rgba(0, 212, 255, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 4px 15px rgba(0, 212, 255, 0.2);
}

.sb-brand-sub {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important;
    color: #6e7681 !important;
    margin-top: 8px !important;
    letter-spacing: 0.02em !important;
}

/* ===== NAVIGATION SECTION ===== */
.sb-nav-section {
    padding: 0 16px;
}

.sb-nav-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.52rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #484f58 !important;
    padding: 20px 8px 12px !important;
    display: flex;
    align-items: center;
    gap: 8px;
}

.sb-nav-label::before {
    content: '//';
    color: #00d4ff;
    font-weight: 700;
}

/* ===== NAV BUTTONS ===== */
section[data-testid="stSidebar"] button[kind="secondary"] {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 12px 12px 0 !important;
    padding: 14px 18px 14px 20px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #8b949e !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    margin: 3px 8px 3px 0 !important;
    position: relative;
    overflow: hidden;
}

/* Hover glow effect */
section[data-testid="stSidebar"] button[kind="secondary"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, rgba(0, 212, 255, 0.08) 0%, transparent 100%);
    opacity: 0;
    transition: opacity 0.25s ease;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover::before {
    opacity: 1;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(0, 212, 255, 0.06) !important;
    color: #e6edf3 !important;
    border-left-color: #00d4ff !important;
    transform: translateX(4px);
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.1) !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:focus,
section[data-testid="stSidebar"] button[kind="secondary"]:active {
    background: linear-gradient(90deg, rgba(0, 212, 255, 0.12) 0%, rgba(0, 255, 136, 0.06) 100%) !important;
    color: #00d4ff !important;
    border-left-color: #00d4ff !important;
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.15), inset 0 0 20px rgba(0, 212, 255, 0.05) !important;
}

/* ===== DIVIDER ===== */
.sb-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.2), rgba(0, 255, 136, 0.1), transparent);
    margin: 24px 16px;
}

/* ===== SIDEBAR FOOTER ===== */
.sb-footer {
    padding: 20px 24px;
    margin-top: auto;
    border-top: 1px solid rgba(0, 212, 255, 0.08);
    background: linear-gradient(180deg, transparent, rgba(0, 212, 255, 0.02));
}

.sb-footer-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.sb-footer-label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.55rem !important;
    font-weight: 500 !important;
    color: #484f58 !important;
    letter-spacing: 0.1em !important;
}

.sb-footer-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: rgba(0, 212, 255, 0.08);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 20px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.5rem !important;
    color: #00d4ff !important;
}

.sb-footer-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 6px #00ff88;
}

/* Sidebar scrollbar */
section[data-testid="stSidebar"]::-webkit-scrollbar { width: 4px; }
section[data-testid="stSidebar"]::-webkit-scrollbar-track { background: transparent; }
section[data-testid="stSidebar"]::-webkit-scrollbar-thumb { 
    background: linear-gradient(180deg, #00d4ff, #00ff88); 
    border-radius: 4px; 
}
section[data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover { 
    background: #00d4ff; 
}

/* ===== GLOBAL DARK THEME OVERRIDES ===== */
/* Make all Streamlit elements dark */
.stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li {
    color: #e6edf3 !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: rgba(22, 27, 34, 0.8) !important;
    border: 1px solid rgba(139, 148, 158, 0.15) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    backdrop-filter: blur(20px) !important;
}
[data-testid="metric-container"] label {
    color: #8b949e !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important;
}

/* Buttons */
.stButton > button {
    background: rgba(0, 212, 255, 0.1) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    color: #00d4ff !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(0, 212, 255, 0.2) !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3) !important;
}

/* Inputs and selects */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stMultiSelect > div > div > div,
.stDateInput > div > div > input {
    background: rgba(22, 27, 34, 0.8) !important;
    border: 1px solid rgba(139, 148, 158, 0.2) !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}
.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus-within {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(22, 27, 34, 0.6) !important;
    border: 2px dashed rgba(0, 212, 255, 0.3) !important;
    border-radius: 12px !important;
    padding: 24px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00d4ff !important;
    background: rgba(0, 212, 255, 0.05) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(22, 27, 34, 0.6) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid rgba(139, 148, 158, 0.15) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8b949e !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: rgba(0, 212, 255, 0.15) !important;
    color: #00d4ff !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: rgba(22, 27, 34, 0.8) !important;
    border: 1px solid rgba(139, 148, 158, 0.15) !important;
    border-radius: 12px !important;
    color: #e6edf3 !important;
}
.streamlit-expanderContent {
    background: rgba(22, 27, 34, 0.6) !important;
    border: 1px solid rgba(139, 148, 158, 0.1) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
}

/* DataFrames / Tables */
.stDataFrame, [data-testid="stDataFrame"] {
    background: rgba(22, 27, 34, 0.8) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(139, 148, 158, 0.15) !important;
}
.stDataFrame th {
    background: rgba(0, 212, 255, 0.1) !important;
    color: #00d4ff !important;
}
.stDataFrame td {
    color: #e6edf3 !important;
    border-color: rgba(139, 148, 158, 0.1) !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #00d4ff, #00ff88) !important;
}

/* Alert boxes */
.stAlert {
    background: rgba(22, 27, 34, 0.8) !important;
    border: 1px solid rgba(139, 148, 158, 0.2) !important;
    border-radius: 12px !important;
}

/* Success message */
.stSuccess {
    background: rgba(0, 255, 136, 0.1) !important;
    border: 1px solid rgba(0, 255, 136, 0.3) !important;
    color: #00ff88 !important;
}

/* Warning message */
.stWarning {
    background: rgba(255, 184, 0, 0.1) !important;
    border: 1px solid rgba(255, 184, 0, 0.3) !important;
    color: #ffb800 !important;
}

/* Error message */
.stError {
    background: rgba(244, 63, 94, 0.1) !important;
    border: 1px solid rgba(244, 63, 94, 0.3) !important;
    color: #f43f5e !important;
}

/* Info message */
.stInfo {
    background: rgba(0, 212, 255, 0.1) !important;
    border: 1px solid rgba(0, 212, 255, 0.3) !important;
    color: #00d4ff !important;
}

/* Plotly charts dark theme */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}

/* Selectbox dropdown */
[data-baseweb="popover"] {
    background: #161b22 !important;
    border: 1px solid rgba(139, 148, 158, 0.2) !important;
    border-radius: 8px !important;
}
[data-baseweb="menu"] {
    background: #161b22 !important;
}
[data-baseweb="menu"] li {
    color: #e6edf3 !important;
}
[data-baseweb="menu"] li:hover {
    background: rgba(0, 212, 255, 0.1) !important;
}

/* Labels */
.stTextInput label, .stSelectbox label, .stMultiSelect label, .stDateInput label, .stFileUploader label {
    color: #8b949e !important;
    font-weight: 500 !important;
}

/* Checkbox and radio */
.stCheckbox label, .stRadio label {
    color: #e6edf3 !important;
}

/* ===== HIDE EXPANDER ARROW TEXT FALLBACK ===== */
/* Aggressively hide "arrow_down" / "arrow_up" text from expander icons */
section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stMarkdownContainer"] + div,
section[data-testid="stSidebar"] [data-testid="stExpander"] summary span:not([data-testid="stMarkdownContainer"]):not(.st-emotion-cache-1wbqy5l) {
    display: none !important;
}

/* Hide the icon text that appears after the label */
section[data-testid="stSidebar"] [data-testid="stExpander"] summary > div {
    display: flex !important;
    align-items: center !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary > div > span:last-child {
    display: none !important;
}

/* Target st-emotion-cache classes that hold the arrow text */
section[data-testid="stSidebar"] .st-emotion-cache-p5msec,
section[data-testid="stSidebar"] .st-emotion-cache-1wbqy5l,
section[data-testid="stSidebar"] [data-testid="stExpanderToggleIcon"] {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    font-size: 0 !important;
}

/* Hide any element containing arrow_down/arrow_up text via font-size trick */
section[data-testid="stSidebar"] details[data-testid="stExpander"] summary span {
    font-size: 0 !important;
}
section[data-testid="stSidebar"] details[data-testid="stExpander"] summary span p,
section[data-testid="stSidebar"] details[data-testid="stExpander"] summary [data-testid="stMarkdownContainer"] p {
    font-size: 0.7rem !important;
}

/* Style the expander nicely */
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(22, 27, 34, 0.6) !important;
    border: 1px solid rgba(0, 212, 255, 0.15) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    margin: 8px 12px !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    background: rgba(0, 212, 255, 0.05) !important;
    padding: 12px 16px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    color: #8b949e !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
    background: rgba(0, 212, 255, 0.1) !important;
    color: #00d4ff !important;
}

section[data-testid="stSidebar"] [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: rgba(13, 17, 23, 0.8) !important;
    padding: 12px 16px !important;
}
</style>
""", unsafe_allow_html=True)

# Session state for active page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar brand with enhanced styling
st.sidebar.markdown("""
<div class="sb-brand">
    <div class="sb-status">
        <div class="sb-status-dot"></div>
        <span class="sb-status-text">System Online</span>
    </div>
    <div class="sb-brand-label">SOC Platform</div>
    <div class="sb-brand-title">
        <div class="sb-brand-icon">&#128737;</div>
        Cyber<span>Pulse</span>
    </div>
    <div class="sb-brand-sub">Enterprise Security Analytics</div>
</div>
<div class="sb-nav-label">Navigation</div>
""", unsafe_allow_html=True)

# Nav buttons
NAV = [
    ("Home", "Home"),
    ("Info", "Info"),
    ("Dashboard", "Dashboard"),
    ("Upload", "Upload"),
    ("Compute KPI", "Compute KPI"),
]
for key, label in NAV:
    if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True):
        st.session_state.page = key

# Sidebar footer with enhanced styling
st.sidebar.markdown("""
<hr class="sb-divider">
<div class="sb-footer">
    <div class="sb-footer-content">
        <span class="sb-footer-label">CYBERPULSE</span>
        <span class="sb-footer-badge">
            <span class="sb-footer-dot"></span>
            v1.0
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Route
page = st.session_state.page
if page == "Home":
    show_home()

elif page == "Info":
    show_info()

elif page == "Dashboard":
    show_dashboard()

elif page == "Upload":
    show_upload()

elif page == "Compute KPI":
    show_compute_kpi()
