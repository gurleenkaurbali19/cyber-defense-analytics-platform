import streamlit as st

def show_home():
    # Enhanced CSS Styles with premium effects
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* === BACKGROUND LAYERS === */
    .noise-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        pointer-events: none; z-index: 9999; opacity: 0.03;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    }

    /* Scanline effect for CRT/terminal aesthetic */
    .scanlines {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 9998; opacity: 0.03;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 212, 255, 0.03) 2px,
            rgba(0, 212, 255, 0.03) 4px
        );
        animation: scanlineMove 8s linear infinite;
    }
    @keyframes scanlineMove {
        0% { background-position: 0 0; }
        100% { background-position: 0 100vh; }
    }

    /* Cyber grid pattern */
    .cyber-grid {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 0; opacity: 0.015;
        background-image: 
            linear-gradient(rgba(0, 212, 255, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.3) 1px, transparent 1px);
        background-size: 60px 60px;
        animation: gridPulse 4s ease-in-out infinite;
    }
    @keyframes gridPulse {
        0%, 100% { opacity: 0.015; }
        50% { opacity: 0.025; }
    }

    .particles-container {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 0; overflow: hidden;
    }
    .particle {
        position: absolute; border-radius: 50%; opacity: 0.15;
        animation: floatParticle linear infinite;
    }
    .particle:nth-child(1) { width: 4px; height: 4px; background: #00d4ff; left: 10%; top: 20%; animation-duration: 25s; animation-delay: 0s; }
    .particle:nth-child(2) { width: 6px; height: 6px; background: #00ff88; left: 20%; top: 80%; animation-duration: 30s; animation-delay: -5s; }
    .particle:nth-child(3) { width: 3px; height: 3px; background: #a855f7; left: 35%; top: 10%; animation-duration: 22s; animation-delay: -3s; }
    .particle:nth-child(4) { width: 5px; height: 5px; background: #00d4ff; left: 50%; top: 50%; animation-duration: 28s; animation-delay: -8s; }
    .particle:nth-child(5) { width: 4px; height: 4px; background: #ffb800; left: 65%; top: 30%; animation-duration: 35s; animation-delay: -2s; }
    .particle:nth-child(6) { width: 7px; height: 7px; background: #f43f5e; left: 75%; top: 70%; animation-duration: 20s; animation-delay: -10s; }
    .particle:nth-child(7) { width: 3px; height: 3px; background: #00ff88; left: 85%; top: 15%; animation-duration: 32s; animation-delay: -7s; }
    .particle:nth-child(8) { width: 5px; height: 5px; background: #14b8a6; left: 90%; top: 85%; animation-duration: 27s; animation-delay: -4s; }
    
    @keyframes floatParticle {
        0% { transform: translate(0, 0) rotate(0deg); opacity: 0; }
        10% { opacity: 0.2; }
        50% { opacity: 0.35; }
        90% { opacity: 0.2; }
        100% { transform: translate(calc(100vw * 0.3), calc(-100vh * 0.5)) rotate(360deg); opacity: 0; }
    }

    /* Floating security icons */
    .floating-icons {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 0; overflow: hidden;
    }
    .float-icon {
        position: absolute; opacity: 0.04; font-size: 3rem;
        animation: floatIcon 20s ease-in-out infinite;
    }
    .float-icon:nth-child(1) { left: 5%; top: 15%; animation-delay: 0s; animation-duration: 25s; }
    .float-icon:nth-child(2) { left: 15%; top: 70%; animation-delay: -5s; animation-duration: 22s; }
    .float-icon:nth-child(3) { left: 80%; top: 20%; animation-delay: -10s; animation-duration: 28s; }
    .float-icon:nth-child(4) { left: 70%; top: 75%; animation-delay: -15s; animation-duration: 24s; }
    .float-icon:nth-child(5) { left: 45%; top: 85%; animation-delay: -8s; animation-duration: 30s; }
    @keyframes floatIcon {
        0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.03; }
        25% { transform: translateY(-30px) rotate(5deg); opacity: 0.06; }
        50% { transform: translateY(-15px) rotate(-3deg); opacity: 0.04; }
        75% { transform: translateY(-40px) rotate(3deg); opacity: 0.05; }
    }

    .gradient-mesh {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 0;
        background: 
            radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse 60% 40% at 80% 20%, rgba(168, 85, 247, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse 70% 60% at 70% 80%, rgba(0, 255, 136, 0.05) 0%, transparent 50%);
        animation: meshMove 20s ease-in-out infinite;
    }
    @keyframes meshMove {
        0%, 100% { background: radial-gradient(ellipse 80% 50% at 20% 40%, rgba(0, 212, 255, 0.08) 0%, transparent 50%), radial-gradient(ellipse 60% 40% at 80% 20%, rgba(168, 85, 247, 0.06) 0%, transparent 50%), radial-gradient(ellipse 70% 60% at 70% 80%, rgba(0, 255, 136, 0.05) 0%, transparent 50%); }
        50% { background: radial-gradient(ellipse 70% 60% at 30% 60%, rgba(0, 212, 255, 0.08) 0%, transparent 50%), radial-gradient(ellipse 80% 50% at 70% 40%, rgba(168, 85, 247, 0.06) 0%, transparent 50%), radial-gradient(ellipse 60% 40% at 50% 20%, rgba(0, 255, 136, 0.05) 0%, transparent 50%); }
    }

    /* Radar pulse ring behind hero */
    .radar-container {
        position: absolute; top: 50px; right: 10%; width: 300px; height: 300px;
        pointer-events: none; z-index: 0; opacity: 0.4;
    }
    .radar-ring {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 50%;
        animation: radarPulse 4s ease-out infinite;
    }
    .radar-ring:nth-child(1) { width: 80px; height: 80px; animation-delay: 0s; }
    .radar-ring:nth-child(2) { width: 140px; height: 140px; animation-delay: 0.8s; }
    .radar-ring:nth-child(3) { width: 200px; height: 200px; animation-delay: 1.6s; }
    .radar-ring:nth-child(4) { width: 260px; height: 260px; animation-delay: 2.4s; }
    .radar-center {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 12px; height: 12px; background: #00d4ff; border-radius: 50%;
        box-shadow: 0 0 20px #00d4ff, 0 0 40px rgba(0, 212, 255, 0.5);
        animation: radarCenterPulse 2s ease-in-out infinite;
    }
    .radar-sweep {
        position: absolute; top: 50%; left: 50%; width: 130px; height: 2px;
        background: linear-gradient(90deg, #00d4ff, transparent);
        transform-origin: left center;
        animation: radarSweep 4s linear infinite;
    }
    @keyframes radarPulse {
        0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0.8; }
        100% { transform: translate(-50%, -50%) scale(1.5); opacity: 0; }
    }
    @keyframes radarCenterPulse {
        0%, 100% { box-shadow: 0 0 20px #00d4ff, 0 0 40px rgba(0, 212, 255, 0.5); }
        50% { box-shadow: 0 0 30px #00d4ff, 0 0 60px rgba(0, 212, 255, 0.7); }
    }
    @keyframes radarSweep {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* === ANIMATIONS === */
    @keyframes fadeUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes pulse { 0%, 100% { opacity: 1; box-shadow: 0 0 8px #00d4ff; } 50% { opacity: 0.5; box-shadow: 0 0 15px #00d4ff; } }
    @keyframes typing { from { width: 0; } to { width: 100%; } }
    @keyframes blink { 0%, 50% { opacity: 1; } 51%, 100% { opacity: 0; } }
    @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
    @keyframes scaleIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
    @keyframes slideInLeft { from { opacity: 0; transform: translateX(-30px); } to { opacity: 1; transform: translateX(0); } }
    @keyframes glowPulse { 0%, 100% { filter: drop-shadow(0 0 5px var(--tc)); } 50% { filter: drop-shadow(0 0 15px var(--tc)); } }
    @keyframes countUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes textGlow { 0%, 100% { text-shadow: 0 0 10px rgba(0, 212, 255, 0.5), 0 0 20px rgba(0, 212, 255, 0.3); } 50% { text-shadow: 0 0 20px rgba(0, 212, 255, 0.8), 0 0 40px rgba(0, 212, 255, 0.5), 0 0 60px rgba(0, 212, 255, 0.3); } }
    @keyframes borderRotate { 0% { --angle: 0deg; } 100% { --angle: 360deg; } }
    @keyframes holographic { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    @keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }

    /* === MAIN CONTENT === */
    .home-main { position: relative; z-index: 1; }
    .h-wrap { animation: fadeUp 0.8s ease forwards; padding: 10px 0; position: relative; }

    .h-eyebrow {
        display: inline-flex; align-items: center; gap: 10px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.12) 0%, rgba(0, 255, 136, 0.08) 100%);
        border: 1px solid rgba(0, 212, 255, 0.35); border-radius: 50px; padding: 8px 20px; margin-bottom: 24px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 500; letter-spacing: 0.14em; text-transform: uppercase; color: #00d4ff;
        backdrop-filter: blur(15px); box-shadow: 0 4px 20px rgba(0, 212, 255, 0.15), inset 0 1px 0 rgba(255,255,255,0.05);
        animation: scaleIn 0.6s ease 0.2s both;
        position: relative; overflow: hidden;
    }
    .h-eyebrow::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shimmerSlide 3s ease-in-out infinite;
    }
    @keyframes shimmerSlide { 0% { left: -100%; } 50%, 100% { left: 100%; } }
    .h-dot { width: 8px; height: 8px; border-radius: 50%; background: #00d4ff; animation: pulse 2s ease-in-out infinite; }

    .h-title-wrap { margin-bottom: 20px; animation: fadeIn 0.5s ease 0.3s both; }
    
    /* CyberPulse brand name */
    .h-brand {
        font-family: 'Space Grotesk', sans-serif; font-size: 1rem; font-weight: 600;
        letter-spacing: 0.35em; text-transform: uppercase; margin-bottom: 8px;
        background: linear-gradient(90deg, #00d4ff 0%, #a855f7 50%, #00ff88 100%);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        animation: fadeIn 0.5s ease 0.2s both, gradientShift 3s ease infinite;
        display: inline-flex; align-items: center; gap: 12px;
        position: relative;
    }
    .h-brand::before {
        content: ''; width: 30px; height: 2px;
        background: linear-gradient(90deg, #00d4ff, transparent);
    }
    .h-brand::after {
        content: ''; width: 30px; height: 2px;
        background: linear-gradient(90deg, transparent, #00ff88);
    }
    .h-brand .pulse-ring {
        position: absolute; left: -8px; top: 50%; transform: translateY(-50%);
        width: 6px; height: 6px; border-radius: 50%; background: #00d4ff;
        box-shadow: 0 0 10px #00d4ff;
    }
    .h-brand .pulse-ring::before {
        content: ''; position: absolute; inset: -4px; border-radius: 50%;
        border: 1px solid rgba(0, 212, 255, 0.5);
        animation: brandPulse 2s ease-out infinite;
    }
    @keyframes brandPulse {
        0% { transform: scale(1); opacity: 1; }
        100% { transform: scale(2.5); opacity: 0; }
    }
    .h-title {
        font-family: 'Space Grotesk', sans-serif; font-size: 3.2rem; font-weight: 700;
        color: #e6edf3; letter-spacing: -0.03em; line-height: 1.05; margin: 0; display: inline;
    }
    .h-title-line { display: block; overflow: hidden; white-space: nowrap; }
    .h-title-line:first-child { animation: typing 1.2s steps(20) 0.5s both; }
    .h-title-line:last-child { animation: typing 1s steps(15) 1.8s both; }
    .h-title .gradient { 
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 50%, #a855f7 100%);
        background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        animation: gradientShift 4s ease infinite, textGlow 3s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.3));
    }
    .h-cursor {
        display: inline-block; width: 3px; height: 3rem; background: #00d4ff;
        margin-left: 4px; vertical-align: middle; animation: blink 1s step-end infinite; box-shadow: 0 0 10px #00d4ff, 0 0 20px rgba(0, 212, 255, 0.5);
    }

    /* Glowing subtitle effect */
    .h-subtitle {
        font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #6e7681;
        letter-spacing: 0.3em; text-transform: uppercase; margin-top: 12px; margin-bottom: 8px;
        animation: fadeIn 0.8s ease 2s both;
    }
    .h-subtitle .bracket { color: #00d4ff; }
    .h-subtitle .text { color: #8b949e; }

    .h-desc {
        font-family: 'Inter', sans-serif; font-size: 1rem; color: #8b949e; 
        line-height: 1.85; max-width: 620px; margin-bottom: 36px; animation: fadeUp 0.8s ease 2.2s both;
    }
    .h-desc strong { 
        color: #e6edf3; font-weight: 600; position: relative; 
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(0, 255, 136, 0.1));
        padding: 2px 8px; border-radius: 4px; margin: 0 2px;
    }
    .h-desc strong::after {
        content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 1px;
        background: linear-gradient(90deg, #00d4ff, #00ff88); border-radius: 2px; opacity: 0.6;
    }

    /* Enhanced stats with animated borders */
    .h-stats { display: flex; gap: 0; margin-bottom: 56px; animation: fadeUp 0.8s ease 2.5s both; }
    .h-stat { 
        padding: 16px 36px 16px 0; margin-right: 36px; 
        border-right: 1px solid rgba(139, 148, 158, 0.2); 
        transition: all 0.3s ease; position: relative;
    }
    .h-stat:hover { transform: translateY(-3px); }
    .h-stat:hover .h-stat-num { text-shadow: 0 0 30px rgba(0, 212, 255, 0.5); }
    .h-stat:last-child { border-right: none; margin-right: 0; padding-right: 0; }
    .h-stat-num {
        font-family: 'Space Grotesk', sans-serif; font-size: 2.2rem; font-weight: 700; 
        color: #e6edf3; line-height: 1; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3); position: relative;
        transition: text-shadow 0.3s ease;
    }
    .h-stat-num .counter { display: inline-block; animation: countUp 0.6s ease forwards; animation-delay: 2.8s; opacity: 0; }
    .h-stat:nth-child(1) .counter { animation-delay: 2.8s; }
    .h-stat:nth-child(2) .counter { animation-delay: 3.0s; }
    .h-stat:nth-child(3) .counter { animation-delay: 3.2s; }
    .h-stat:nth-child(4) .counter { animation-delay: 3.4s; }
    .h-stat-num em { 
        color: #00d4ff; font-style: normal; font-size: 1.2rem; 
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        animation: textGlow 2s ease-in-out infinite;
    }
    .h-stat-lbl { 
        font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #6e7681; 
        font-weight: 500; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 8px; 
    }

    /* Section headers with animated line */
    .sec {
        font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; font-weight: 500;
        letter-spacing: 0.18em; text-transform: uppercase; color: #6e7681;
        margin: 48px 0 22px; display: flex; align-items: center; gap: 14px; animation: slideInLeft 0.6s ease both;
    }
    .sec::before { content: '//'; color: #00d4ff; font-weight: 700; }
    .sec::after { 
        content: ""; flex: 1; height: 1px; 
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.5) 0%, rgba(0, 255, 136, 0.3) 30%, transparent 100%); 
        animation: lineGrow 1s ease 0.3s both;
    }
    @keyframes lineGrow { from { transform: scaleX(0); transform-origin: left; } to { transform: scaleX(1); } }

    /* Enhanced tool cards with holographic hover */
    .tgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 10px; perspective: 1000px; }
    .tc {
        background: rgba(22, 27, 34, 0.7); backdrop-filter: blur(25px); border-radius: 20px; padding: 26px;
        border: 1px solid rgba(139, 148, 158, 0.12); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s ease; 
        cursor: default; position: relative; overflow: hidden; animation: scaleIn 0.5s ease both; transform-style: preserve-3d;
    }
    .tgrid .tc:nth-child(1) { animation-delay: 0.1s; }
    .tgrid .tc:nth-child(2) { animation-delay: 0.2s; }
    .tgrid .tc:nth-child(3) { animation-delay: 0.3s; }
    .tgrid .tc:nth-child(4) { animation-delay: 0.4s; }
    .tgrid .tc:nth-child(5) { animation-delay: 0.5s; }
    .tgrid .tc:nth-child(6) { animation-delay: 0.6s; }
    .tc::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, var(--tc), var(--t2)); opacity: 0.9; transition: height 0.3s ease;
    }
    .tc::after {
        content: ""; position: absolute; inset: 0; border-radius: 20px;
        background: radial-gradient(ellipse at top, rgba(var(--tc-rgb), 0.1) 0%, transparent 70%);
        opacity: 0; transition: opacity 0.4s ease;
    }
    .tc:hover { 
        transform: translateY(-8px) scale(1.02) rotateX(2deg); 
        border-color: rgba(var(--tc-rgb), 0.5); 
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 0 0 60px rgba(var(--tc-rgb), 0.2), inset 0 0 30px rgba(var(--tc-rgb), 0.05); 
    }
    .tc:hover::before { height: 4px; box-shadow: 0 0 20px var(--tc); }
    .tc:hover::after { opacity: 1; }
    
    /* Holographic shimmer on hover */
    .tc .holo-shimmer {
        position: absolute; inset: 0; opacity: 0; transition: opacity 0.4s ease;
        background: linear-gradient(
            135deg,
            transparent 0%,
            rgba(0, 212, 255, 0.03) 25%,
            rgba(168, 85, 247, 0.03) 50%,
            rgba(0, 255, 136, 0.03) 75%,
            transparent 100%
        );
        background-size: 400% 400%;
        animation: holographic 3s ease infinite;
    }
    .tc:hover .holo-shimmer { opacity: 1; }

    .tc-inner { position: relative; z-index: 1; transition: transform 0.3s ease; }
    .tc:hover .tc-inner { transform: translateZ(20px); }
    .tc-dot { 
        width: 10px; height: 10px; border-radius: 50%; background: var(--tc); 
        display: inline-block; margin-right: 10px; box-shadow: 0 0 12px var(--tc); 
        animation: glowPulse 2s ease-in-out infinite; 
    }
    .tc-name { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; color: #e6edf3; margin-bottom: 6px; display: inline; }
    .tc-cat { 
        font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #6e7681; 
        text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 14px; margin-top: 8px;
        padding: 4px 10px; background: rgba(139, 148, 158, 0.08); border-radius: 4px; display: inline-block;
    }
    .tc-desc { font-family: 'Inter', sans-serif; font-size: 0.82rem; color: #8b949e; line-height: 1.75; }

    /* Enhanced step cards */
    .sgrid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; position: relative; z-index: 1; }
    .sc {
        background: rgba(22, 27, 34, 0.5); backdrop-filter: blur(25px); border-radius: 20px; padding: 26px 20px 24px;
        border: 1px solid rgba(139, 148, 158, 0.12); transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1), transform 0.3s ease;
        position: relative; overflow: hidden; animation: scaleIn 0.5s ease both; transform-style: preserve-3d;
    }
    .sgrid .sc:nth-child(1) { animation-delay: 0.2s; }
    .sgrid .sc:nth-child(2) { animation-delay: 0.3s; }
    .sgrid .sc:nth-child(3) { animation-delay: 0.4s; }
    .sgrid .sc:nth-child(4) { animation-delay: 0.5s; }
    .sc::before {
        content: ""; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
        width: 50px; height: 3px; background: var(--sa); box-shadow: 0 0 20px var(--sa); border-radius: 0 0 4px 4px;
    }
    .sc::after {
        content: ""; position: absolute; inset: 0;
        background: radial-gradient(ellipse at top center, rgba(var(--sa-rgb), 0.08) 0%, transparent 60%);
        opacity: 0; transition: opacity 0.4s ease;
    }
    .sc:hover { transform: translateY(-6px) rotateX(2deg); border-color: rgba(139, 148, 158, 0.25); box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4), 0 0 40px rgba(var(--sa-rgb), 0.15); }
    .sc:hover::after { opacity: 1; }
    .sc-inner { position: relative; z-index: 1; transition: transform 0.3s ease; }
    .sc:hover .sc-inner { transform: translateZ(15px); }
    .sc-num {
        font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.4rem; 
        background: linear-gradient(180deg, rgba(139, 148, 158, 0.25) 0%, rgba(139, 148, 158, 0.05) 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1; margin-bottom: 14px;
    }
    .sc:hover .sc-num {
        background: linear-gradient(180deg, rgba(var(--sa-rgb), 0.5) 0%, rgba(var(--sa-rgb), 0.1) 100%);
        -webkit-background-clip: text; background-clip: text;
    }
    .sc-title {
        font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 0.95rem; 
        color: var(--sa); margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.06em; text-shadow: 0 0 25px var(--sa);
    }
    .sc-desc { font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #8b949e; line-height: 1.7; }

    /* Connector line between steps */
    .sgrid::before {
        content: ''; position: absolute; top: 40px; left: 12.5%; right: 12.5%; height: 2px;
        background: linear-gradient(90deg, 
            rgba(0, 212, 255, 0.3) 0%, 
            rgba(168, 85, 247, 0.3) 33%, 
            rgba(0, 255, 136, 0.3) 66%, 
            rgba(255, 184, 0, 0.3) 100%
        );
        z-index: 0; opacity: 0.5;
    }

    /* Bottom band */
    .bband { display: grid; grid-template-columns: 1fr 1fr auto; gap: 16px; margin-top: 44px; animation: fadeUp 0.8s ease 0.8s both; perspective: 1000px; }
    .bb-card {
        background: rgba(22, 27, 34, 0.5); backdrop-filter: blur(25px); border-radius: 20px; padding: 26px 28px;
        border: 1px solid rgba(139, 148, 158, 0.12); transition: all 0.4s ease, transform 0.3s ease; transform-style: preserve-3d;
    }
    .bb-card:hover { transform: translateY(-4px) rotateX(1deg); border-color: rgba(139, 148, 158, 0.25); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.35); }
    .bb-lbl { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; font-weight: 500; letter-spacing: 0.16em; text-transform: uppercase; color: #6e7681; margin-bottom: 16px; }
    .bb-chips { display: flex; flex-wrap: wrap; gap: 10px; }
    .bb-chip {
        background: rgba(0, 212, 255, 0.06); border: 1px solid rgba(0, 212, 255, 0.18); 
        border-radius: 10px; padding: 8px 14px; font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem; font-weight: 500; color: #8b949e; transition: all 0.3s ease;
        position: relative; overflow: hidden;
    }
    .bb-chip::before {
        content: ''; position: absolute; inset: 0; 
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), transparent);
        opacity: 0; transition: opacity 0.3s ease;
    }
    .bb-chip:hover { 
        background: rgba(0, 212, 255, 0.12); border-color: rgba(0, 212, 255, 0.45); 
        color: #00d4ff; box-shadow: 0 4px 20px rgba(0, 212, 255, 0.2), inset 0 0 20px rgba(0, 212, 255, 0.05); 
        transform: translateY(-2px); 
    }
    .bb-chip:hover::before { opacity: 1; }
    .bb-pipe { font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #8b949e; line-height: 1.9; }
    .bb-pipe strong { color: #00d4ff; font-weight: 600; text-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }

    /* Enhanced built-by card */
    .bb-dark {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.12) 0%, rgba(0, 255, 136, 0.06) 100%);
        border: 1px solid rgba(0, 212, 255, 0.35); border-radius: 20px; padding: 26px 28px;
        min-width: 200px; position: relative; overflow: hidden; transition: all 0.4s ease, transform 0.3s ease; transform-style: preserve-3d;
    }
    .bb-dark:hover { transform: translateY(-4px) rotateX(1deg); box-shadow: 0 15px 50px rgba(0, 212, 255, 0.2); }
    .bb-dark::before {
        content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #00d4ff 0%, #00ff88 50%, #a855f7 100%);
        background-size: 200% auto; animation: shimmer 3s linear infinite;
    }
    /* Animated corner accents */
    .bb-dark::after {
        content: ''; position: absolute; bottom: 10px; right: 10px;
        width: 30px; height: 30px; border-right: 2px solid rgba(0, 212, 255, 0.3); border-bottom: 2px solid rgba(0, 212, 255, 0.3);
        opacity: 0.5;
    }
    .bb-dark-lbl { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #6e7681; margin-bottom: 12px; }
    .bb-dark-name { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.1rem; color: #e6edf3; line-height: 1.4; }
    .bb-dark-name .gradient { 
        background: linear-gradient(135deg, #00d4ff 0%, #00ff88 50%, #a855f7 100%); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
        animation: gradientShift 3s ease infinite;
    }
    .bb-dark-sub { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #6e7681; margin-top: 14px; letter-spacing: 0.06em; }

    /* Security badge */
    .security-badge {
        position: absolute; top: 20px; right: 20px;
        display: flex; align-items: center; gap: 8px;
        background: rgba(0, 255, 136, 0.08); border: 1px solid rgba(0, 255, 136, 0.25);
        border-radius: 8px; padding: 6px 12px;
        font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #00ff88;
        letter-spacing: 0.1em; text-transform: uppercase;
        animation: float 3s ease-in-out infinite;
    }
    .security-badge::before {
        content: ''; width: 6px; height: 6px; background: #00ff88; border-radius: 50%;
        box-shadow: 0 0 10px #00ff88; animation: pulse 2s ease-in-out infinite;
    }

    @media (max-width: 1000px) {
        .tgrid { grid-template-columns: repeat(2, 1fr); }
        .sgrid { grid-template-columns: repeat(2, 1fr); }
        .sgrid::before { display: none; }
        .bband { grid-template-columns: 1fr; }
        .radar-container { display: none; }
    }
    @media (max-width: 600px) {
        .tgrid, .sgrid { grid-template-columns: 1fr; }
        .h-title { font-size: 2.2rem; }
        .h-stats { flex-wrap: wrap; gap: 24px; }
        .h-stat { border-right: none; padding-right: 0; margin-right: 0; }
        .security-badge { display: none; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Background elements with enhanced visuals
    st.markdown("""
    <div class="noise-overlay"></div>
    <div class="scanlines"></div>
    <div class="cyber-grid"></div>
    <div class="gradient-mesh"></div>
    <div class="particles-container">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    <div class="floating-icons">
        <div class="float-icon">&#128737;</div>
        <div class="float-icon">&#128274;</div>
        <div class="float-icon">&#128272;</div>
        <div class="float-icon">&#9881;</div>
        <div class="float-icon">&#128161;</div>
    </div>
    """, unsafe_allow_html=True)

    # Hero section with radar and security badge
    st.markdown("""
    <div class="home-main">
        <div class="h-wrap">
          <div class="radar-container">
            <div class="radar-ring"></div>
            <div class="radar-ring"></div>
            <div class="radar-ring"></div>
            <div class="radar-ring"></div>
            <div class="radar-center"></div>
            <div class="radar-sweep"></div>
          </div>
          <div class="security-badge">System Active</div>
          <div class="h-eyebrow"><div class="h-dot"></div>SOC Analytics Platform</div>
          <div class="h-title-wrap">
            <div class="h-brand"><span class="pulse-ring"></span>Cyber Defense Dasbaord</div>
            <div class="h-title">
              <span class="h-title-line">Cyber<span class="gradient">Pulse</span></span>
              </span>
            </div>
          </div>
          <div class="h-subtitle"><span class="bracket">[</span><span class="text"> Real-time Security Intelligence </span><span class="bracket">]</span></div>
          <div class="h-desc">
            A <strong>centralized security analytics platform</strong> that ingests raw exports,
            computes KPIs, and renders executive dashboards across 6 integrated tools.
          </div>
          <div class="h-stats">
            <div class="h-stat">
              <div class="h-stat-num"><span class="counter">6</span><em>+</em></div>
              <div class="h-stat-lbl">Tools</div>
            </div>
            <div class="h-stat">
              <div class="h-stat-num"><span class="counter">KPI</span><em>s</em></div>
              <div class="h-stat-lbl">Centralized</div>
            </div>
            <div class="h-stat">
              <div class="h-stat-num"><span class="counter">1</span><em>x</em></div>
              <div class="h-stat-lbl">Dashboard</div>
            </div>
            <div class="h-stat">
              <div class="h-stat-num"><span class="counter">MySQL</span></div>
              <div class="h-stat-lbl">Backend</div>
            </div>
          </div>
        </div>
    """, unsafe_allow_html=True)

    # Security Tools section with holographic shimmer
    st.markdown("""
        <div class="sec">Security Tools</div>
        <div class="tgrid">
          <div class="tc" style="--tc:#00d4ff;--t2:#00ff88;--tc-rgb:0,212,255">
            <div class="holo-shimmer"></div>
            <div class="tc-inner">
              <div><span class="tc-dot"></span><span class="tc-name">CrowdStrike Falcon</span></div>
              <div class="tc-cat">EDR - Endpoint Detection</div>
              <div class="tc-desc">Tracks alerts, MTTR, severity distribution and MITRE tactic coverage across your fleet.</div>
            </div>
          </div>
          <div class="tc" style="--tc:#a855f7;--t2:#c084fc;--tc-rgb:168,85,247">
            <div class="holo-shimmer"></div>
            <div class="tc-inner">
              <div><span class="tc-dot"></span><span class="tc-name">Cyble</span></div>
              <div class="tc-cat">Threat Intel - Dark Web</div>
              <div class="tc-desc">Monitors dark web mentions, keywords, source distribution and alert ratios.</div>
            </div>
          </div>
          <div class="tc" style="--tc:#f43f5e;--t2:#fb7185;--tc-rgb:244,63,94">
            <div class="holo-shimmer"></div>
            <div class="tc-inner">
              <div><span class="tc-dot"></span><span class="tc-name">SIEM</span></div>
              <div class="tc-cat">Security Event Management</div>
              <div class="tc-desc">Analyzes events, false positive rates, alert categories and validation status.</div>
            </div>
          </div>
          <div class="tc" style="--tc:#ffb800;--t2:#fcd34d;--tc-rgb:255,184,0">
            <div class="holo-shimmer"></div>
            <div class="tc-inner">
              <div><span class="tc-dot"></span><span class="tc-name">Trend Vision</span></div>
              <div class="tc-cat">Email - Cloud Protection</div>
              <div class="tc-desc">Surfaces phishing threats, quarantine rates and security filter performance.</div>
            </div>
          </div>
          <div class="tc" style="--tc:#00ff88;--t2:#34d399;--tc-rgb:0,255,136">
            <div class="holo-shimmer"></div>
            <div class="tc-inner">
              <div><span class="tc-dot"></span><span class="tc-name">Netskope</span></div>
              <div class="tc-cat">Endpoint - Network Security</div>
              <div class="tc-desc">Reports device coverage, OS spread, tunnel status and security enable rates.</div>
            </div>
          </div>
          <div class="tc" style="--tc:#14b8a6;--t2:#2dd4bf;--tc-rgb:20,184,166">
            <div class="holo-shimmer"></div>
            <div class="tc-inner">
              <div><span class="tc-dot"></span><span class="tc-name">Com Olho</span></div>
              <div class="tc-cat">Vuln Management - Bug Bounty</div>
              <div class="tc-desc">Tracks vulnerabilities, SLA breach rates, average age and bug bounty rewards.</div>
            </div>
          </div>
        </div>
    """, unsafe_allow_html=True)

    # How It Works section with connector line
    st.markdown("""
        <div class="sec">How It Works</div>
        <div class="sgrid">
          <div class="sc" style="--sa:#00d4ff;--sa-rgb:0,212,255">
            <div class="sc-inner">
              <div class="sc-num">01</div>
              <div class="sc-title">Upload</div>
              <div class="sc-desc">Drop your Excel export. Duplicate detection prevents re-processing the same file.</div>
            </div>
          </div>
          <div class="sc" style="--sa:#a855f7;--sa-rgb:168,85,247">
            <div class="sc-inner">
              <div class="sc-num">02</div>
              <div class="sc-title">Ingest</div>
              <div class="sc-desc">Data is parsed, cleaned and stored in tool-specific MySQL tables.</div>
            </div>
          </div>
          <div class="sc" style="--sa:#00ff88;--sa-rgb:0,255,136">
            <div class="sc-inner">
              <div class="sc-num">03</div>
              <div class="sc-title">Compute</div>
              <div class="sc-desc">The KPI engine processes raw records and writes metrics into kpi_master.</div>
            </div>
          </div>
          <div class="sc" style="--sa:#ffb800;--sa-rgb:255,184,0">
            <div class="sc-inner">
              <div class="sc-num">04</div>
              <div class="sc-title">Visualize</div>
              <div class="sc-desc">Filter by date on the Dashboard. Live Plotly charts render for every tool.</div>
            </div>
          </div>
        </div>
    """, unsafe_allow_html=True)

    # Bottom band section
    st.markdown("""
        <div class="bband">
          <div class="bb-card">
            <div class="bb-lbl">// Tech Stack</div>
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
            <div class="bb-lbl">// Pipeline</div>
            <div class="bb-pipe">
              Upload an Excel export then head to <strong>Compute KPI</strong>
              to run the analytics engine then open the <strong>Dashboard</strong>,
              pick a date range and explore charts for every tool.
            </div>
          </div>
          <div class="bb-dark">
            <div class="bb-dark-lbl">// Built by</div>
            <div class="bb-dark-name">Gurleen Kaur<br><span class="gradient">Bali</span></div>
            <div class="bb-dark-sub">Cyber Defense SOC Platform</div>
          </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
