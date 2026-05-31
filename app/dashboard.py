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
    "FALCON":       {"primary": "#2563EB", "accent": "#60A5FA", "palette": ["#1D4ED8","#2563EB","#3B82F6","#60A5FA","#93C5FD","#BFDBFE"]},
    "CYBLE":        {"primary": "#7C3AED", "accent": "#C4B5FD", "palette": ["#5B21B6","#6D28D9","#7C3AED","#8B5CF6","#A78BFA","#C4B5FD"]},
    "SIEM":         {"primary": "#EF4444", "accent": "#FCA5A5", "palette": ["#991B1B","#B91C1C","#DC2626","#EF4444","#F87171","#FCA5A5"]},
    "TREND_VISION": {"primary": "#F59E0B", "accent": "#FCD34D", "palette": ["#92400E","#B45309","#D97706","#F59E0B","#FBBF24","#FCD34D"]},
    "NETSKOPE":     {"primary": "#10B981", "accent": "#6EE7B7", "palette": ["#064E3B","#047857","#059669","#10B981","#34D399","#6EE7B7"]},
    "COM_OLHO":     {"primary": "#14B8A6", "accent": "#5EEAD4", "palette": ["#134E4A","#0F766E","#0D9488","#14B8A6","#2DD4BF","#5EEAD4"]},
}

SEVERITY_ORDER = ["Critical","HIGH","MEDIUM","LOW","Minor","Major","High (P2)","Medium (P3)","Low (P4)"]

def gt(tool): return TOOL_THEME.get(tool, {"primary":"#4F46E5","accent":"#93C5FD","palette":["#4F46E5"]})

# ─────────────────────────────
# DYNAMIC COLOR MAPS
# ─────────────────────────────
SEVERITY_COLORS = {
    "critical":    "#991B1B",
    "high":        "#DC2626",
    "high (p2)":   "#DC2626",
    "major":       "#F97316",
    "medium":      "#F59E0B",
    "medium (p3)": "#F59E0B",
    "minor":       "#38BDF8",
    "low":         "#22C55E",
    "low (p4)":    "#22C55E",
}

def severity_palette(df, col="dimension_value"):
    return [SEVERITY_COLORS.get(str(v).lower(), "#94A3B8") for v in df[col]]

RESOLUTION_COLORS = {
    "true_positive":  "#22C55E",
    "true positive":  "#22C55E",
    "false_positive": "#EF4444",
    "false positive": "#EF4444",
}

def resolution_palette(df, col="dimension_value"):
    return [RESOLUTION_COLORS.get(str(v).lower(), "#94A3B8") for v in df[col]]

SLA_COLORS = {
    "on time":  "#22C55E",
    "breached": "#EF4444",
}

def sla_palette(df, col="dimension_value"):
    return [SLA_COLORS.get(str(v).lower(), "#94A3B8") for v in df[col]]

SECURITY_STATUS_COLORS = {
    "enabled":  "#22C55E",
    "disabled": "#EF4444",
}

def security_status_palette(df, col="dimension_value"):
    return [SECURITY_STATUS_COLORS.get(str(v).lower(), "#94A3B8") for v in df[col]]

DELIVERY_COLORS = {
    "quarantined": "#22C55E",
    "delivered":   "#EF4444",
    "blocked":     "#F59E0B",
}

def delivery_palette(df, col="dimension_value"):
    return [DELIVERY_COLORS.get(str(v).lower(), "#94A3B8") for v in df[col]]

TUNNEL_COLORS = {
    "tunnel up":   "#22C55E",
    "tunnel down": "#EF4444",
}

def tunnel_palette(df, col="dimension_value"):
    return [TUNNEL_COLORS.get(str(v).lower(), "#94A3B8") for v in df[col]]

def fuzzy_sum(df, col, pattern):
    if df.empty: return 0
    mask = df[col].str.lower().str.contains(pattern.lower(), na=False)
    return int(df[mask]["kpi_value"].sum())

def dim_sum(df, col, value):
    if df.empty: return 0
    mask = df[col].str.lower() == value.lower()
    return int(df[mask]["kpi_value"].sum())

# ─────────────────────────────
# CSS
# ─────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

    /* ── Metric cards ── */
    .m-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1.5px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 14px rgba(0,0,0,0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .m-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    }
    .m-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--mc);
    }
    .m-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.62rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .m-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--mc);
        line-height: 1;
    }

    /* ── Tool section header ── */
    .tool-header {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #FFFFFF;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 18px;
        border: 1.5px solid #F1F5F9;
        border-left: 4px solid var(--th);
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 14px rgba(0,0,0,0.05);
    }
    .tool-header-icon {
        font-size: 1.4rem;
        line-height: 1;
    }
    .tool-header-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.01em;
    }
    .tool-header-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    .tool-header-badge {
        margin-left: auto;
        background: var(--tb);
        color: var(--tc);
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 20px;
    }

    /* ── Section divider ── */
    .sec-div {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #94A3B8;
        margin: 20px 0 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .sec-div::after {
        content: "";
        flex: 1;
        height: 1px;
        background: #E9EEF4;
    }

    /* ── Insight box ── */
    .insight-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 3px solid var(--ib);
        border-radius: 12px;
        padding: 14px 18px;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        color: #475569;
        line-height: 1.75;
    }
    .insight-box b { color: #1E293B; }

    /* ── Chart wrapper ── */
    .chart-card {
        background: #FFFFFF;
        border-radius: 14px;
        border: 1.5px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 14px rgba(0,0,0,0.04);
        overflow: hidden;
        margin-bottom: 4px;
    }

    /* ── Tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: #FFFFFF;
        border-radius: 12px;
        padding: 4px;
        border: 1.5px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px;
        padding: 8px 18px;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        color: #64748B;
        background: transparent;
        border: none;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #1E293B;
        background: #F8FAFC;
    }
    .stTabs [aria-selected="true"] {
        background: #0F172A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
    .stTabs [data-baseweb="tab-border"]    { display: none !important; }

    /* ── Dashboard page title ── */
    .dash-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.02em;
        border-left: 4px solid #3B82F6;
        padding-left: 14px;
        margin-bottom: 4px;
    }
    .dash-sub {
        font-family: 'Inter', sans-serif;
        font-size: 0.88rem;
        color: #64748B;
        margin-bottom: 20px;
        padding-left: 18px;
    }

    /* ── Sidebar filter section ── */
    .filter-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #334D6E;
        margin-bottom: 6px;
    }
    </style>
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
def metric_row(items):
    cols = st.columns(len(items))
    for c, (l, v, col) in zip(cols, items):
        c.markdown(f"""
        <div class="m-card" style="--mc:{col}">
            <div class="m-label">{l}</div>
            <div class="m-value">{v}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

# ─────────────────────────────
# TOOL HEADER
# ─────────────────────────────
def tool_header(icon, name, sub, badge_text, primary, badge_bg, badge_color):
    st.markdown(f"""
    <div class="tool-header" style="--th:{primary}">
        <div class="tool-header-icon">{icon}</div>
        <div>
            <div class="tool-header-name">{name}</div>
            <div class="tool-header-sub">{sub}</div>
        </div>
        <div class="tool-header-badge" style="--tb:{badge_bg};--tc:{badge_color}">{badge_text}</div>
    </div>
    """, unsafe_allow_html=True)

def section_div(label):
    st.markdown(f'<div class="sec-div">{label}</div>', unsafe_allow_html=True)

# ─────────────────────────────
# CHART BUILDERS
# ─────────────────────────────
CHART_LAYOUT = dict(
    template="plotly_white",
    margin=dict(l=16, r=16, t=40, b=16),
    font=dict(family="Inter, sans-serif", size=11, color="#475569"),
    paper_bgcolor="white",
    plot_bgcolor="white",
    title_font=dict(family="Space Grotesk, sans-serif", size=13, color="#1E293B"),
    title_x=0,
    title_pad=dict(l=4),

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
        marker["colorscale"] = [[0, "#E9EEF4"], [1, color]]
    if horizontal:
        fig = go.Figure(go.Bar(
            y=df[x], x=df[y], orientation="h",
            marker=marker,
            text=df[y], textposition="outside",
        ))
        fig.update_layout(yaxis=dict(autorange="reversed"))
    else:
        fig = go.Figure(go.Bar(
            x=df[x], y=df[y],
            marker=marker,
            text=df[y], textposition="outside",
        ))
    fig.update_layout(height=290, **CHART_LAYOUT, title=title)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#F1F5F9", gridwidth=1)
    st.plotly_chart(fig, use_container_width=True, key=f"bar_{key}")


def donut_chart(df, labels, values, title, colors, key=""):
    if df.empty: st.info("No data available"); return
    fig = go.Figure(go.Pie(
        labels=df[labels], values=df[values], hole=0.65,
        marker=dict(colors=colors[:len(df)], line=dict(color="white", width=2.5)),
        textinfo="label+percent",
        textfont=dict(size=10),
        pull=[0.05] + [0] * (len(df) - 1),
        sort=False,
    ))
    total_val = int(df[values].sum())
    fig.add_annotation(
        text=f"<b>{total_val}</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color="#0F172A", family="Space Grotesk"),
    )
    fig.update_layout(height=290, **CHART_LAYOUT, title=title,
                      showlegend=True,
                      legend=dict(orientation="v", x=1.02, y=0.5,
                                  font=dict(size=10)))
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
        marker=dict(color=color, size=6, line=dict(color="white", width=2)),
        fill="tozeroy",
        fillcolor=f"rgba({r},{g},{b},0.08)",
        name="Volume",
    ))
    fig.update_layout(height=270, **CHART_LAYOUT, title=title)
    fig.update_xaxes(showgrid=False, tickformat="%b %d")
    fig.update_yaxes(gridcolor="#F1F5F9", gridwidth=1)
    st.plotly_chart(fig, use_container_width=True, key=f"area_{key}")


def stacked_bar(df_list, names, x_col, y_col, title, colors, key=""):
    if not df_list: st.info("No data available"); return
    fig = go.Figure()
    for df, name, color in zip(df_list, names, colors):
        if not df.empty:
            fig.add_trace(go.Bar(name=name, x=df[x_col], y=df[y_col],
                                 marker_color=color, marker_line_width=0))
    fig.update_layout(barmode="stack", height=290, **CHART_LAYOUT, title=title,
                      legend=dict(orientation="h", y=-0.18))
    st.plotly_chart(fig, use_container_width=True, key=f"stacked_{key}")


def gauge_chart(value, max_val, title, color, key=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title=dict(text=title, font=dict(size=12, color="#64748B", family="Inter")),
        gauge=dict(
            axis=dict(range=[0, max_val], tickwidth=1, tickcolor="#E2E8F0",
                      tickfont=dict(size=9, color="#94A3B8")),
            bar=dict(color=color, thickness=0.65),
            bgcolor="white",
            borderwidth=0,
            steps=[
                dict(range=[0, max_val * 0.4], color="#F8FAFC"),
                dict(range=[max_val * 0.4, max_val * 0.7], color="#F1F5F9"),
                dict(range=[max_val * 0.7, max_val], color="#FEE2E2"),
            ],
        ),
        number=dict(font=dict(size=30, color=color, family="Space Grotesk"),
                    suffix="" ),
    ))
    fig.update_layout(height=230, margin=dict(l=24, r=24, t=48, b=10),
                      paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True, key=f"gauge_{key}")


def funnel_chart(df, x, y, title, color, key=""):
    if df.empty: st.info("No data available"); return
    fig = go.Figure(go.Funnel(
        y=df[x], x=df[y],
        textinfo="value+percent initial",
        marker=dict(color=color),
        textfont=dict(size=11),
    ))
    fig.update_layout(height=290, **CHART_LAYOUT, title=title)
    st.plotly_chart(fig, use_container_width=True, key=f"funnel_{key}")


def treemap_chart(df, labels, values, title, color, key=""):
    if df.empty: st.info("No data available"); return
    fig = px.treemap(df, path=[labels], values=values,
                     color=values,
                     color_continuous_scale=["#F8FAFC", color],
                     title=title)
    fig.update_layout(height=290, margin=dict(l=10, r=10, t=40, b=10),
                      font=dict(family="Inter, sans-serif", size=11),
                      title_font=dict(family="Space Grotesk, sans-serif", size=13))
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig, use_container_width=True, key=f"tree_{key}")


def bullet_chart(value, target, label, color, key=""):
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        value=value,
        delta=dict(reference=target, relative=False,
                   increasing=dict(color="#EF4444"),
                   decreasing=dict(color="#22C55E")),
        gauge=dict(
            shape="bullet",
            axis=dict(range=[0, max(value, target) * 1.2]),
            threshold=dict(line=dict(color=color, width=2), value=target),
            bgcolor="#F8FAFC",
            bar=dict(color=color),
        ),
        title=dict(text=label, font=dict(size=11, color="#64748B", family="Inter")),
        number=dict(font=dict(size=20, color=color, family="Space Grotesk")),
    ))
    fig.update_layout(height=110, margin=dict(l=10, r=24, t=28, b=8),
                      paper_bgcolor="white")
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
                      legend=dict(orientation="h", y=-0.18))
    st.plotly_chart(fig, use_container_width=True, key=f"dual_{key}")


def heatmap_like_bar(df, x, y, title, palette, key=""):
    if df.empty: st.info("No data available"); return
    fig = go.Figure(go.Bar(
        x=df[x], y=df[y],
        marker_color=palette[:len(df)],
        marker_line_width=0,
        text=df[y], textposition="outside",
        opacity=0.9,
    ))
    fig.update_layout(height=290, **CHART_LAYOUT, title=title)
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#F1F5F9")
    st.plotly_chart(fig, use_container_width=True, key=f"heat_{key}")


# ─────────────────────────────
# FALCON
# ─────────────────────────────
def show_falcon(df):
    t = gt("FALCON")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#128737;", "CrowdStrike Falcon", "Endpoint Detection & Response",
                "EDR", p, "#EFF6FF", "#1D4ED8")

    total    = int(scalar(df, "Total Alerts"))
    open_a   = int(scalar(df, "Open Alerts"))
    mttr     = round(scalar(df, "MTTR (Hours)"), 2)
    high     = int(scalar(df, "High Severity Alerts"))
    res_rate = round(scalar(df, "Resolution Rate") * 100, 1)

    metric_row([
        ("Total Alerts",  total,           p),
        ("Open Alerts",   open_a,          "#F59E0B"),
        ("MTTR (hrs)",    mttr,            a),
        ("High Severity", high,            "#EF4444"),
        ("Resolution %",  f"{res_rate}%",  "#22C55E"),
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
                "Threat Intel", p, "#F5F3FF", "#5B21B6")

    total = int(scalar(df, "Total Alerts"))
    ratio = round(scalar(df, "Open/Resolved Ratio"), 2)

    metric_row([
        ("Total Alerts",        total, p),
        ("Open/Resolved Ratio", ratio, "#EF4444" if ratio > 1 else "#22C55E"),
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
                "Events", p, "#FEF2F2", "#B91C1C")

    total   = int(scalar(df, "Total Alerts"))
    tp      = int(scalar(df, "True Positives"))
    fp      = int(scalar(df, "False Positives"))
    fp_rate = round((fp / total * 100) if total else 0, 1)

    metric_row([
        ("Total Alerts",    total,        p),
        ("True Positives",  tp,           "#22C55E"),
        ("False Positives", fp,           "#EF4444"),
        ("FP Rate",         f"{fp_rate}%","#F59E0B"),
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
                    "#EF4444" if fp_rate > 50 else "#F59E0B", key="siem_fp_gauge")
    with c4:
        val = breakdown(df, "Alerts", "validation_status")
        bar_chart(val, "dimension_value", "kpi_value", "Validation Status",
                  p, key="siem_val")

    section_div("TP vs FP Volume")
    bullet_chart(tp, total, "True Positives vs Total",  "#22C55E", key="siem_tp_bullet")
    bullet_chart(fp, total, "False Positives vs Total", "#EF4444", key="siem_fp_bullet")


# ─────────────────────────────
# TREND VISION
# ─────────────────────────────
def show_trend(df):
    t = gt("TREND_VISION")
    p, a, pal = t["primary"], t["accent"], t["palette"]
    tool_header("&#128231;", "Trend Vision", "Email & Cloud Threat Protection",
                "Email Security", p, "#FFFBEB", "#92400E")

    total = int(scalar(df, "Total Threats"))
    sta   = breakdown(df, "Threats", "status")
    quarantined = dim_sum(sta, "dimension_value", "quarantined")
    delivered   = dim_sum(sta, "dimension_value", "delivered")
    tt    = breakdown(df, "Threats", "threat_type")
    phish = fuzzy_sum(tt, "dimension_value", "phish")

    metric_row([
        ("Total Threats",    total,       p),
        ("Phishing",         phish,       "#EF4444"),
        ("Quarantined",      quarantined, "#22C55E"),
        ("Delivered (Risk)", delivered,   "#F59E0B"),
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
                    "#22C55E" if q_rate > 40 else "#EF4444", key="tv_qrate")
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
                "Network", p, "#F0FDF4", "#065F46")

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
        ("Security Enabled",  enabled,       "#22C55E"),
        ("Security Disabled", disabled,      "#EF4444"),
        ("Tunnel Up",         tup,           a),
        ("Coverage %",        f"{coverage}%","#22C55E" if coverage > 80 else "#F59E0B"),
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
                    "#22C55E" if coverage > 80 else "#EF4444", key="nsk_cov")

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
                "Vuln Mgmt", p, "#F0FDFA", "#0F766E")

    total       = int(scalar(df, "Total Vulnerabilities"))
    avg_age     = round(scalar(df, "Average Vulnerability Age"), 1)
    reward      = int(scalar(df, "Total Reward Amount"))
    sla_df      = breakdown(df, "SLA Status", "sla_status")
    breached    = dim_sum(sla_df, "dimension_value", "breached")
    breach_rate = round((breached / total * 100) if total else 0, 1)

    metric_row([
        ("Total Vulns",    total,            p),
        ("SLA Breached",   breached,         "#EF4444"),
        ("Avg Age (Days)", avg_age,          "#F59E0B"),
        ("Total Rewards",  f"&#8377;{reward:,}", a),
        ("Breach Rate",    f"{breach_rate}%","#EF4444" if breach_rate > 40 else "#22C55E"),
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
                    "#EF4444" if breach_rate > 40 else "#F59E0B", key="co_breach_gauge")
    with c6:
        bullet_chart(avg_age, 30, "Avg Vulnerability Age vs 30-Day Target",
                     "#F59E0B", key="co_age_bullet")


# ─────────────────────────────
# MAIN
# ─────────────────────────────
def show_dashboard():
    inject_css()

    st.markdown('<div class="dash-title">Security Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dash-sub">Executive overview across all integrated security tools.</div>', unsafe_allow_html=True)

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