import streamlit as st

def show_home():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@600;700&display=swap');

    @keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

    .h-wrap { animation: fadeUp 0.5s ease forwards; }

    .h-eyebrow {
        display: inline-flex; align-items: center; gap: 7px;
        background: #EFF6FF; border: 1px solid #BFDBFE;
        border-radius: 20px; padding: 4px 12px; margin-bottom: 14px;
        font-family: 'Inter', sans-serif; font-size: 0.65rem;
        font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #1D4ED8;
    }
    .h-dot { width: 6px; height: 6px; border-radius: 50%; background: #3B82F6; }

    .h-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.6rem; font-weight: 700;
        color: #0F172A; letter-spacing: -0.03em; line-height: 1.1;
        margin-bottom: 14px;
    }
    .h-title span { color: #2563EB; }

    .h-desc {
        font-family: 'Inter', sans-serif; font-size: 0.93rem;
        color: #64748B; line-height: 1.8; max-width: 640px; margin-bottom: 28px;
    }
    .h-desc strong { color: #1E293B; }

    .h-stats {
        display: flex; gap: 0; margin-bottom: 40px;
    }
    .h-stat {
        padding-right: 28px; margin-right: 28px;
        border-right: 1px solid #E2E8F0;
    }
    .h-stat:last-child { border-right: none; }
    .h-stat-num {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem; font-weight: 700; color: #0F172A; line-height: 1;
    }
    .h-stat-num em { color: #2563EB; font-style: normal; font-size: 1.1rem; }
    .h-stat-lbl {
        font-family: 'Inter', sans-serif; font-size: 0.63rem;
        color: #94A3B8; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.08em; margin-top: 4px;
    }

    .sec {
        font-family: 'Inter', sans-serif; font-size: 0.6rem; font-weight: 700;
        letter-spacing: 0.15em; text-transform: uppercase; color: #94A3B8;
        margin: 32px 0 14px; display: flex; align-items: center; gap: 10px;
    }
    .sec::after { content: ""; flex: 1; height: 1px; background: #DDE1E8; }

    .tgrid {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;
        margin-bottom: 8px;
    }
    .tc {
        background: #FFFFFF; border-radius: 16px; padding: 20px;
        border: 1.5px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 14px rgba(0,0,0,0.05);
        transition: all 0.22s ease; cursor: default; position: relative; overflow: hidden;
    }
    .tc::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, var(--tc), var(--t2));
        transform: scaleX(0); transform-origin: left;
        transition: transform 0.3s ease;
    }
    .tc:hover::before { transform: scaleX(1); }
    .tc:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.06), 0 20px 40px rgba(0,0,0,0.09);
        border-color: var(--tb);
    }
    .tc-name {
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: 0.9rem; color: #0F172A; margin-bottom: 3px;
    }
    .tc-cat {
        font-family: 'Inter', sans-serif; font-size: 0.62rem; color: #94A3B8;
        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px;
    }
    .tc-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: var(--tc); display: inline-block; margin-right: 6px;
    }
    .tc-desc {
        font-family: 'Inter', sans-serif; font-size: 0.79rem;
        color: #64748B; line-height: 1.65;
    }

    .sgrid {
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
    }
    .sc {
        background: #FFFFFF; border-radius: 16px; padding: 20px 16px 18px;
        border: 1.5px solid #F1F5F9;
        border-top: 3px solid var(--sa);
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 14px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .sc:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.06), 0 20px 36px rgba(0,0,0,0.08);
    }
    .sc-num {
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: 1.8rem; color: #EEF0F4; line-height: 1; margin-bottom: 10px;
    }
    .sc-title {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600;
        font-size: 0.88rem; color: var(--sa); margin-bottom: 6px;
        text-transform: uppercase; letter-spacing: 0.04em;
    }
    .sc-desc {
        font-family: 'Inter', sans-serif; font-size: 0.77rem;
        color: #64748B; line-height: 1.6;
    }

    .bband {
        display: grid; grid-template-columns: 1fr 1fr auto; gap: 12px;
        margin-top: 28px;
    }
    .bb-card {
        background: #FFFFFF; border-radius: 16px; padding: 20px 22px;
        border: 1.5px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 14px rgba(0,0,0,0.04);
    }
    .bb-lbl {
        font-family: 'Inter', sans-serif; font-size: 0.6rem; font-weight: 700;
        letter-spacing: 0.14em; text-transform: uppercase; color: #94A3B8;
        margin-bottom: 12px;
    }
    .bb-chips { display: flex; flex-wrap: wrap; gap: 6px; }
    .bb-chip {
        background: #F8FAFC; border: 1px solid #E9EEF4; border-radius: 7px;
        padding: 4px 10px; font-family: 'Inter', sans-serif;
        font-size: 0.71rem; font-weight: 500; color: #475569;
        transition: all 0.15s ease;
    }
    .bb-chip:hover { background: #EFF6FF; border-color: #BFDBFE; color: #1D4ED8; }

    .bb-pipe {
        font-family: 'Inter', sans-serif; font-size: 0.83rem;
        color: #64748B; line-height: 1.8;
    }
    .bb-pipe strong { color: #1E293B; font-weight: 600; }

    .bb-dark {
        background: #0B1A2E; border-radius: 16px; padding: 20px 22px;
        min-width: 180px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 14px 32px rgba(0,0,0,0.18);
    }
    .bb-dark-lbl {
        font-family: 'Inter', sans-serif; font-size: 0.56rem; font-weight: 700;
        letter-spacing: 0.16em; text-transform: uppercase; color: #2D4A6E;
        margin-bottom: 8px;
    }
    .bb-dark-name {
        font-family: 'Space Grotesk', sans-serif; font-weight: 700;
        font-size: 1rem; color: #F1F5F9; line-height: 1.3;
    }
    .bb-dark-name span { color: #60A5FA; }
    .bb-dark-sub {
        font-family: 'Inter', sans-serif; font-size: 0.6rem;
        color: #2D4A6E; margin-top: 10px; letter-spacing: 0.04em;
    }
    </style>

    <div class="h-wrap">
      <div class="h-eyebrow"><div class="h-dot"></div>SOC Analytics Platform</div>
      <div class="h-title">Cyber<span>Defense</span><br>Dashboard</div>
      <div class="h-desc">
        A <strong>centralized security analytics platform</strong> that ingests raw exports,
        computes KPIs, and renders executive dashboards across 6 integrated tools.
      </div>
      <div class="h-stats">
        <div class="h-stat">
          <div class="h-stat-num">6<em>+</em></div>
          <div class="h-stat-lbl">Tools</div>
        </div>
        <div class="h-stat">
          <div class="h-stat-num">KPI<em>s</em></div>
          <div class="h-stat-lbl">Centralized</div>
        </div>
        <div class="h-stat">
          <div class="h-stat-num">1<em>x</em></div>
          <div class="h-stat-lbl">Dashboard</div>
        </div>
        <div class="h-stat">
          <div class="h-stat-num">MySQL</div>
          <div class="h-stat-lbl">Backend</div>
        </div>
      </div>
    </div>

    <div class="sec">Security Tools</div>
    <div class="tgrid">
      <div class="tc" style="--tc:#2563EB;--t2:#60A5FA;--tb:#BFDBFE">
        <div><span class="tc-dot"></span></div>
        <div class="tc-name">CrowdStrike Falcon</div>
        <div class="tc-cat">EDR &middot; Endpoint Detection</div>
        <div class="tc-desc">Tracks alerts, MTTR, severity distribution and MITRE tactic coverage across your fleet.</div>
      </div>
      <div class="tc" style="--tc:#7C3AED;--t2:#A78BFA;--tb:#DDD6FE">
        <div><span class="tc-dot"></span></div>
        <div class="tc-name">Cyble</div>
        <div class="tc-cat">Threat Intel &middot; Dark Web</div>
        <div class="tc-desc">Monitors dark web mentions, keywords, source distribution and alert ratios.</div>
      </div>
      <div class="tc" style="--tc:#EF4444;--t2:#F87171;--tb:#FECACA">
        <div><span class="tc-dot"></span></div>
        <div class="tc-name">SIEM</div>
        <div class="tc-cat">Security Event Management</div>
        <div class="tc-desc">Analyzes events, false positive rates, alert categories and validation status.</div>
      </div>
      <div class="tc" style="--tc:#F59E0B;--t2:#FCD34D;--tb:#FDE68A">
        <div><span class="tc-dot"></span></div>
        <div class="tc-name">Trend Vision</div>
        <div class="tc-cat">Email &middot; Cloud Protection</div>
        <div class="tc-desc">Surfaces phishing threats, quarantine rates and security filter performance.</div>
      </div>
      <div class="tc" style="--tc:#10B981;--t2:#34D399;--tb:#A7F3D0">
        <div><span class="tc-dot"></span></div>
        <div class="tc-name">Netskope</div>
        <div class="tc-cat">Endpoint &middot; Network Security</div>
        <div class="tc-desc">Reports device coverage, OS spread, tunnel status and security enable rates.</div>
      </div>
      <div class="tc" style="--tc:#14B8A6;--t2:#2DD4BF;--tb:#99F6E4">
        <div><span class="tc-dot"></span></div>
        <div class="tc-name">Com Olho</div>
        <div class="tc-cat">Vuln Management &middot; Bug Bounty</div>
        <div class="tc-desc">Tracks vulnerabilities, SLA breach rates, average age and bug bounty rewards.</div>
      </div>
    </div>

    <div class="sec">How It Works</div>
    <div class="sgrid">
      <div class="sc" style="--sa:#2563EB">
        <div class="sc-num">01</div>
        <div class="sc-title">Upload</div>
        <div class="sc-desc">Drop your Excel export. Duplicate detection prevents re-processing the same file.</div>
      </div>
      <div class="sc" style="--sa:#7C3AED">
        <div class="sc-num">02</div>
        <div class="sc-title">Ingest</div>
        <div class="sc-desc">Data is parsed, cleaned and stored in tool-specific MySQL tables.</div>
      </div>
      <div class="sc" style="--sa:#10B981">
        <div class="sc-num">03</div>
        <div class="sc-title">Compute</div>
        <div class="sc-desc">The KPI engine processes raw records and writes metrics into kpi_master.</div>
      </div>
      <div class="sc" style="--sa:#F59E0B">
        <div class="sc-num">04</div>
        <div class="sc-title">Visualize</div>
        <div class="sc-desc">Filter by date on the Dashboard. Live Plotly charts render for every tool.</div>
      </div>
    </div>

    <div class="bband">
      <div class="bb-card">
        <div class="bb-lbl">Tech Stack</div>
        <div class="bb-chips">
          <span class="bb-chip">Python 3</span>
          <span class="bb-chip">Streamlit</span>
          <span class="bb-chip">MySQL</span>
          <span class="bb-chip">Plotly</span>
          <span class="bb-chip">Pandas</span>
          <span class="bb-chip">mysql-connector</span>
          <span class="bb-chip">openpyxl</span>
          <span class="bb-chip">hashlib</span>
        </div>
      </div>
      <div class="bb-card">
        <div class="bb-lbl">Pipeline</div>
        <div class="bb-pipe">
          Upload an Excel export &rarr; head to <strong>Compute KPI</strong>
          to run the analytics engine &rarr; open the <strong>Dashboard</strong>,
          pick a date range and explore charts for every integrated tool.
        </div>
      </div>
      <div class="bb-dark">
        <div class="bb-dark-lbl">Built by</div>
        <div class="bb-dark-name">Gurleen Kaur<br><span>Bali</span></div>
        <div class="bb-dark-sub">Cyber Defense SOC Platform</div>
      </div>
    </div>
    """, unsafe_allow_html=True)