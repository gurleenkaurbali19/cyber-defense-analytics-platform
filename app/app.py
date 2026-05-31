import streamlit as st

from home import show_home
from upload import show_upload
from compute import show_compute_kpi
from dashboard import show_dashboard
from info import show_info

st.set_page_config(
    page_title="Cyber Defense Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

/* Background */
.stApp { background: #F0F2F7 !important; }
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* Hide hamburger menu and footer */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Hide the collapse button that appears INSIDE the sidebar at the top */
section[data-testid="stSidebar"] > div:first-child > div:first-child button {
    display: none !important;
}
/* Also target by test id in case Streamlit version differs */
[data-testid="stSidebarNav"] { display: none !important; }
button[data-testid="baseButton-headerNoPadding"] { display: none !important; }

/* Sidebar base */
section[data-testid="stSidebar"] {
    background: #0B1A2E !important;
    border-right: 1px solid #1E3A5F !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* All sidebar text white */
section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar nav buttons */
section[data-testid="stSidebar"] button[kind="secondary"] {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 !important;
    padding: 10px 20px !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    color: #94A3B8 !important;
    transition: all 0.15s ease !important;
    margin: 0 !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: rgba(255,255,255,0.06) !important;
    color: #E2E8F0 !important;
    border-left-color: #3B82F6 !important;
}
section[data-testid="stSidebar"] button[kind="secondary"]:focus {
    background: rgba(59,130,246,0.15) !important;
    color: #FFFFFF !important;
    border-left-color: #3B82F6 !important;
    box-shadow: none !important;
}

/* Sidebar scrollbar */
section[data-testid="stSidebar"]::-webkit-scrollbar { width: 3px; }
section[data-testid="stSidebar"]::-webkit-scrollbar-track { background: #0B1A2E; }
section[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: #1E3A5F; border-radius: 2px; }

/* Sidebar brand block */
.sb-brand {
    padding: 24px 20px 18px;
    border-bottom: 1px solid #1E3A5F;
    margin-bottom: 8px;
}
.sb-brand-label {
    font-size: 0.6rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #3B82F6 !important;
    margin-bottom: 6px;
}
.sb-brand-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #F1F5F9 !important;
    letter-spacing: -0.01em;
}
.sb-brand-title span { color: #3B82F6 !important; }
.sb-brand-sub {
    font-size: 0.62rem;
    color: #334D6E !important;
    margin-top: 4px;
    letter-spacing: 0.04em;
}
.sb-nav-label {
    font-size: 0.58rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #334D6E !important;
    padding: 4px 20px 8px;
}
.sb-divider {
    border: none;
    border-top: 1px solid #1E3A5F;
    margin: 10px 0;
}
.sb-footer {
    padding: 12px 20px;
    font-size: 0.6rem;
    color: #2D4A6E !important;
    letter-spacing: 0.06em;
}
</style>
""", unsafe_allow_html=True)

# Session state for active page
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar brand
st.sidebar.markdown("""
<div class="sb-brand">
    <div class="sb-brand-label">SOC Platform</div>
    <div class="sb-brand-title">Cyber<span>Defense</span></div>
    <div class="sb-brand-sub">Security Analytics</div>
</div>
<div class="sb-nav-label">Navigation</div>
""", unsafe_allow_html=True)

# Nav buttons
NAV = [
    ("Home", "△ Home"),
    ("Info", "ⓘ Info"),
    ("Dashboard", "⊞ Dashboard"),
    ("Upload", "↑ Upload"),
    ("Compute KPI", "⊙ Compute KPI"),
]
for key, label in NAV:
    if st.sidebar.button(label, key=f"nav_{key}", use_container_width=True):
        st.session_state.page = key

# Sidebar footer
st.sidebar.markdown("""
<hr class="sb-divider">
<div class="sb-footer">CYBER DEFENSE &nbsp;·&nbsp; v1.0</div>
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