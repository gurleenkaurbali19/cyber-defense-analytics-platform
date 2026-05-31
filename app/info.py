import streamlit as st
import os

def show_info():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SAMPLE_FILES = {
        "CrowdStrike Falcon": os.path.join(BASE_DIR, "Data", "SampleFiles", "falcon_sample.xlsx"),
        "Cyble":              os.path.join(BASE_DIR, "Data", "SampleFiles", "cyble_sample.xlsx"),
        "SIEM":               os.path.join(BASE_DIR, "Data", "SampleFiles", "siem_sample.xlsx"),
        "Trend Vision":       os.path.join(BASE_DIR, "Data", "SampleFiles", "trend_sample.xlsx"),
        "Netskope":           os.path.join(BASE_DIR, "Data", "SampleFiles", "netskope_sample.xlsx"),
        "Com Olho":           os.path.join(BASE_DIR, "Data", "SampleFiles", "comolho_sample.xlsx"),
    }

    TOOL_META = {
        "CrowdStrike Falcon": ("🛡", "#2563EB", "#EFF6FF", "#BFDBFE", "EDR · Endpoint Detection & Response"),
        "Cyble":              ("🌐", "#7C3AED", "#F5F3FF", "#DDD6FE", "Threat Intelligence · Dark Web"),
        "SIEM":               ("🔐", "#EF4444", "#FEF2F2", "#FECACA", "Security Information & Event Management"),
        "Trend Vision":       ("📧", "#F59E0B", "#FFFBEB", "#FDE68A", "Email & Cloud Threat Protection"),
        "Netskope":           ("🔗", "#10B981", "#F0FDF4", "#A7F3D0", "Endpoint & Network Security"),
        "Com Olho":           ("🛠", "#14B8A6", "#F0FDFA", "#99F6E4", "Vulnerability Management · Bug Bounty"),
    }

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    .stApp { background: #F0F2F7 !important; }
    .main .block-container { padding-top: 1.8rem !important; max-width: 1100px; }

    @keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
    @keyframes fadeIn { from{opacity:0} to{opacity:1} }
    @keyframes pulse  { 0%,100%{box-shadow:0 0 0 0 rgba(37,99,235,0.3)} 50%{box-shadow:0 0 0 7px rgba(37,99,235,0)} }
    @keyframes drift  { 0%,100%{transform:translateY(0) translateX(0)} 50%{transform:translateY(-10px) translateX(5px)} }

    /* ── PAGE HEADER ── */
    .pg-header {
        background:#FFFFFF;
        border-radius:24px;
        padding:0;
        display:grid;
        grid-template-columns:1fr 260px;
        overflow:hidden;
        box-shadow:0 4px 6px rgba(0,0,0,0.04),0 16px 40px rgba(0,0,0,0.07);
        margin-bottom:18px;
        opacity:0; animation:fadeUp 0.7s ease forwards 0.05s;
        min-height:220px;
    }
    .pg-header-left {
        padding:40px 48px;
        position:relative; overflow:hidden;
    }
    .pg-header-left::before {
        content:"";
        position:absolute; inset:0;
        background:
            radial-gradient(ellipse 300px 220px at 90% 20%, rgba(37,99,235,0.06),transparent),
            radial-gradient(ellipse 200px 180px at 10% 80%, rgba(124,58,237,0.05),transparent);
        pointer-events:none;
    }
    .pg-header-right {
        background:linear-gradient(145deg,#0F172A,#1a2744);
        display:flex; align-items:center; justify-content:center;
        position:relative; overflow:hidden;
    }
    .pg-header-right::before {
        content:""; position:absolute;
        top:-40px; right:-40px;
        width:160px; height:160px;
        border:1px solid rgba(59,130,246,0.12); border-radius:50%;
    }
    .pg-header-right::after {
        content:""; position:absolute;
        top:-20px; right:-20px;
        width:100px; height:100px;
        border:1px solid rgba(59,130,246,0.07); border-radius:50%;
    }
    .pg-arch-visual {
        font-family:'Inter',monospace; font-size:0.72rem;
        color:#475569; line-height:2.1;
        position:relative; z-index:1;
    }
    .pg-arch-visual .arch-step {
        display:block; color:#94A3B8; letter-spacing:0.04em;
        transition:color 0.2s;
    }
    .pg-arch-visual .arch-step.hi { color:#60A5FA; font-weight:600; }
    .pg-arch-visual .arch-arrow { color:#1E3A5F; display:block; }

    .pg-eyebrow {
        font-family:'Inter',sans-serif; font-size:0.65rem; font-weight:700;
        letter-spacing:0.14em; text-transform:uppercase; color:#2563EB;
        margin-bottom:12px; position:relative; z-index:1;
        display:flex; align-items:center; gap:8px;
    }
    .pg-dot {
        width:7px; height:7px; background:#2563EB;
        border-radius:50%; animation:pulse 2s ease infinite;
    }
    .pg-title {
        font-family:'Space Grotesk',sans-serif; font-weight:700;
        font-size:2rem; color:#0F172A; letter-spacing:-0.02em;
        line-height:1.15; margin-bottom:12px; position:relative; z-index:1;
    }
    .pg-title span { color:#2563EB; }
    .pg-desc {
        font-family:'Inter',sans-serif; font-size:0.88rem; color:#64748B;
        line-height:1.75; max-width:440px; position:relative; z-index:1;
    }
    .pg-desc strong { color:#334155; font-weight:600; }

    /* ── SECTION LABEL ── */
    .sec {
        font-family:'Inter',sans-serif; font-size:0.62rem; font-weight:700;
        letter-spacing:0.14em; text-transform:uppercase; color:#94A3B8;
        margin:22px 0 12px; display:flex; align-items:center; gap:10px;
        opacity:0; animation:fadeIn 0.5s ease forwards 0.5s;
    }
    .sec::after { content:""; flex:1; height:1px; background:#DDE1E8; }

    /* ── WORKFLOW STEPS ── */
    .wf-grid {
        display:grid; grid-template-columns:repeat(4,1fr); gap:12px;
        opacity:0; animation:fadeUp 0.6s ease forwards 0.3s;
    }
    .wf-card {
        background:#FFFFFF; border-radius:18px; padding:22px 18px 18px;
        border:1.5px solid #F1F5F9;
        box-shadow:0 1px 3px rgba(0,0,0,0.04),0 6px 16px rgba(0,0,0,0.04);
        transition:all 0.22s ease; position:relative; overflow:hidden;
    }
    .wf-card::after {
        content:""; position:absolute; top:0; left:0; right:0; height:3px;
        background:linear-gradient(90deg,var(--wa),var(--wb));
        transform:scaleX(0); transform-origin:left; transition:transform 0.3s ease;
    }
    .wf-card:hover::after { transform:scaleX(1); }
    .wf-card:hover { transform:translateY(-4px); box-shadow:0 8px 12px rgba(0,0,0,0.06),0 20px 40px rgba(0,0,0,0.08); }
    .wf-num {
        font-family:'Space Grotesk',sans-serif; font-weight:700;
        font-size:1.7rem; color:#EEF0F4; line-height:1; margin-bottom:10px;
    }
    .wf-pill {
        display:inline-block; font-family:'Inter',sans-serif;
        font-size:0.6rem; font-weight:700; letter-spacing:0.1em;
        text-transform:uppercase; padding:3px 10px; border-radius:20px;
        background:var(--wpb); color:var(--wpc); margin-bottom:10px;
    }
    .wf-title {
        font-family:'Space Grotesk',sans-serif; font-weight:600;
        font-size:0.88rem; color:#1E293B; margin-bottom:5px;
    }
    .wf-desc { font-family:'Inter',sans-serif; font-size:0.77rem; color:#64748B; line-height:1.6; }

    /* ── TOOL GRID ── */
    .tgrid {
        display:grid; grid-template-columns:repeat(3,1fr); gap:12px;
        opacity:0; animation:fadeUp 0.6s ease forwards 0.4s;
    }
    .tc {
        background:#FFFFFF; border-radius:18px; padding:20px 22px;
        border:1.5px solid #F1F5F9;
        box-shadow:0 1px 3px rgba(0,0,0,0.04),0 6px 16px rgba(0,0,0,0.04);
        transition:all 0.22s ease; cursor:default; position:relative; overflow:hidden;
    }
    .tc::before {
        content:""; position:absolute; inset:0; border-radius:18px; opacity:0;
        background:radial-gradient(ellipse 140px 100px at 90% 10%, var(--tg),transparent);
        transition:opacity 0.3s;
    }
    .tc:hover::before { opacity:1; }
    .tc:hover { transform:translateY(-5px); border-color:var(--tb);
                box-shadow:0 8px 12px rgba(0,0,0,0.05),0 20px 40px rgba(0,0,0,0.09); }
    .tc-top { display:flex; align-items:center; gap:12px; margin-bottom:10px; }
    .tc-icon-wrap {
        width:38px; height:38px; border-radius:11px;
        background:var(--ti); display:flex; align-items:center;
        justify-content:center; font-size:1rem; flex-shrink:0;
        position:relative; z-index:1;
    }
    .tc-name {
        font-family:'Space Grotesk',sans-serif; font-weight:600;
        font-size:0.88rem; color:#1E293B; position:relative; z-index:1;
    }
    .tc-cat {
        font-family:'Inter',sans-serif; font-size:0.65rem; color:#94A3B8;
        text-transform:uppercase; letter-spacing:0.05em;
        position:relative; z-index:1;
    }
    .tc-bar {
        height:2px; border-radius:2px; margin-top:12px;
        background:linear-gradient(90deg,var(--tc),transparent);
        transform:scaleX(0.25); transform-origin:left; transition:transform 0.3s ease;
        position:relative; z-index:1;
    }
    .tc:hover .tc-bar { transform:scaleX(1); }

    /* ── DOWNLOADS ── */
    .dl-grid {
        display:grid; grid-template-columns:repeat(3,1fr); gap:12px;
        opacity:0; animation:fadeUp 0.6s ease forwards 0.5s;
    }
    .dl-card {
        background:#FFFFFF; border-radius:18px; padding:20px 22px;
        border:1.5px solid #F1F5F9;
        box-shadow:0 1px 3px rgba(0,0,0,0.04),0 6px 16px rgba(0,0,0,0.04);
        display:flex; align-items:center; gap:14px;
        transition:all 0.2s ease;
    }
    .dl-card:hover { transform:translateY(-3px); box-shadow:0 6px 10px rgba(0,0,0,0.05),0 16px 32px rgba(0,0,0,0.08); }
    .dl-icon {
        width:40px; height:40px; border-radius:11px;
        background:var(--di); display:flex; align-items:center;
        justify-content:center; font-size:1rem; flex-shrink:0;
    }
    .dl-name {
        font-family:'Space Grotesk',sans-serif; font-weight:600;
        font-size:0.84rem; color:#1E293B; flex:1;
    }
    .dl-cat {
        font-family:'Inter',sans-serif; font-size:0.63rem; color:#94A3B8;
        text-transform:uppercase; letter-spacing:0.05em; margin-top:2px;
    }
    .dl-missing {
        font-family:'Inter',sans-serif; font-size:0.7rem;
        color:#EF4444; font-weight:500;
    }

    /* Streamlit download button override */
    .stDownloadButton > button {
        background: #F8FAFC !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 10px !important;
        color: #475569 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        padding: 6px 16px !important;
        transition: all 0.18s !important;
        white-space: nowrap !important;
    }
    .stDownloadButton > button:hover {
        background: #EFF6FF !important;
        border-color: #BFDBFE !important;
        color: #1D4ED8 !important;
        transform: translateY(-1px) !important;
    }

    /* ── TECH + FOOTER ── */
    .tech-row {
        display:grid; grid-template-columns:1fr auto; gap:12px; margin-top:4px;
        opacity:0; animation:fadeUp 0.5s ease forwards 0.6s;
    }
    .tech-card {
        background:#FFFFFF; border-radius:18px; padding:22px 24px;
        border:1.5px solid #F1F5F9;
        box-shadow:0 1px 3px rgba(0,0,0,0.04),0 6px 16px rgba(0,0,0,0.04);
    }
    .tech-lbl {
        font-family:'Inter',sans-serif; font-size:0.6rem; font-weight:700;
        letter-spacing:0.14em; text-transform:uppercase; color:#94A3B8; margin-bottom:12px;
    }
    .tech-chips { display:flex; flex-wrap:wrap; gap:7px; }
    .tech-chip {
        background:#F8FAFC; border:1px solid #E9EEF4; border-radius:8px;
        padding:5px 13px; font-family:'Inter',sans-serif;
        font-size:0.72rem; font-weight:500; color:#475569;
        transition:all 0.16s;
    }
    .tech-chip:hover { background:#EFF6FF; border-color:#BFDBFE; color:#1D4ED8; }
    .footer-card {
        background:linear-gradient(145deg,#0F172A,#162032);
        border-radius:18px; padding:22px 28px;
        min-width:200px; position:relative; overflow:hidden;
        box-shadow:0 4px 6px rgba(0,0,0,0.1),0 16px 36px rgba(0,0,0,0.18);
        display:flex; flex-direction:column; justify-content:center;
    }
    .footer-card::before {
        content:""; position:absolute; top:-30px; right:-30px;
        width:120px; height:120px;
        background:radial-gradient(circle,rgba(59,130,246,0.15),transparent 65%);
        border-radius:50%;
    }
    .footer-lbl {
        font-family:'Inter',sans-serif; font-size:0.56rem; font-weight:700;
        letter-spacing:0.16em; text-transform:uppercase; color:#2D4A6E;
        margin-bottom:8px; position:relative; z-index:1;
    }
    .footer-name {
        font-family:'Space Grotesk',sans-serif; font-weight:700;
        font-size:1rem; color:#F1F5F9; position:relative; z-index:1;
    }
    .footer-name span { color:#60A5FA; }
    .footer-sub {
        font-family:'Inter',sans-serif; font-size:0.6rem; color:#2D4A6E;
        margin-top:6px; position:relative; z-index:1; letter-spacing:0.04em;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── PAGE HEADER ────────────────────────────────────────────
    st.markdown("""
    <div class="pg-header">
      <div class="pg-header-left">
        <div class="pg-eyebrow"><span class="pg-dot"></span>Platform Documentation</div>
        <div class="pg-title">Cyber<span>Defense</span><br>Info Center</div>
        <div class="pg-desc">
          A <strong>unified SOC analytics platform</strong> — upload security exports,
          compute KPIs automatically, and visualize trends across 6 integrated tools
          from a single executive dashboard.
        </div>
      </div>
      <div class="pg-header-right">
        <div class="pg-arch-visual">
          <span class="arch-step">📄 Excel File</span>
          <span class="arch-arrow">    ↓</span>
          <span class="arch-step">↑  Upload Module</span>
          <span class="arch-arrow">    ↓</span>
          <span class="arch-step hi">⊡  Raw Tables (MySQL)</span>
          <span class="arch-arrow">    ↓</span>
          <span class="arch-step">⚙  KPI Engine</span>
          <span class="arch-arrow">    ↓</span>
          <span class="arch-step hi">⊞  kpi_master</span>
          <span class="arch-arrow">    ↓</span>
          <span class="arch-step">▦  Dashboard</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── WORKFLOW ────────────────────────────────────────────────
    st.markdown('<div class="sec">Workflow</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="wf-grid">
      <div class="wf-card" style="--wa:#2563EB;--wb:#60A5FA;--wpb:#EFF6FF;--wpc:#1D4ED8">
        <div class="wf-num">01</div>
        <div class="wf-pill">Download</div>
        <div class="wf-title">Get Sample File</div>
        <div class="wf-desc">Download a sample Excel file for any tool to test the full pipeline end-to-end.</div>
      </div>
      <div class="wf-card" style="--wa:#7C3AED;--wb:#A78BFA;--wpb:#F5F3FF;--wpc:#5B21B6">
        <div class="wf-num">02</div>
        <div class="wf-pill">Upload</div>
        <div class="wf-title">Ingest Data</div>
        <div class="wf-desc">Upload your Excel export. Duplicate detection prevents re-processing the same file.</div>
      </div>
      <div class="wf-card" style="--wa:#10B981;--wb:#34D399;--wpb:#F0FDF4;--wpc:#065F46">
        <div class="wf-num">03</div>
        <div class="wf-pill">Compute</div>
        <div class="wf-title">Generate KPIs</div>
        <div class="wf-desc">Select your upload ID and run the KPI engine. Results store in kpi_master automatically.</div>
      </div>
      <div class="wf-card" style="--wa:#F59E0B;--wb:#FCD34D;--wpb:#FFFBEB;--wpc:#92400E">
        <div class="wf-num">04</div>
        <div class="wf-pill">Visualize</div>
        <div class="wf-title">Explore Dashboard</div>
        <div class="wf-desc">Filter by date range. Charts and KPIs render live for every tool in dedicated tabs.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SUPPORTED TOOLS ─────────────────────────────────────────
    st.markdown('<div class="sec">Supported Security Tools</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tgrid">
      <div class="tc" style="--tc:#2563EB;--tb:#BFDBFE;--ti:#EFF6FF;--tg:rgba(219,234,254,0.55)">
        <div class="tc-top"><div class="tc-icon-wrap">🛡</div><div><div class="tc-name">CrowdStrike Falcon</div><div class="tc-cat">EDR · Endpoint Detection</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#7C3AED;--tb:#DDD6FE;--ti:#F5F3FF;--tg:rgba(237,233,254,0.55)">
        <div class="tc-top"><div class="tc-icon-wrap">🌐</div><div><div class="tc-name">Cyble</div><div class="tc-cat">Threat Intel · Dark Web</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#EF4444;--tb:#FECACA;--ti:#FEF2F2;--tg:rgba(254,226,226,0.55)">
        <div class="tc-top"><div class="tc-icon-wrap">🔐</div><div><div class="tc-name">SIEM</div><div class="tc-cat">Security Event Management</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#F59E0B;--tb:#FDE68A;--ti:#FFFBEB;--tg:rgba(253,243,208,0.55)">
        <div class="tc-top"><div class="tc-icon-wrap">📧</div><div><div class="tc-name">Trend Vision</div><div class="tc-cat">Email · Cloud Protection</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#10B981;--tb:#A7F3D0;--ti:#F0FDF4;--tg:rgba(209,250,229,0.55)">
        <div class="tc-top"><div class="tc-icon-wrap">🔗</div><div><div class="tc-name">Netskope</div><div class="tc-cat">Endpoint · Network Security</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#14B8A6;--tb:#99F6E4;--ti:#F0FDFA;--tg:rgba(204,251,241,0.55)">
        <div class="tc-top"><div class="tc-icon-wrap">🛠</div><div><div class="tc-name">Com Olho</div><div class="tc-cat">Vulnerability · Bug Bounty</div></div></div>
        <div class="tc-bar"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SAMPLE DOWNLOADS ────────────────────────────────────────
    st.markdown('<div class="sec">Sample Files</div>', unsafe_allow_html=True)
    st.markdown('<div class="dl-grid">', unsafe_allow_html=True)

    tools_list = list(SAMPLE_FILES.items())
    # Render 2 per row using columns
    for i in range(0, len(tools_list), 3):
        row = tools_list[i:i+3]
        cols = st.columns(3)
        for col, (tool, filepath) in zip(cols, row):
            icon, color, bg, border, cat = TOOL_META[tool]
            with col:
                st.markdown(f"""
                <div class="dl-card" style="--di:{bg};">
                  <div class="dl-icon" style="background:{bg};">{icon}</div>
                  <div>
                    <div class="dl-name">{tool}</div>
                    <div class="dl-cat">{cat.split('·')[0].strip()}</div>
                  </div>
                """, unsafe_allow_html=True)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="↓ Download",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_{tool}"
                        )
                else:
                    st.markdown('<div class="dl-missing">⚠ File not found</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ── TECH STACK + FOOTER ─────────────────────────────────────
    st.markdown('<div class="sec">Tech Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-row">
      <div class="tech-card">
        <div class="tech-lbl">Built With</div>
        <div class="tech-chips">
          <span class="tech-chip">🐍 Python 3</span>
          <span class="tech-chip">⚡ Streamlit</span>
          <span class="tech-chip">🗄 MySQL</span>
          <span class="tech-chip">📊 Plotly</span>
          <span class="tech-chip">🐼 Pandas</span>
          <span class="tech-chip">🔌 mysql-connector-python</span>
          <span class="tech-chip">📋 openpyxl</span>
          <span class="tech-chip">🔐 hashlib</span>
        </div>
      </div>
      <div class="footer-card">
        <div class="footer-lbl">Built by</div>
        <div class="footer-name">Gurleen Kaur <span>Bali</span></div>
        <div class="footer-sub">Cyber Defense SOC Platform</div>
      </div>
    </div>
    """, unsafe_allow_html=True)