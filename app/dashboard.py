
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from Database.database_connection import get_connection

# ─────────────────────────────
# TOOL COLOR THEMES
# ─────────────────────────────
TOOL_THEME = {
    "FALCON":       {"primary": "#3B82F6", "accent": "#60A5FA", "glow": "rgba(59,130,246,0.4)", "palette": ["#1D4ED8","#2563EB","#3B82F6","#60A5FA","#93C5FD","#BFDBFE"]},
    "CYBLE":        {"primary": "#A78BFA", "accent": "#C4B5FD", "glow": "rgba(167,139,250,0.4)", "palette": ["#5B21B6","#6D28D9","#7C3AED","#8B5CF6","#A78BFA","#C4B5FD"]},
    "SIEM":         {"primary": "#F87171", "accent": "#FCA5A5", "glow": "rgba(248,113,113,0.4)", "palette": ["#991B1B","#B91C1C","#DC2626","#EF4444","#F87171","#FCA5A5"]},
    "TREND_VISION": {"primary": "#FBBF24", "accent": "#FCD34D", "glow": "rgba(251,191,36,0.4)", "palette": ["#92400E","#B45309","#D97706","#F59E0B","#FBBF24","#FCD34D"]},
    "NETSKOPE":     {"primary": "#34D399", "accent": "#6EE7B7", "glow": "rgba(52,211,153,0.4)", "palette": ["#064E3B","#047857","#059669","#10B981","#34D399","#6EE7B7"]},
    "COM_OLHO":     {"primary": "#2DD4BF", "accent": "#5EEAD4", "glow": "rgba(45,212,191,0.4)", "palette": ["#134E4A","#0F766E","#0D9488","#14B8A6","#2DD4BF","#5EEAD4"]},
}

SEVERITY_ORDER = ["Critical","HIGH","MEDIUM","LOW","Minor","Major","High (P2)","Medium (P3)","Low (P4)"]

def gt(tool): return TOOL_THEME.get(tool, {"primary":"#818CF8","accent":"#93C5FD","glow":"rgba(129,140,248,0.4)","palette":["#4F46E5"]})

# ─────────────────────────────
# DYNAMIC COLOR MAPS
# ─────────────────────────────
SEVERITY_COLORS = {
    "critical":    "#EF4444",
    "high":        "#F87171",
    "high (p2)":   "#F87171",
    "major":       "#FB923C",
    "medium":      "#FBBF24",
    "medium (p3)": "#FBBF24",
    "minor":       "#38BDF8",
    "low":         "#4ADE80",
    "low (p4)":    "#4ADE80",
}

def severity_palette(df, col="dimension_value"):
    return [SEVERITY_COLORS.get(str(v).lower(), "#64748B") for v in df[col]]

RESOLUTION_COLORS = {
    "true_positive":  "#4ADE80",
    "true positive":  "#4ADE80",
    "false_positive": "#F87171",
    "false positive": "#F87171",
}

def resolution_palette(df, col="dimension_value"):
    return [RESOLUTION_COLORS.get(str(v).lower(), "#64748B") for v in df[col]]

SLA_COLORS = {
    "on time":  "#4ADE80",
    "breached": "#F87171",
}

def sla_palette(df, col="dimension_value"):
    return [SLA_COLORS.get(str(v).lower(), "#64748B") for v in df[col]]

SECURITY_STATUS_COLORS = {
    "enabled":  "#4ADE80",
    "disabled": "#F87171",
}

def security_status_palette(df, col="dimension_value"):
    return [SECURITY_STATUS_COLORS.get(str(v).lower(), "#64748B") for v in df[col]]

DELIVERY_COLORS = {
    "quarantined": "#4ADE80",
    "delivered":   "#F87171",
    "blocked":     "#FBBF24",
}

def delivery_palette(df, col="dimension_value"):
    return [DELIVERY_COLORS.get(str(v).lower(), "#64748B") for v in df[col]]

TUNNEL_COLORS = {
    "tunnel up":   "#4ADE80",
    "tunnel down": "#F87171",
}

def tunnel_palette(df, col="dimension_value"):
    return [TUNNEL_COLORS.get(str(v).lower(), "#64748B") for v in df[col]]

def fuzzy_sum(df, col, pattern):
    if df.empty: return 0
    mask = df[col].str.lower().str.contains(pattern.lower(), na=False)
    return int(df[mask]["kpi_value"].sum())

def dim_sum(df, col, value):
    if df.empty: return 0
    mask = df[col].str.lower() == value.lower()
    return int(df[mask]["kpi_value"].sum())

# ─────────────────────────────
# CSS - DARK SOC THEME
# ─────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@600;700&display=swap');

    /* ── Global Dark Theme ── */
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f1a 100%) !important;
    }
    
    /* ── Animated Background Elements ── */
    .bg-effects {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    /* Scanlines */
    .scanlines {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 255, 0.01) 2px,
            rgba(0, 255, 255, 0.01) 4px
        );
        animation: scanlines 8s linear infinite;
    }
    @keyframes scanlines {
        0% { transform: translateY(0); }
        100% { transform: translateY(4px); }
    }
    
    /* Cyber Grid */
    .cyber-grid {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridPulse 4s ease-in-out infinite;
    }
    @keyframes gridPulse {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.6; }
    }
    
    /* Floating Particles */
    .particles {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
    }
    .particle {
        position: absolute;
        width: 2px;
        height: 2px;
        background: #00ffff;
        border-radius: 50%;
        animation: float 20s infinite linear;
        opacity: 0.4;
    }
    .particle:nth-child(1) { left: 10%; animation-delay: 0s; animation-duration: 25s; }
    .particle:nth-child(2) { left: 20%; animation-delay: 2s; animation-duration: 20s; }
    .particle:nth-child(3) { left: 30%; animation-delay: 4s; animation-duration: 28s; }
    .particle:nth-child(4) { left: 40%; animation-delay: 1s; animation-duration: 22s; }
    .particle:nth-child(5) { left: 50%; animation-delay: 3s; animation-duration: 26s; }
    .particle:nth-child(6) { left: 60%; animation-delay: 5s; animation-duration: 24s; }
    .particle:nth-child(7) { left: 70%; animation-delay: 2s; animation-duration: 21s; }
    .particle:nth-child(8) { left: 80%; animation-delay: 4s; animation-duration: 27s; }
    .particle:nth-child(9) { left: 90%; animation-delay: 1s; animation-duration: 23s; }
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.4; }
        90% { opacity: 0.4; }
        100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
    }

    /* ── Metric cards ── */
    .m-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 15, 25, 0.95));
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 
            0 4px 24px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.05) inset,
            0 0 30px var(--glow) inset;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    .m-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--mc), transparent);
        opacity: 0.8;
    }
    .m-card::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, transparent 40%, var(--glow) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .m-card:hover {
        transform: translateY(-4px);
        border-color: var(--mc);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.5),
            0 0 40px var(--glow),
            0 0 60px var(--glow);
    }
    .m-card:hover::after { opacity: 0.15; }
    .m-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #64748B;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .m-label::before {
        content: "//";
        color: var(--mc);
        opacity: 0.6;
    }
    .m-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--mc);
        line-height: 1;
        text-shadow: 0 0 20px var(--glow);
    }
    .m-card .pulse-dot {
        position: absolute;
        top: 16px;
        right: 16px;
        width: 8px;
        height: 8px;
        background: var(--mc);
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; box-shadow: 0 0 0 0 var(--glow); }
        50% { opacity: 0.6; box-shadow: 0 0 0 8px transparent; }
    }

    /* ── Tool section header ── */
    .tool-header {
        display: flex;
        align-items: center;
        gap: 16px;
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 25, 0.98));
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 4px solid var(--th);
        box-shadow: 
            0 4px 24px rgba(0, 0, 0, 0.4),
            0 0 40px var(--thglow);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    .tool-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, var(--thglow), transparent 50%);
        opacity: 0.1;
    }
    .tool-header::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, var(--thglow), transparent 30%);
        animation: borderRotate 8s linear infinite;
        opacity: 0.3;
    }
    @keyframes borderRotate {
        100% { transform: rotate(360deg); }
    }
    .tool-header-icon {
        font-size: 1.8rem;
        line-height: 1;
        filter: drop-shadow(0 0 10px var(--th));
        z-index: 1;
    }
    .tool-header-content {
        z-index: 1;
    }
    .tool-header-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #F1F5F9;
        letter-spacing: -0.01em;
        text-shadow: 0 0 20px var(--thglow);
    }
    .tool-header-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        color: #64748B;
        margin-top: 4px;
    }
    .tool-header-badge {
        margin-left: auto;
        background: linear-gradient(135deg, var(--tb), rgba(15, 23, 42, 0.9));
        color: var(--tc);
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid var(--tc);
        box-shadow: 0 0 20px var(--thglow);
        z-index: 1;
    }
    .tool-header-status {
        display: flex;
        align-items: center;
        gap: 8px;
        z-index: 1;
        margin-left: 12px;
    }
    .status-dot {
        width: 10px;
        height: 10px;
        background: #4ADE80;
        border-radius: 50%;
        animation: statusPulse 2s ease-in-out infinite;
        box-shadow: 0 0 10px rgba(74, 222, 128, 0.5);
    }
    @keyframes statusPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.2); }
    }
    .status-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #4ADE80;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* ── Section divider ── */
    .sec-div {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #00ffff;
        margin: 28px 0 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .sec-div::before {
        content: ">";
        color: #00ffff;
        animation: blink 1s step-end infinite;
    }
    @keyframes blink {
        50% { opacity: 0; }
    }
    .sec-div::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(0, 255, 255, 0.5), transparent);
    }

    /* ── Insight box ── */
    .insight-box {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 15, 25, 0.95));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left: 3px solid var(--ib);
        border-radius: 14px;
        padding: 18px 22px;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #94A3B8;
        line-height: 1.8;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    .insight-box b { color: #F1F5F9; }

    /* ── Chart wrapper ── */
    .chart-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 15, 25, 0.95));
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        overflow: hidden;
        margin-bottom: 8px;
        backdrop-filter: blur(10px);
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 25, 0.98));
        border-radius: 14px;
        padding: 6px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 500;
        color: #64748B;
        background: transparent;
        border: none;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #00ffff;
        background: rgba(0, 255, 255, 0.05);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.15), rgba(0, 255, 255, 0.05)) !important;
        color: #00ffff !important;
        font-weight: 600 !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.2) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"]    { display: none !important; }

    /* ── Dashboard page title ── */
    .dash-header {
        position: relative;
        padding: 24px 0;
        margin-bottom: 24px;
    }
    .dash-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #F1F5F9;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .dash-title-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.5));
    }
    .dash-title-text {
        background: linear-gradient(135deg, #F1F5F9, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }
    .dash-title-glow {
        color: #00ffff;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
        -webkit-text-fill-color: #00ffff;
    }
    .dash-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #64748B;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .dash-sub::before {
        content: "";
        width: 40px;
        height: 2px;
        background: linear-gradient(90deg, #00ffff, transparent);
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        color: #4ADE80;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-left: 12px;
    }
    .live-badge::before {
        content: "";
        width: 6px;
        height: 6px;
        background: #4ADE80;
        border-radius: 50%;
        animation: livePulse 1.5s ease-in-out infinite;
    }
    @keyframes livePulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }

    /* ── Sidebar styling ── */
    .filter-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #00ffff;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .filter-label::before {
        content: ">";
        opacity: 0.6;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0f; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #334155; }
    </style>
    
    <!-- Background Effects -->
    <div class="bg-effects">
        <div class="scanlines"></div>
        <div class="cyber-grid"></div>
        <div class="particles">
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
            <div class="particle"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────
# DATA
# ─────────────────────────────
@st.cache_data(ttl=120)
def load_kpi(tool, start_date=None, end_date=None):
    try:
        conn = get_connection()
        q = """SELECT kpi_name, kpi_value, kpi_dimension, dimension_value
               FROM kpi_master WHERE tool_name = %s"""
        params = [tool]
        if start_date and end_date:
            q += " AND start_date <= %s AND end_date >= %s"
            params += [str(end_date), str(start_date)]
        elif start_date:
            q += " AND end_date >= %s"; params.append(str(start_date))
        elif end_date:
            q += " AND start_date <= %s"; params.append(str(end_date))
        try:
            df = pd.read_sql(q, conn, params=params)
            return df
        finally:
            conn.close()
    except Exception as e:
        st.error(f"DB error: {e}"); return pd.DataFrame()

def scalar(df, k, default=0):
    r = df[(df["kpi_name"]==k) & (df["kpi_dimension"].isna()|(df["kpi_dimension"]==""))]
    return r["kpi_value"].iloc[0] if not r.empty else default

def breakdown(df, k, d):
    return df[(df["kpi_name"]==k) & (df["kpi_dimension"]==d)].copy()

# ─────────────────────────────
# METRIC ROW
# ─────────────────────────────
def metric_row(items, tool_glow="rgba(0,255,255,0.3)"):
    cols = st.columns(len(items))
    for c, (l, v, col) in zip(cols, items):
        # Calculate glow color from main color
        r, g, b = int(col[1:3], 16), int(col[3:5], 16), int(col[5:7], 16)
        glow = f"rgba({r},{g},{b},0.3)"
        c.markdown(f"""
        <div class="m-card" style="--mc:{col};--glow:{glow}">
            <div class="pulse-dot"></div>
            <div class="m-label">{l}</div>
            <div class="m-value">{v}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:20px'></div>", unsafe_allow_html=True)

# ─────────────────────────────
# TOOL HEADER
# ─────────────────────────────
def tool_header(icon, name, sub, badge_text, primary, badge_bg, badge_color):
    # Calculate glow from primary
    r, g, b = int(primary[1:3], 16), int(primary[3:5], 16), int(primary[5:7], 16)
    glow = f"rgba({r},{g},{b},0.3)"
    st.markdown(f"""
    <div class="tool-header" style="--th:{primary};--thglow:{glow}">
        <div class="tool-header-icon">{icon}</div>
        <div class="tool-header-content">
            <div class="tool-header-name">{name}</div>
            <div class="tool-header-sub">{sub}</div>
        </div>
        <div class="tool-header-status">
            <div class="status-dot"></div>
            <div class="status-text">Online</div>
        </div>
        <div class="tool-header-badge" style="--tb:{badge_bg};--tc:{badge_color}">{badge_text}</div>
    </div>
    """, unsafe_allow_html=True)

def section_div(label):
    st.markdown(f'<div class="sec-div">{label}</div>', unsafe_allow_html=True)

# ─────────────────────────────
# CHART BUILDERS - DARK THEME
# ─────────────────────────────
CHART_LAYOUT = dict(
    template="plotly_dark",
    margin=dict(l=20, r=20, t=50, b=20),
    font=dict(family="Inter, sans-serif", size=11, color="#94A3B8"),
    paper_bgcolor="rgba(15, 23, 42, 0.95)",
    plot_bgcolor="rgba(10, 15, 25, 0.9)",
    title_font=dict(family="Space Grotesk, sans-serif", size=14, color="#F1F5F9"),
    title_x=0,
    title_pad=dict(l=8),
)

def bar_chart(df, x, y, title, color, horizontal=False, key="", color_list=None):
    if df.empty: st.info("No data available"); return
    marker = dict(
        color=color_list if color_list else color,
        line=dict(width=0),
        opacity=0.9,
    )
    if not color_list:
        marker["color"] = df[y]
        marker["colorscale"] = [[0, "#1e293b"], [1, color]]
    if horizontal:
        fig = go.Figure(go.Bar(
            y=df[x], x=df[y], orientation="h",
            marker=marker,
            text=df[y], textposition="outside",
            textfont=dict(color="#94A3B8"),
        ))
        fig.update_layout(yaxis=dict(autorange="reversed"))
    else:
        fig = go.Figure(go.Bar(
            x=df[x], y=df[y],
            marker=marker,
            text=df[y], textposition="outside",
            textfont=dict(color="#94A3B8"),
        ))
    fig.update_layout(height=290, **CHART_LAYOUT, title=title)
    fig.update_xaxes(showgrid=False, color="#64748B")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", gridwidth=1, color="#64748B")
    st.plotly_chart(fig, use_container_width=True, key=f"bar_{key}")


def donut_chart(df, labels, values, title, colors, key=""):
    if df.empty: st.info("No data available"); return
    fig = go.Figure(go.Pie(
        labels=df[labels], values=df[values], hole=0.65,
        marker=dict(colors=colors[:len(df)], line=dict(color="rgba(15,23,42,0.95)", width=3)),
        textinfo="label+percent",
        textfont=dict(size=10, color="#F1F5F9"),
        pull=[0.05] + [0] * (len(df) - 1),
        sort=False,
    ))
    total_val = int(df[values].sum())
    fig.add_annotation(
        text=f"<b>{total_val}</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=22, color="#00ffff", family="Space Grotesk"),
    )
    fig.update_layout(height=290, **CHART_LAYOUT, title=title,
                      showlegend=True,
                      legend=dict(orientation="v", x=1.02, y=0.5,
                                  font=dict(size=10, color="#94A3B8")))
    st.plotly_chart(fig, use_container_width=True, key=f"donut_{key}")


def area_line_chart(df, x, y, title, color, key=""):
    if df.empty: st.info("No data available"); return
    df = df.copy()
    df[x] = pd.to_datetime(df[x], errors="coerce")
    df = df.dropna(subset=[x]).sort_values(x)
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x], y=df[y], mode="lines+markers",
        line=dict(color=color, width=2.5),
        marker=dict(color=color, size=7, line=dict(color="rgba(15,23,42,0.95)", width=2)),
        fill="tozeroy",
        fillcolor=f"rgba({r},{g},{b},0.15)",
        name="Volume",
    ))
    fig.update_layout(height=270, **CHART_LAYOUT, title=title)
    fig.update_xaxes(showgrid=False, tickformat="%b %d", color="#64748B")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", gridwidth=1, color="#64748B")
    st.plotly_chart(fig, use_container_width=True, key=f"area_{key}")


def stacked_bar(df_list, names, x_col, y_col, title, colors, key=""):
    if not df_list: st.info("No data available"); return
    fig = go.Figure()
    for df, name, color in zip(df_list, names, colors):
        if not df.empty:
            fig.add_trace(go.Bar(name=name, x=df[x_col], y=df[y_col],
                                 marker_color=color, marker_line_width=0))
    fig.update_layout(barmode="stack", height=290, **CHART_LAYOUT, title=title,
                      legend=dict(orientation="h", y=-0.18, font=dict(color="#94A3B8")))
    st.plotly_chart(fig, use_container_width=True, key=f"stacked_{key}")


def gauge_chart(value, max_val, title, color, key=""):
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=12, color="#94A3B8", family="Inter")),
        gauge=dict(
            axis=dict(range=[0, max_val], tickwidth=1, tickcolor="#334155",
                      tickfont=dict(size=9, color="#64748B")),
            bar=dict(color=color, thickness=0.65),
            bgcolor="rgba(15,23,42,0.9)",
            borderwidth=0,
            steps=[
                dict(range=[0, max_val * 0.4], color="rgba(30,41,59,0.8)"),
                dict(range=[max_val * 0.4, max_val * 0.7], color="rgba(51,65,85,0.6)"),
                dict(range=[max_val * 0.7, max_val], color=f"rgba({r},{g},{b},0.2)"),
            ],
        ),
        number=dict(font=dict(size=32, color=color, family="Space Grotesk"),
                    suffix="" ),
    ))
    fig.update_layout(height=230, margin=dict(l=24, r=24, t=48, b=10),
                      paper_bgcolor="rgba(15,23,42,0.95)")
    st.plotly_chart(fig, use_container_width=True, key=f"gauge_{key}")


def funnel_chart(df, x, y, title, color, key=""):
    if df.empty: st.info("No data available"); return
    fig = go.Figure(go.Funnel(
        y=df[x], x=df[y],
        textinfo="value+percent initial",
        marker=dict(color=color),
        textfont=dict(size=11, color="#F1F5F9"),
    ))
    fig.update_layout(height=290, **CHART_LAYOUT, title=title)
    st.plotly_chart(fig, use_container_width=True, key=f"funnel_{key}")


def treemap_chart(df, labels, values, title, color, key=""):
    if df.empty: st.info("No data available"); return
    fig = px.treemap(df, path=[labels], values=values,
                     color=values,
                     color_continuous_scale=["#1e293b", color],
                     title=title)
    fig.update_layout(height=290, margin=dict(l=10, r=10, t=50, b=10),
                      font=dict(family="Inter, sans-serif", size=11, color="#F1F5F9"),
                      title_font=dict(family="Space Grotesk, sans-serif", size=14, color="#F1F5F9"),
                      paper_bgcolor="rgba(15,23,42,0.95)")
    fig.update_traces(textinfo="label+value", textfont=dict(color="#F1F5F9"))
    st.plotly_chart(fig, use_container_width=True, key=f"tree_{key}")


def bullet_chart(value, target, label, color, key=""):
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        value=value,
        delta=dict(reference=target, relative=False,
                   increasing=dict(color="#F87171"),
                   decreasing=dict(color="#4ADE80")),
        gauge=dict(
            shape="bullet",
            axis=dict(range=[0, max(value, target) * 1.2], tickfont=dict(color="#64748B")),
            threshold=dict(line=dict(color=color, width=2), value=target),
            bgcolor="rgba(30,41,59,0.8)",
            bar=dict(color=color),
        ),
        title=dict(text=label, font=dict(size=11, color="#94A3B8", family="Inter")),
        number=dict(font=dict(size=22, color=color, family="Space Grotesk")),
    ))
    fig.update_layout(height=110, margin=dict(l=10, r=24, t=28, b=8),
                      paper_bgcolor="rgba(15,23,42,0.95)")
    st.plotly_chart(fig, use_container_width=True, key=f"bullet_{key}")


def dual_axis_chart(df1, df2, x, y, title, color1, color2, name1, name2, key=""):
    if df1.empty and df2.empty: st.info("No data available"); return
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if not df1.empty:
        fig.add_trace(go.Bar(name=name1, x=df1[x], y=df1[y],
                             marker_color=color1, opacity=0.8,
                             marker_line_width=0), secondary_y=False)
    if not df2.empty:
        fig.add_trace(go.Scatter(name=name2, x=df2[x], y=df2[y],
                                 mode="lines+markers",
                                 line=dict(color=color2, width=2.5)),
                      secondary_y=True)
    fig.update_layout(height=290, **CHART_LAYOUT, title=title,
                      legend=dict(orientation="h", y=-0.18, font=dict(color="#94A3B8")))
    st.plotly_chart(fig, use_container_width=True, key=f"dual_{key}")


def heatmap_like_bar(df, x, y, title, palette, key=""):
    if df.empty: st.info("No data available"); return
    fig = go.Figure(go.Bar(
        x=df[x], y=df[y],
        marker_color=palette[:len(df)],
        marker_line_width=0,
        text=df[y], textposition="outside",
        textfont=dict(color="#94A3B8"),
        opacity=0.9,
    ))
    fig.update_layout(height=290, **CHART_LAYOUT, title=title)
    fig.update_xaxes(showgrid=False, color="#64748B")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", color="#64748B")
    st.plotly_chart(fig, use_container_width=True, key=f"heat_{key}")


# ─────────────────────────────
# FALCON
# ─────────────────────────────
def show_falcon(df):
    t = gt("FALCON")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#128737;", "CrowdStrike Falcon", "Endpoint Detection & Response",
                "EDR", p, "rgba(59,130,246,0.2)", p)

    total    = int(scalar(df, "Total Alerts"))
    open_a   = int(scalar(df, "Open Alerts"))
    mttr     = round(scalar(df, "MTTR (Hours)"), 2)
    high     = int(scalar(df, "High Severity Alerts"))
    res_rate = round(scalar(df, "Resolution Rate") * 100, 1)

    metric_row([
        ("Total Alerts",  total,           p),
        ("Open Alerts",   open_a,          "#FBBF24"),
        ("MTTR (hrs)",    mttr,            a),
        ("High Severity", high,            "#F87171"),
        ("Resolution %",  f"{res_rate}%",  "#4ADE80"),
    ])

    section_div("Severity & Status")
    c1, c2 = st.columns(2)
    with c1:
        sev = breakdown(df, "Alerts", "severity")
        donut_chart(sev, "dimension_value", "kpi_value", "Severity Breakdown",
                    severity_palette(sev), key="fal_sev")
    with c2:
        sta = breakdown(df, "Alerts", "status")
        funnel_chart(sta, "dimension_value", "kpi_value", "Alert Status Funnel",
                     p, key="fal_funnel")

    section_div("Resolution & Response Time")
    c3, c4 = st.columns(2)
    with c3:
        res = breakdown(df, "Alerts", "resolution")
        donut_chart(res, "dimension_value", "kpi_value", "TP vs FP Resolution",
                    resolution_palette(res), key="fal_res")
    with c4:
        gauge_chart(mttr, max(mttr * 2, 24), "MTTR (Hours)", p, key="fal_mttr")

    section_div("Daily Volume Trend")
    daily = breakdown(df, "Daily Alerts", "date")
    area_line_chart(daily, "dimension_value", "kpi_value",
                    "Daily Alert Volume", p, key="fal_daily")


# ─────────────────────────────
# CYBLE
# ─────────────────────────────
def show_cyble(df):
    t = gt("CYBLE")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#127760;", "Cyble", "Threat Intelligence & Dark Web Monitoring",
                "Threat Intel", p, "rgba(167,139,250,0.2)", p)

    total = int(scalar(df, "Total Alerts"))
    ratio = round(scalar(df, "Open/Resolved Ratio"), 2)

    metric_row([
        ("Total Alerts",        total, p),
        ("Open/Resolved Ratio", ratio, "#F87171" if ratio > 1 else "#4ADE80"),
    ])

    section_div("Threat Severity & Status")
    c1, c2 = st.columns(2)
    with c1:
        sev = breakdown(df, "Alerts", "severity")
        donut_chart(sev, "dimension_value", "kpi_value", "Threat Severity",
                    severity_palette(sev), key="cyb_sev")
    with c2:
        sta = breakdown(df, "Alerts", "status")
        bar_chart(sta, "dimension_value", "kpi_value", "Open vs Resolved",
                  a, key="cyb_sta")

    section_div("Sources & Keywords")
    c3, c4 = st.columns(2)
    with c3:
        src = breakdown(df, "Alerts", "source")
        treemap_chart(src, "dimension_value", "kpi_value", "Threat Sources",
                      p, key="cyb_src")
    with c4:
        kw = breakdown(df, "Alerts", "keyword")
        bar_chart(kw, "dimension_value", "kpi_value", "Top Keywords",
                  a, horizontal=True, key="cyb_kw")

    section_div("Daily Volume Trend")
    daily = breakdown(df, "Daily Alerts", "date")
    area_line_chart(daily, "dimension_value", "kpi_value",
                    "Daily Threat Volume", p, key="cyb_daily")


# ─────────────────────────────
# SIEM
# ─────────────────────────────
def show_siem(df):
    t = gt("SIEM")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#128272;", "SIEM", "Security Information & Event Management",
                "Events", p, "rgba(248,113,113,0.2)", p)

    total   = int(scalar(df, "Total Alerts"))
    tp      = int(scalar(df, "True Positives"))
    fp      = int(scalar(df, "False Positives"))
    fp_rate = round((fp / total * 100) if total else 0, 1)

    metric_row([
        ("Total Alerts",    total,        p),
        ("True Positives",  tp,           "#4ADE80"),
        ("False Positives", fp,           "#F87171"),
        ("FP Rate",         f"{fp_rate}%","#FBBF24"),
    ])

    section_div("Severity & Alert Categories")
    c1, c2 = st.columns(2)
    with c1:
        sev = breakdown(df, "Alerts", "severity")
        donut_chart(sev, "dimension_value", "kpi_value", "Severity Distribution",
                    severity_palette(sev), key="siem_sev")
    with c2:
        atype = breakdown(df, "Alerts", "alert_type")
        heatmap_like_bar(atype, "dimension_value", "kpi_value",
                         "Alert Categories", pal, key="siem_atype")

    section_div("False Positive Analysis")
    c3, c4 = st.columns(2)
    with c3:
        gauge_chart(fp_rate, 100, "False Positive Rate (%)",
                    "#F87171" if fp_rate > 50 else "#FBBF24", key="siem_fp_gauge")
    with c4:
        val = breakdown(df, "Alerts", "validation_status")
        bar_chart(val, "dimension_value", "kpi_value", "Validation Status",
                  p, key="siem_val")

    section_div("TP vs FP Volume")
    bullet_chart(tp, total, "True Positives vs Total",  "#4ADE80", key="siem_tp_bullet")
    bullet_chart(fp, total, "False Positives vs Total", "#F87171", key="siem_fp_bullet")


# ─────────────────────────────
# TREND VISION
# ─────────────────────────────
def show_trend(df):
    t = gt("TREND_VISION")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#128231;", "Trend Vision", "Email & Cloud Threat Protection",
                "Email Security", p, "rgba(251,191,36,0.2)", p)

    total = int(scalar(df, "Total Threats"))
    sta   = breakdown(df, "Threats", "status")
    quarantined = dim_sum(sta, "dimension_value", "quarantined")
    delivered   = dim_sum(sta, "dimension_value", "delivered")
    tt    = breakdown(df, "Threats", "threat_type")
    phish = fuzzy_sum(tt, "dimension_value", "phish")

    metric_row([
        ("Total Threats",    total,       p),
        ("Phishing",         phish,       "#F87171"),
        ("Quarantined",      quarantined, "#4ADE80"),
        ("Delivered (Risk)", delivered,   "#FBBF24"),
    ])

    section_div("Threat Mix & Delivery")
    c1, c2 = st.columns(2)
    with c1:
        donut_chart(tt, "dimension_value", "kpi_value", "Threat Type Mix",
                    pal[:len(tt)], key="tv_type")
    with c2:
        donut_chart(sta, "dimension_value", "kpi_value", "Delivery Status",
                    delivery_palette(sta), key="tv_sta")

    section_div("Protection & Filters")
    pm = breakdown(df, "Threats", "protection_mode")
    sf = breakdown(df, "Threats", "security_filter")
    c3, c4 = st.columns(2)
    with c3:
        bar_chart(pm, "dimension_value", "kpi_value",
                  "Protection Mode (API vs INLINE)", p, key="tv_pm")
    with c4:
        bar_chart(sf, "dimension_value", "kpi_value",
                  "Security Filters Triggered", a, horizontal=True, key="tv_sf")

    section_div("Quarantine Rate & Summary")
    q_rate = round((quarantined / total * 100) if total else 0, 1)
    c5, c6 = st.columns([1, 2])
    with c5:
        gauge_chart(q_rate, 100, "Quarantine Rate (%)",
                    "#4ADE80" if q_rate > 40 else "#F87171", key="tv_qrate")
    with c6:
        st.markdown(f"""
        <div class="insight-box" style="--ib:{p}">
            <b>Threat Summary</b><br>
            &bull; {phish} phishing threats detected ({round(phish/total*100,1) if total else 0}% of total)<br>
            &bull; {quarantined} emails quarantined &mdash; {q_rate}% quarantine rate<br>
            &bull; {delivered} threats delivered to inbox (requires review)<br>
            &bull; Protection split: API vs INLINE modes active
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────
# NETSKOPE
# ─────────────────────────────
def show_netskope(df):
    t = gt("NETSKOPE")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#127760;", "Netskope", "Endpoint & Network Security",
                "Network", p, "rgba(52,211,153,0.2)", p)

    total    = int(scalar(df, "Total Devices"))
    sec      = breakdown(df, "Security Status", "internet_security_status")
    enabled  = dim_sum(sec, "dimension_value", "enabled")
    disabled = dim_sum(sec, "dimension_value", "disabled")
    tun      = breakdown(df, "Tunnel Status", "last_event")
    tup      = dim_sum(tun, "dimension_value", "tunnel up")
    tdown    = dim_sum(tun, "dimension_value", "tunnel down")
    coverage = round((enabled / total * 100) if total else 0, 1)

    metric_row([
        ("Total Devices",     total,         p),
        ("Security Enabled",  enabled,       "#4ADE80"),
        ("Security Disabled", disabled,      "#F87171"),
        ("Tunnel Up",         tup,           a),
        ("Coverage %",        f"{coverage}%","#4ADE80" if coverage > 80 else "#FBBF24"),
    ])

    section_div("OS & Security Status")
    c1, c2 = st.columns(2)
    with c1:
        os_d = breakdown(df, "Devices", "os_platform")
        donut_chart(os_d, "dimension_value", "kpi_value", "OS Platform Distribution",
                    pal[:len(os_d)], key="nsk_os")
    with c2:
        donut_chart(sec, "dimension_value", "kpi_value", "Security Status",
                    security_status_palette(sec), key="nsk_sec")

    section_div("Tunnel Status & Coverage")
    c3, c4 = st.columns(2)
    with c3:
        bar_chart(tun, "dimension_value", "kpi_value", "Tunnel Status",
                  p, key="nsk_tun", color_list=tunnel_palette(tun))
    with c4:
        gauge_chart(coverage, 100, "Security Coverage (%)",
                    "#4ADE80" if coverage > 80 else "#F87171", key="nsk_cov")

    section_div("Posture Summary")
    os_count = breakdown(df, "Devices", "os_platform")["dimension_value"].nunique() \
               if not breakdown(df, "Devices", "os_platform").empty else 0
    st.markdown(f"""
    <div class="insight-box" style="--ib:{p}">
        <b>Endpoint Posture Summary</b><br>
        &bull; {total} devices monitored across {os_count} OS platforms<br>
        &bull; Security coverage: <b>{coverage}%</b> ({enabled} enabled, {disabled} disabled)<br>
        &bull; Tunnel status: {tup} up / {tdown} down
        {"&nbsp;&mdash;&nbsp; &#9888; <b>" + str(tdown) + " devices with tunnel down</b>" if tdown > 0 else "&nbsp;&mdash;&nbsp; All tunnels operational"}
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────
# COM OLHO
# ─────────────────────────────
def show_com(df):
    t = gt("COM_OLHO")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#128296;", "Com Olho", "Vulnerability Management & Bug Bounty",
                "Vuln Mgmt", p, "rgba(45,212,191,0.2)", p)

    total       = int(scalar(df, "Total Vulnerabilities"))
    avg_age     = round(scalar(df, "Average Vulnerability Age"), 1)
    reward      = int(scalar(df, "Total Reward Amount"))
    sla_df      = breakdown(df, "SLA Status", "sla_status")
    breached    = dim_sum(sla_df, "dimension_value", "breached")
    breach_rate = round((breached / total * 100) if total else 0, 1)

    metric_row([
        ("Total Vulns",    total,            p),
        ("SLA Breached",   breached,         "#F87171"),
        ("Avg Age (Days)", avg_age,          "#FBBF24"),
        ("Total Rewards",  f"&#8377;{reward:,}", a),
        ("Breach Rate",    f"{breach_rate}%","#F87171" if breach_rate > 40 else "#4ADE80"),
    ])

    section_div("Severity & SLA Compliance")
    c1, c2 = st.columns(2)
    with c1:
        sev = breakdown(df, "Vulnerabilities", "severity")
        donut_chart(sev, "dimension_value", "kpi_value", "Severity Distribution",
                    severity_palette(sev), key="co_sev")
    with c2:
        donut_chart(sla_df, "dimension_value", "kpi_value", "SLA Compliance",
                    sla_palette(sla_df), key="co_sla")

    section_div("Vulnerability Types & Status")
    c3, c4 = st.columns(2)
    with c3:
        vtype = breakdown(df, "Vulnerabilities", "vulnerability_type")
        treemap_chart(vtype, "dimension_value", "kpi_value",
                      "Vulnerability Types", p, key="co_vtype")
    with c4:
        vstatus = breakdown(df, "Vulnerability Status", "status")
        bar_chart(vstatus, "dimension_value", "kpi_value",
                  "Vulnerability Status", a, key="co_vstatus")

    section_div("SLA Breach & Age Analysis")
    c5, c6 = st.columns(2)
    with c5:
        gauge_chart(breach_rate, 100, "SLA Breach Rate (%)",
                    "#F87171" if breach_rate > 40 else "#FBBF24", key="co_breach_gauge")
    with c6:
        bullet_chart(avg_age, 30, "Avg Vulnerability Age vs 30-Day Target",
                     "#FBBF24", key="co_age_bullet")


# ─────────────────────────────
# MAIN
# ─────────────────────────────
def show_dashboard():
    inject_css()

    # Dashboard Header
    st.markdown("""
    <div class="dash-header">
        <div class="dash-title">
            <span class="dash-title-icon">&#128737;</span>
            <span class="dash-title-text">Security</span>
            <span class="dash-title-glow">Dashboard</span>
            <span class="live-badge">Live</span>
        </div>
        <div class="dash-sub">Executive overview across all integrated security tools</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar filters
    st.sidebar.markdown('<div class="filter-label">Date Range</div>', unsafe_allow_html=True)
    start = st.sidebar.date_input("Start Date", value=None, label_visibility="collapsed")
    end   = st.sidebar.date_input("End Date",   value=None, label_visibility="collapsed")

    st.sidebar.markdown('<div class="filter-label" style="margin-top:14px">Tools</div>', unsafe_allow_html=True)
    tools = st.sidebar.multiselect(
        "Tools",
        ["Falcon", "Cyble", "SIEM", "Trend Vision", "Netskope", "Com Olho"],
        default=["Falcon", "Cyble", "SIEM", "Trend Vision", "Netskope", "Com Olho"],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")
    if st.sidebar.button("Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    with st.sidebar.expander("Debug Info"):
        sd = start.strftime("%Y-%m-%d") if start else None
        ed = end.strftime("%Y-%m-%d")   if end   else None
        st.caption(f"Start: {sd or 'none'}\nEnd: {ed or 'none'}")

    TOOL_MAP = {
        "Falcon":      "FALCON",
        "Cyble":       "CYBLE",
        "SIEM":        "SIEM",
        "Trend Vision":"TREND_VISION",
        "Netskope":    "NETSKOPE",
        "Com Olho":    "COM_OLHO",
    }

    sd = start.strftime("%Y-%m-%d") if start else None
    ed = end.strftime("%Y-%m-%d")   if end   else None
    data = {t: load_kpi(TOOL_MAP[t], sd, ed) for t in tools}

    render = {
        "Falcon":      show_falcon,
        "Cyble":       show_cyble,
        "SIEM":        show_siem,
        "Trend Vision":show_trend,
        "Netskope":    show_netskope,
        "Com Olho":    show_com,
    }

    if not tools:
        st.info("Select at least one tool from the sidebar to view the dashboard.")
        return

    tabs = st.tabs(tools)
    for tab, t in zip(tabs, tools):
        with tab:
            if data[t].empty:
                st.warning(f"No data for {t} in the selected date range.")
            else:
                try:
                    render[t](data[t])
                except Exception as e:
                    st.error(f"Error rendering {t}: {e}")
                    st.caption("Other tabs are unaffected. Try refreshing.")
