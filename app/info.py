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
        "CrowdStrike Falcon": ("shield", "#3B82F6", "EDR - Endpoint Detection & Response"),
        "Cyble":              ("globe", "#8B5CF6", "Threat Intelligence - Dark Web"),
        "SIEM":               ("lock", "#EF4444", "Security Information & Event Management"),
        "Trend Vision":       ("mail", "#F59E0B", "Email & Cloud Threat Protection"),
        "Netskope":           ("link", "#10B981", "Endpoint & Network Security"),
        "Com Olho":           ("tool", "#14B8A6", "Vulnerability Management - Bug Bounty"),
    }

    # ══════════════════════════════════════════════════════════════
    # DARK SOC THEME CSS
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    .stApp {
        background: #0a0e1a !important;
    }
    .main .block-container {
        padding-top: 1.5rem !important;
        max-width: 1200px;
    }

    /* ══ ANIMATIONS ══ */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(0, 255, 200, 0.4); }
        50% { box-shadow: 0 0 0 8px rgba(0, 255, 200, 0); }
    }
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(0, 255, 200, 0.5), 0 0 40px rgba(0, 255, 200, 0.3); }
        50% { text-shadow: 0 0 30px rgba(0, 255, 200, 0.8), 0 0 60px rgba(0, 255, 200, 0.5); }
    }
    @keyframes borderRotate {
        0% { --angle: 0deg; }
        100% { --angle: 360deg; }
    }
    @keyframes scanline {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }
    @keyframes gridPulse {
        0%, 100% { opacity: 0.03; }
        50% { opacity: 0.06; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        50% { transform: translateY(-15px) rotate(5deg); }
    }
    @keyframes shimmer {
        0% { background-position: -200% center; }
        100% { background-position: 200% center; }
    }
    @keyframes lineGrow {
        from { transform: scaleX(0); }
        to { transform: scaleX(1); }
    }
    @keyframes dataFlow {
        0% { opacity: 0; transform: translateY(-10px); }
        50% { opacity: 1; }
        100% { opacity: 0; transform: translateY(10px); }
    }

    /* ══ BACKGROUND EFFECTS ══ */
    .cyber-grid {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background-image: 
            linear-gradient(rgba(0, 255, 200, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 200, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
        animation: gridPulse 4s ease-in-out infinite;
    }

    .scanlines {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 200, 0.01) 2px,
            rgba(0, 255, 200, 0.01) 4px
        );
        pointer-events: none;
        z-index: 1;
        animation: scanline 8s linear infinite;
    }

    .floating-icons {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    .floating-icon {
        position: absolute;
        font-size: 1.5rem;
        opacity: 0.08;
        animation: float 6s ease-in-out infinite;
        color: #00ffc8;
    }
    .floating-icon:nth-child(1) { top: 10%; left: 5%; animation-delay: 0s; }
    .floating-icon:nth-child(2) { top: 20%; right: 8%; animation-delay: 1s; }
    .floating-icon:nth-child(3) { top: 50%; left: 3%; animation-delay: 2s; }
    .floating-icon:nth-child(4) { top: 70%; right: 5%; animation-delay: 3s; }
    .floating-icon:nth-child(5) { top: 85%; left: 10%; animation-delay: 4s; }
    .floating-icon:nth-child(6) { top: 30%; right: 3%; animation-delay: 2.5s; }

    /* ══ PAGE HEADER ══ */
    .pg-header {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(10, 14, 26, 0.98));
        border-radius: 24px;
        padding: 0;
        display: grid;
        grid-template-columns: 1fr 280px;
        overflow: hidden;
        border: 1px solid rgba(0, 255, 200, 0.15);
        box-shadow: 
            0 0 40px rgba(0, 255, 200, 0.1),
            0 20px 60px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        margin-bottom: 24px;
        opacity: 0;
        animation: fadeUp 0.7s ease forwards 0.1s;
        min-height: 240px;
        position: relative;
    }
    .pg-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ffc8, #3B82F6, transparent);
    }

    .pg-header-left {
        padding: 44px 52px;
        position: relative;
        overflow: hidden;
    }
    .pg-header-left::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
            radial-gradient(ellipse 350px 250px at 90% 20%, rgba(0, 255, 200, 0.08), transparent),
            radial-gradient(ellipse 250px 200px at 10% 80%, rgba(59, 130, 246, 0.06), transparent);
        pointer-events: none;
    }

    .pg-header-right {
        background: linear-gradient(145deg, #0d1321, #0a0e1a);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border-left: 1px solid rgba(0, 255, 200, 0.1);
    }
    .pg-header-right::before {
        content: "";
        position: absolute;
        top: -50px; right: -50px;
        width: 180px; height: 180px;
        border: 1px solid rgba(0, 255, 200, 0.1);
        border-radius: 50%;
    }
    .pg-header-right::after {
        content: "";
        position: absolute;
        top: -25px; right: -25px;
        width: 110px; height: 110px;
        border: 1px solid rgba(0, 255, 200, 0.05);
        border-radius: 50%;
    }

    .pg-arch-visual {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        line-height: 2.2;
        position: relative;
        z-index: 1;
    }
    .arch-step {
        display: block;
        color: #4a5568;
        letter-spacing: 0.04em;
        transition: all 0.3s ease;
        padding: 2px 8px;
        border-radius: 4px;
    }
    .arch-step:hover {
        color: #00ffc8;
        background: rgba(0, 255, 200, 0.1);
    }
    .arch-step.hi {
        color: #00ffc8;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 255, 200, 0.5);
    }
    .arch-arrow {
        color: #1a2332;
        display: block;
    }
    .arch-icon {
        display: inline-block;
        width: 18px;
        text-align: center;
        margin-right: 6px;
    }

    .pg-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #00ffc8;
        margin-bottom: 14px;
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .pg-dot {
        width: 8px; height: 8px;
        background: #00ffc8;
        border-radius: 50%;
        animation: pulse 2s ease infinite;
        box-shadow: 0 0 10px #00ffc8;
    }

    .pg-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        color: #f1f5f9;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin-bottom: 14px;
        position: relative;
        z-index: 1;
    }
    .pg-title span {
        background: linear-gradient(135deg, #00ffc8, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 3s ease-in-out infinite;
    }

    .pg-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        color: #64748b;
        line-height: 1.8;
        max-width: 480px;
        position: relative;
        z-index: 1;
    }
    .pg-desc strong {
        color: #94a3b8;
        font-weight: 600;
    }

    /* ══ SECTION LABEL ══ */
    .sec {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #00ffc8;
        margin: 28px 0 16px;
        display: flex;
        align-items: center;
        gap: 12px;
        opacity: 0;
        animation: fadeIn 0.5s ease forwards 0.5s;
    }
    .sec::before {
        content: "//";
        color: #00ffc8;
        opacity: 0.6;
    }
    .sec::after {
        content: "";
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(0, 255, 200, 0.3), transparent);
        animation: lineGrow 1s ease forwards 0.6s;
        transform-origin: left;
    }

    /* ══ WORKFLOW STEPS ══ */
    .wf-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        opacity: 0;
        animation: fadeUp 0.6s ease forwards 0.3s;
    }

    .wf-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(10, 14, 26, 0.95));
        border-radius: 18px;
        padding: 24px 20px 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .wf-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--wa), var(--wb));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s ease;
    }
    .wf-card::after {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at top right, var(--wg), transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
        pointer-events: none;
    }
    .wf-card:hover::before { transform: scaleX(1); }
    .wf-card:hover::after { opacity: 1; }
    .wf-card:hover {
        transform: translateY(-6px);
        border-color: var(--wa);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 30px var(--wg);
    }

    .wf-num {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 2rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.02));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    .wf-card:hover .wf-num {
        background: linear-gradient(135deg, var(--wa), var(--wb));
        -webkit-background-clip: text;
        background-clip: text;
    }

    .wf-pill {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.58rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        background: var(--wpb);
        color: var(--wpc);
        margin-bottom: 12px;
        border: 1px solid var(--wa);
    }

    .wf-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: #f1f5f9;
        margin-bottom: 6px;
    }

    .wf-desc {
        font-family: 'Inter', sans-serif;
        font-size: 0.78rem;
        color: #64748b;
        line-height: 1.65;
    }

    /* ══ TOOL GRID ══ */
    .tgrid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        opacity: 0;
        animation: fadeUp 0.6s ease forwards 0.4s;
    }

    .tc {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(10, 14, 26, 0.95));
        border-radius: 18px;
        padding: 22px 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        cursor: default;
        position: relative;
        overflow: hidden;
    }
    .tc::before {
        content: "";
        position: absolute;
        inset: 0;
        border-radius: 18px;
        opacity: 0;
        background: radial-gradient(ellipse 150px 120px at 90% 10%, var(--tg), transparent);
        transition: opacity 0.3s;
        pointer-events: none;
    }
    .tc::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--tc), transparent);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    .tc:hover::before { opacity: 1; }
    .tc:hover::after { transform: scaleX(1); }
    .tc:hover {
        transform: translateY(-6px);
        border-color: var(--tb);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4), 0 0 30px var(--tg);
    }

    .tc-top {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 12px;
    }

    .tc-icon-wrap {
        width: 44px; height: 44px;
        border-radius: 12px;
        background: var(--ti);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        position: relative;
        z-index: 1;
        border: 1px solid var(--tc);
        box-shadow: 0 0 20px var(--tg);
    }
    .tc-icon-wrap svg {
        width: 20px; height: 20px;
        stroke: var(--tc);
        stroke-width: 2;
        fill: none;
    }

    .tc-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        color: #f1f5f9;
        position: relative;
        z-index: 1;
    }

    .tc-cat {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        position: relative;
        z-index: 1;
        margin-top: 2px;
    }

    .tc-bar {
        height: 2px;
        border-radius: 2px;
        margin-top: 14px;
        background: linear-gradient(90deg, var(--tc), transparent);
        transform: scaleX(0.2);
        transform-origin: left;
        transition: transform 0.4s ease;
        position: relative;
        z-index: 1;
    }
    .tc:hover .tc-bar { transform: scaleX(1); }

    /* ══ DOWNLOADS ══ */
    .dl-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        opacity: 0;
        animation: fadeUp 0.6s ease forwards 0.5s;
    }

    .dl-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(10, 14, 26, 0.95));
        border-radius: 18px;
        padding: 20px 24px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 16px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .dl-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: var(--dc);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .dl-card:hover::before { opacity: 1; }
    .dl-card:hover {
        transform: translateY(-4px);
        border-color: rgba(0, 255, 200, 0.2);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), 0 0 20px var(--dg);
    }

    .dl-icon {
        width: 46px; height: 46px;
        border-radius: 12px;
        background: var(--di);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        border: 1px solid var(--dc);
        box-shadow: 0 0 15px var(--dg);
    }
    .dl-icon svg {
        width: 20px; height: 20px;
        stroke: var(--dc);
        stroke-width: 2;
        fill: none;
    }

    .dl-info { flex: 1; }

    .dl-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        color: #f1f5f9;
    }

    .dl-cat {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.6rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 3px;
    }

    .dl-missing {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        color: #ef4444;
        font-weight: 500;
        padding: 4px 10px;
        background: rgba(239, 68, 68, 0.1);
        border-radius: 6px;
        border: 1px solid rgba(239, 68, 68, 0.2);
    }

    /* Streamlit download button override */
    .stDownloadButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.1), rgba(0, 255, 200, 0.05)) !important;
        border: 1px solid rgba(0, 255, 200, 0.3) !important;
        border-radius: 10px !important;
        color: #00ffc8 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        transition: all 0.25s ease !important;
        white-space: nowrap !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 200, 0.2), rgba(0, 255, 200, 0.1)) !important;
        border-color: #00ffc8 !important;
        box-shadow: 0 0 20px rgba(0, 255, 200, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    /* ══ TECH + FOOTER ══ */
    .tech-row {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 16px;
        margin-top: 8px;
        opacity: 0;
        animation: fadeUp 0.5s ease forwards 0.6s;
    }

    .tech-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(10, 14, 26, 0.95));
        border-radius: 18px;
        padding: 24px 28px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .tech-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #00ffc8;
        margin-bottom: 14px;
    }
    .tech-lbl::before {
        content: "// ";
        opacity: 0.5;
    }

    .tech-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
    }

    .tech-chip {
        background: rgba(0, 255, 200, 0.05);
        border: 1px solid rgba(0, 255, 200, 0.15);
        border-radius: 8px;
        padding: 6px 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 500;
        color: #94a3b8;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .tech-chip::before {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 200, 0.1), transparent);
        background-size: 200% 100%;
        animation: shimmer 3s ease infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .tech-chip:hover::before { opacity: 1; }
    .tech-chip:hover {
        background: rgba(0, 255, 200, 0.1);
        border-color: rgba(0, 255, 200, 0.4);
        color: #00ffc8;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 255, 200, 0.2);
    }

    .footer-card {
        background: linear-gradient(145deg, #0d1321, #0a0e1a);
        border-radius: 18px;
        padding: 24px 32px;
        min-width: 220px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(0, 255, 200, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 30px rgba(0, 255, 200, 0.1);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .footer-card::before {
        content: "";
        position: absolute;
        top: -40px; right: -40px;
        width: 140px; height: 140px;
        background: radial-gradient(circle, rgba(0, 255, 200, 0.15), transparent 65%);
        border-radius: 50%;
    }
    .footer-card::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, #00ffc8, #3B82F6, transparent);
    }

    .footer-lbl {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.58rem;
        font-weight: 600;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #4a5568;
        margin-bottom: 8px;
        position: relative;
        z-index: 1;
    }

    .footer-name {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        color: #f1f5f9;
        position: relative;
        z-index: 1;
    }
    .footer-name span {
        background: linear-gradient(135deg, #00ffc8, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .footer-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.62rem;
        color: #4a5568;
        margin-top: 6px;
        position: relative;
        z-index: 1;
        letter-spacing: 0.04em;
    }

    /* Hide Streamlit elements */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # BACKGROUND EFFECTS
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="cyber-grid"></div>
    <div class="scanlines"></div>
    <div class="floating-icons">
        <div class="floating-icon">&#9737;</div>
        <div class="floating-icon">&#9881;</div>
        <div class="floating-icon">&#8962;</div>
        <div class="floating-icon">&#9883;</div>
        <div class="floating-icon">&#10070;</div>
        <div class="floating-icon">&#9880;</div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # PAGE HEADER
    # ══════════════════════════════════════════════════════════════
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
          <span class="arch-step"><span class="arch-icon">&#128196;</span>Excel File</span>
          <span class="arch-arrow">    &#8595;</span>
          <span class="arch-step"><span class="arch-icon">&#8593;</span>Upload Module</span>
          <span class="arch-arrow">    &#8595;</span>
          <span class="arch-step hi"><span class="arch-icon">&#9633;</span>Raw Tables (MySQL)</span>
          <span class="arch-arrow">    &#8595;</span>
          <span class="arch-step"><span class="arch-icon">&#9881;</span>KPI Engine</span>
          <span class="arch-arrow">    &#8595;</span>
          <span class="arch-step hi"><span class="arch-icon">&#9638;</span>kpi_master</span>
          <span class="arch-arrow">    &#8595;</span>
          <span class="arch-step"><span class="arch-icon">&#9632;</span>Dashboard</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # WORKFLOW
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="sec">Workflow</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="wf-grid">
      <div class="wf-card" style="--wa:#3B82F6;--wb:#60A5FA;--wpb:rgba(59,130,246,0.1);--wpc:#60A5FA;--wg:rgba(59,130,246,0.15)">
        <div class="wf-num">01</div>
        <div class="wf-pill">Download</div>
        <div class="wf-title">Get Sample File</div>
        <div class="wf-desc">Download a sample Excel file for any tool to test the full pipeline end-to-end.</div>
      </div>
      <div class="wf-card" style="--wa:#8B5CF6;--wb:#A78BFA;--wpb:rgba(139,92,246,0.1);--wpc:#A78BFA;--wg:rgba(139,92,246,0.15)">
        <div class="wf-num">02</div>
        <div class="wf-pill">Upload</div>
        <div class="wf-title">Ingest Data</div>
        <div class="wf-desc">Upload your Excel export. Duplicate detection prevents re-processing the same file.</div>
      </div>
      <div class="wf-card" style="--wa:#10B981;--wb:#34D399;--wpb:rgba(16,185,129,0.1);--wpc:#34D399;--wg:rgba(16,185,129,0.15)">
        <div class="wf-num">03</div>
        <div class="wf-pill">Compute</div>
        <div class="wf-title">Generate KPIs</div>
        <div class="wf-desc">Select your upload ID and run the KPI engine. Results store in kpi_master automatically.</div>
      </div>
      <div class="wf-card" style="--wa:#F59E0B;--wb:#FCD34D;--wpb:rgba(245,158,11,0.1);--wpc:#FCD34D;--wg:rgba(245,158,11,0.15)">
        <div class="wf-num">04</div>
        <div class="wf-pill">Visualize</div>
        <div class="wf-title">Explore Dashboard</div>
        <div class="wf-desc">Filter by date range. Charts and KPIs render live for every tool in dedicated tabs.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SUPPORTED TOOLS
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="sec">Supported Security Tools</div>', unsafe_allow_html=True)
    
    # SVG icons for each tool
    icons_svg = {
        "shield": '<svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "globe": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        "lock": '<svg viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
        "mail": '<svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
        "link": '<svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
        "tool": '<svg viewBox="0 0 24 24"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/></svg>',
    }
    
    st.markdown(f"""
    <div class="tgrid">
      <div class="tc" style="--tc:#3B82F6;--tb:rgba(59,130,246,0.4);--ti:rgba(59,130,246,0.15);--tg:rgba(59,130,246,0.2)">
        <div class="tc-top"><div class="tc-icon-wrap">{icons_svg['shield']}</div><div><div class="tc-name">CrowdStrike Falcon</div><div class="tc-cat">EDR - Endpoint Detection</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#8B5CF6;--tb:rgba(139,92,246,0.4);--ti:rgba(139,92,246,0.15);--tg:rgba(139,92,246,0.2)">
        <div class="tc-top"><div class="tc-icon-wrap">{icons_svg['globe']}</div><div><div class="tc-name">Cyble</div><div class="tc-cat">Threat Intel - Dark Web</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#EF4444;--tb:rgba(239,68,68,0.4);--ti:rgba(239,68,68,0.15);--tg:rgba(239,68,68,0.2)">
        <div class="tc-top"><div class="tc-icon-wrap">{icons_svg['lock']}</div><div><div class="tc-name">SIEM</div><div class="tc-cat">Security Event Management</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#F59E0B;--tb:rgba(245,158,11,0.4);--ti:rgba(245,158,11,0.15);--tg:rgba(245,158,11,0.2)">
        <div class="tc-top"><div class="tc-icon-wrap">{icons_svg['mail']}</div><div><div class="tc-name">Trend Vision</div><div class="tc-cat">Email - Cloud Protection</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#10B981;--tb:rgba(16,185,129,0.4);--ti:rgba(16,185,129,0.15);--tg:rgba(16,185,129,0.2)">
        <div class="tc-top"><div class="tc-icon-wrap">{icons_svg['link']}</div><div><div class="tc-name">Netskope</div><div class="tc-cat">Endpoint - Network Security</div></div></div>
        <div class="tc-bar"></div>
      </div>
      <div class="tc" style="--tc:#14B8A6;--tb:rgba(20,184,166,0.4);--ti:rgba(20,184,166,0.15);--tg:rgba(20,184,166,0.2)">
        <div class="tc-top"><div class="tc-icon-wrap">{icons_svg['tool']}</div><div><div class="tc-name">Com Olho</div><div class="tc-cat">Vulnerability - Bug Bounty</div></div></div>
        <div class="tc-bar"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SAMPLE DOWNLOADS
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="sec">Sample Files</div>', unsafe_allow_html=True)
    
    tools_list = list(SAMPLE_FILES.items())
    for i in range(0, len(tools_list), 3):
        row = tools_list[i:i+3]
        cols = st.columns(3)
        for col, (tool, filepath) in zip(cols, row):
            icon_name, color, cat = TOOL_META[tool]
            icon_svg = icons_svg.get(icon_name, icons_svg['shield'])
            with col:
                st.markdown(f"""
                <div class="dl-card" style="--di:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.15);--dc:{color};--dg:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.2);">
                  <div class="dl-icon">{icon_svg}</div>
                  <div class="dl-info">
                    <div class="dl-name">{tool}</div>
                    <div class="dl-cat">{cat.split('-')[0].strip()}</div>
                  </div>
                """, unsafe_allow_html=True)
                if os.path.exists(filepath):
                    with open(filepath, "rb") as f:
                        st.download_button(
                            label="Download",
                            data=f.read(),
                            file_name=os.path.basename(filepath),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"dl_{tool}"
                        )
                else:
                    st.markdown('<div class="dl-missing">File not found</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # TECH STACK + FOOTER
    # ══════════════════════════════════════════════════════════════
    st.markdown('<div class="sec">Tech Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-row">
      <div class="tech-card">
        <div class="tech-lbl">Built With</div>
        <div class="tech-chips">
          <span class="tech-chip">Python 3</span>
          <span class="tech-chip">Streamlit</span>
          <span class="tech-chip">MySQL</span>
          <span class="tech-chip">Plotly</span>
          <span class="tech-chip">Pandas</span>
          <span class="tech-chip">mysql-connector</span>
          </span>
        </div>
      </div>
      <div class="footer-card">
        <div class="footer-lbl">Built by</div>
        <div class="footer-name">Gurleen Kaur <span>Bali</span></div>
        <div class="footer-sub">Cyber Defense SOC Platform</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
