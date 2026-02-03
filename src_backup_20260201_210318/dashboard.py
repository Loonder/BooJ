# -*- coding: utf-8 -*-
"""
Dashboard Web do BooJ System - Interface Premium (PT-BR)
Mobile-First, Responsive, LinkedIn-Ready
"""

import streamlit as st
import pandas as pd
import os
from math import ceil
from datetime import datetime, timedelta
from config import GOLD_KEYWORDS, DATA_DIR, OUTPUT_FILENAME, LOG_FILE
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="BooJ // Caçador de Vagas TI",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UTILS ---
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- CUSTOM CSS: PREMIUM TECH THEME ---
st.markdown("""
<style>
    /* FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    :root {
        --bg-main: #050505;
        --bg-sec: #0a0a0a;
        --card-bg: #111111;
        --card-border: #222222;
        --accent-primary: #6366f1; /* Indigo */
        --accent-secondary: #ec4899; /* Pink */
        --accent-cyan: #06b6d4; /* Cyan */
        --text-primary: #ffffff;
        --text-secondary: #a1a1aa;
        --btn-apply-bg: #22c55e; /* Green for better CTA */
        --btn-apply-hover: #16a34a;
        --font-main: 'Outfit', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* GLOBAL RESET */
    .stApp {
        background-color: var(--bg-main);
        font-family: var(--font-main);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-main) !important;
        color: var(--text-primary) !important;
        letter-spacing: -0.02em;
    }

    /* CUSTOM SCROLLBAR */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-main); }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #444; }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sec);
        border-right: 1px solid var(--card-border);
    }

    /* KPI CARDS - NEON GLOW */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 16px;
        margin-bottom: 32px;
    }
    
    .kpi-card {
        background: rgba(17, 17, 17, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, var(--accent-primary), var(--accent-cyan));
        opacity: 0.5;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3);
    }

    .kpi-value {
        font-family: var(--font-mono);
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
        background: linear-gradient(to right, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--text-secondary);
    }

    /* JOB LISTING CARDS - GLASSMORPHISM */
    .job-card {
        background: linear-gradient(145deg, #111 0%, #0d0d0d 100%);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .job-card:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    .job-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-primary);
        text-decoration: none;
        margin-bottom: 8px;
        display: block;
        transition: color 0.2s;
    }
    
    .job-title:hover {
        color: var(--accent-cyan);
    }

    .job-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        font-size: 0.85rem;
        color: var(--text-secondary);
        margin-bottom: 16px;
        font-family: var(--font-main);
    }
    
    .job-meta-item {
        display: flex;
        align-items: center;
        gap: 6px;
        background: rgba(255,255,255,0.03);
        padding: 4px 10px;
        border-radius: 6px;
    }

    /* TAGS */
    .tag {
        font-size: 0.75rem;
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 800; /* BOLD UX */
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .tag-level { background: rgba(99, 102, 241, 0.15); color: #c4b5fd; border: 1px solid rgba(99, 102, 241, 0.2); }
    .tag-gold { background: rgba(251, 191, 36, 0.1); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.2); box-shadow: 0 0 10px rgba(251, 191, 36, 0.1); }

    /* BUTTONS */
    .btn-apply {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 10px 24px;
        background: linear-gradient(135deg, var(--btn-apply-bg), var(--btn-apply-hover));
        color: #fff !important;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.9rem;
        transition: all 0.3s;
        border: 1px solid transparent;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .btn-apply:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.5);
        color: white;
    }

    /* GHOST ANIMATION */
    @keyframes float-ghost {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    
    .ghost-mascot {
        animation: float-ghost 4s ease-in-out infinite;
        filter: drop-shadow(0 0 15px rgba(99, 102, 241, 0.3));
    }

    /* INPUTS */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #111 !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* GLOBE ANIMATION CONTAINER */
    .globe-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
        perspective: 1000px;
    }
    
    .tech-header {
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .tech-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 16px 0 0 0;
        letter-spacing: -0.05em;
    }
    
    .tech-subtitle {
        color: var(--accent-cyan);
        font-family: var(--font-mono);
        font-size: 0.8rem;
        margin-top: 8px;
        opacity: 0.8;
    }

    /* SOCIAL LINKS (Restored) */
    .social-links {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 16px 0;
    }
    
    .social-icon {
        width: 36px; height: 36px;
        display: flex; align-items: center; justify-content: center;
        background: #1f1f23;
        border-radius: 8px;
        color: #a1a1aa;
        text-decoration: none;
        transition: 0.2s;
        border: 1px solid #333;
    }
    
    .social-icon:hover {
        background: var(--accent-primary);
        color: white;
        border-color: var(--accent-primary);
    }
    
    .social-icon svg { width: 18px; height: 18px; fill: currentColor; }

    /* PIX BOX (Restored) */
    .pix-box {
        background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px dashed var(--card-border);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin-top: 20px;
    }
    .pix-key {
        font-family: var(--font-mono);
        background: rgba(0,0,0,0.3);
        padding: 6px;
        border-radius: 4px;
        color: var(--accent-cyan);
        font-size: 0.8rem;
        margin: 8px 0;
    }

    /* PORTFOLIO BADGE */
    .portfolio-badge {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(10, 10, 10, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid #333;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #fff;
        text-decoration: none;
        z-index: 9999;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .portfolio-badge:hover {
        border-color: var(--accent-primary);
        background: rgba(99, 102, 241, 0.1);
    }

    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    button[kind="headerNoPadding"] { display: block !important; }
    
</style>
""", unsafe_allow_html=True)

# --- DATA LOGIC ---
from config import DB_PATH

@st.cache_data(ttl=300)
def load_data():
    """Load jobs and filter > 4 days old."""
    
    # 1. Load Data
    df = pd.DataFrame()
    if os.path.exists(DB_PATH):
        try:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query("SELECT * FROM jobs ORDER BY created_at DESC", conn)
            conn.close()
        except Exception as e:
            st.error(f"Erro ao carregar banco de dados: {e}")
    
    if df.empty:
        # Fallback to CSV if needed (simplified)
        CSV_PATH = os.path.join(DATA_DIR, OUTPUT_FILENAME.replace("data/", ""))
        if os.path.exists(CSV_PATH):
            df = pd.read_csv(CSV_PATH)

    if df.empty:
        return pd.DataFrame()

    # 2. Preprocessing
    if 'created_at' in df.columns:
        df['data_coleta'] = pd.to_datetime(df['created_at'], errors='coerce')
    elif 'data_coleta' in df.columns:
        df['data_coleta'] = pd.to_datetime(df['data_coleta'], errors='coerce')
    else:
        # If no date column, we can't filter by age properly
        return df

    # 3. FILTER: Remove jobs > 4 days old
    now = pd.Timestamp.now()
    cutoff_date = now - pd.Timedelta(days=2)
    
    if df['data_coleta'].dt.tz is not None:
        df['data_coleta'] = df['data_coleta'].dt.tz_localize(None)

    df = df[df['data_coleta'] >= cutoff_date]

    # 4. Deduplication
    if 'link' in df.columns:
        df = df.drop_duplicates(subset=['link'], keep='first')
    
    # Fuzzy Dedup
    df['titulo_lower'] = df['titulo'].str.lower().str.strip()
    df = df.drop_duplicates(subset=['titulo_lower', 'empresa'], keep='first')
    df = df.drop(columns=['titulo_lower'])

    return df

def get_seniority_tag(title):
    t = str(title).lower()
    if any(x in t for x in ["sênior", "senior", "lead", "especialista"]): return "Senior"
    if any(x in t for x in ["pleno", "mid"]): return "Pleno"
    if any(x in t for x in ["júnior", "junior", "jr"]): return "Júnior"
    if any(x in t for x in ["estágio", "estagio", "intern"]): return "Estágio"
    if "trainee" in t: return "Trainee"
    return "Geral"

# Load Data
df = load_data()

# Process Tags
if not df.empty:
    df['is_gold'] = df['titulo'].apply(lambda x: any(kw.lower() in str(x).lower() for kw in GOLD_KEYWORDS))
    df['tag'] = df['titulo'].apply(get_seniority_tag)
    
    # --- BLACKLIST LOGIC ---
    BLACKLIST_TERMS = ["emprego.pt", "net-empregos", "zaask", "cronoshare", "workana"]
    # We will filter later based on the toggle, but defining terms here or near config is better. 
    # Actually, let's keep it simple and filter in the 'APPLY FILTERS' section using the toggle variable.
    
    # Sort based on Sidebar Selection (needs to come after sidebar definition, moving logic below)
    pass 
    # Logic moved to after sidebar rendering to access sort_option


# --- SIDEBAR (Restored Features) ---
with st.sidebar:
    # Mascot with Animation logic
    mascot_html = ""
    # Image provided by user (already clean)
    mascot_img = "assets/boo_ghost_clean.png"
    
    # Fallback to original if clean doesn't exist (though we just copied it)
    if not os.path.exists(mascot_img):
        mascot_img = "assets/boo_ghost.png"

    if os.path.exists(mascot_img):
        bin_str = get_img_as_base64(mascot_img)
        mascot_html = f'<div style="text-align: center;"><img src="data:image/png;base64,{bin_str}" class="ghost-mascot" style="width: 140px; max-width: 100%; border-radius: 12px;"></div>'
    else:
        mascot_html = '<div style="font-size: 80px; text-align: center;" class="ghost-mascot">👻</div>'

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 24px;">
        <div style="margin-bottom: 16px;">
            {mascot_html.replace('width: 140px', 'width: 420px')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quality Control
    st.markdown("### 🛡️ Controle de Qualidade")
    remove_junk = st.toggle("Ocultar vagas suspeitas/ruins", value=True)
    if remove_junk:
        st.caption("Remove: emprego.pt, net-empregos, etc.")

    st.markdown("---")  # Divisor visual
    
    # SORTING CONTROL
    st.markdown("### 🔀 Ordenação")
    sort_option = st.selectbox(
        "Como deseja ver as vagas?",
        ["Mais Recentes", "Aleatório (Shuffle)", "Mais Antigas"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("### ⚙️ Filtros da Caçada")
    
    loc_options = ["Todas", "Remoto", "São Paulo", "Rio de Janeiro", "Minas Gerais", "Sul", "Nordeste"]
    sel_loc = st.selectbox("Localização", loc_options, label_visibility="collapsed")
    
    sel_level = st.multiselect("Nível", ["Estágio", "Júnior", "Pleno", "Senior"], default=["Estágio", "Júnior", "Pleno"])
    
    st.markdown("---")
    
    # Dev Profile & Socials (RESTORED)
    st.markdown("""
<div style="background: #111; border-radius: 12px; padding: 16px; border: 1px solid #222;">
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
<div style="width: 40px; height: 40px; background: #222; border-radius: 50%; display: flex; align-items: center; justify-content: center;">👨‍💻</div>
<div>
<div style="font-weight: 600; font-size: 0.9rem; color: #fff;">Paulo Moraes</div>
<div style="font-size: 0.7rem; color: #64748b;">Fullstack Engineer</div>
</div>
</div>
<div class="social-links">
<a href="https://linkedin.com/in/paulomoraesdev" target="_blank" class="social-icon" title="LinkedIn">
<svg viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
</a>
<a href="https://github.com/Loonder" target="_blank" class="social-icon" title="GitHub">
<svg viewBox="0 0 24 24"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
</a>
<a href="https://discord.gg/boojvagas" target="_blank" class="social-icon" title="Discord">
<svg viewBox="0 0 24 24"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/></svg>
</a>
</div>
<a href="https://paulomoraes.cloud" target="_blank" style="display: block; text-align: center; background: #222; color: #fff; text-decoration: none; padding: 8px; border-radius: 6px; font-size: 0.8rem; transition: 0.2s;">
🌐 Visitar Portfolio
</a>
</div>
""", unsafe_allow_html=True)
    
    # PIX (RESTORED)
    st.markdown("""
    <div class="pix-box">
        <div style="font-weight: 600; font-size: 0.9rem; color: #white;">☕ Apoie o projeto</div>
        <div class="pix-key">11941068987</div>
        <div style="font-size: 0.7rem; color: #a1a1aa;">Chave Pix (Celular)</div>
    </div>
    """, unsafe_allow_html=True)


# --- APPLY FILTERS & SORTING ---
# Moved here to access sidebar variables
if not df.empty and 'data_coleta' in df.columns:
    # 1. Quality Filter
    if remove_junk:
        junk_mask = df['link'].str.contains('emprego.pt|net-empregos|zaask|cronoshare', case=False, na=False) | \
                    df['empresa'].str.contains('emprego.pt|net-empregos', case=False, na=False)
        df = df[~junk_mask]

    # 2. Sorting
    if sort_option == "Mais Recentes":
        df = df.sort_values(by='data_coleta', ascending=False)
    elif sort_option == "Mais Antigas":
        df = df.sort_values(by='data_coleta', ascending=True)
    elif sort_option == "Aleatório (Shuffle)":
        df = df.sample(frac=1, random_state=None).reset_index(drop=True)

# --- MAIN CONTENT ---

# 1. HEADER with Tech Globe
globe_svg = """
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="width: 100px; height: 100px; animation: float 6s ease-in-out infinite;">
    <style>
        @keyframes rotate { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
        .globe-wire { fill: none; stroke: url(#grad1); stroke-width: 1.5; opacity: 0.8; }
        .globe-inner { fill: none; stroke: url(#grad2); stroke-width: 0.5; opacity: 0.3; }
    </style>
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ec4899;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
        </linearGradient>
    </defs>
    <circle cx="100" cy="100" r="90" class="globe-wire" />
    <ellipse cx="100" cy="100" rx="90" ry="30" class="globe-wire" transform="rotate(20 100 100)" />
    <ellipse cx="100" cy="100" rx="90" ry="30" class="globe-wire" transform="rotate(-20 100 100)" />
    <ellipse cx="100" cy="100" rx="90" ry="80" class="globe-inner" stroke-dasharray="4 4"/>
    <circle cx="100" cy="100" r="40" fill="url(#grad1)" opacity="0.1" />
</svg>
"""

st.html(f"""
<div class="tech-header">
    <div class="globe-container">
        {globe_svg}
    </div>
    <h1 class="tech-title">BooJ // SYSTEM</h1>
    <div class="tech-subtitle">ADVANCED JOB INTELLIGENCE PROTOCOL</div>
</div>
""")

# 2. METRICS
total_vagas = len(df)
gold_vagas = len(df[df['is_gold']]) if not df.empty else 0
# "Recent" in this context is just 24h as per general dashboard logic
today_vagas = 0
if not df.empty and 'data_coleta' in df.columns:
    today_vagas = len(df[df['data_coleta'] >= pd.Timestamp.now().normalize()])

col1, col2, col3 = st.columns(3)
with col1:
    st.html(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_vagas}</div>
        <div class="kpi-label">Vagas Ativas (4d)</div>
    </div>
    """)
with col2:
    st.html(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="background: linear-gradient(to right, #fbbf24, #d97706); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{gold_vagas}</div>
        <div class="kpi-label">Vagas Ouro</div>
    </div>
    """)
with col3:
    st.html(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="background: linear-gradient(to right, #34d399, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{today_vagas}</div>
        <div class="kpi-label">Encontradas Hoje</div>
    </div>
    """)

# 3. SEARCH & LIST
st.html("<div style='height: 30px;'></div>")
query = st.text_input("QUERY_DB", placeholder="Buscar por tecnologia, empresa...", label_visibility="collapsed")

# Filter Logic applied to DF
filtered_df = df.copy()

if query:
    mask = filtered_df['titulo'].str.contains(query, case=False, na=False) | \
           filtered_df['empresa'].str.contains(query, case=False, na=False)
    filtered_df = filtered_df[mask]

if sel_loc != "Todas":
    loc_map = {
        "Remoto": "remot|home",
        "São Paulo": "SP|São Paulo",
        "Rio de Janeiro": "RJ|Rio de Janeiro",
        "Minas Gerais": "MG|Minas Gerais",
        "Sul": "PR|SC|RS|Curitiba|Florian|Porto Alegre",
        "Nordeste": "BA|PE|CE|Recife|Salvador|Fortaleza"
    }
    term = loc_map.get(sel_loc, sel_loc)
    filtered_df = filtered_df[filtered_df['localizacao'].str.contains(term, case=False, na=False)]

if sel_level:
    filtered_df = filtered_df[filtered_df['tag'].isin(sel_level)]

# Pagination
PER_PAGE = 20
total_pages = max(ceil(len(filtered_df) / PER_PAGE), 1)
if 'page' not in st.session_state: st.session_state.page = 1

# Reset page on filter change
curr_hash = f"{query}_{sel_loc}_{len(sel_level)}"
if st.session_state.get('last_hash') != curr_hash:
    st.session_state.page = 1
    st.session_state.last_hash = curr_hash

start_idx = (st.session_state.page - 1) * PER_PAGE
page_df = filtered_df.iloc[start_idx : start_idx + PER_PAGE]

st.html(f"<div style='margin-bottom: 20px; color: #64748b; font-size: 0.8rem; font-family: monospace;'>// EXIBINDO {len(page_df)} DE {len(filtered_df)} RESULTADOS_</div>")

for _, row in page_df.iterrows():
    # Format Date
    date_disp = "N/A"
    if pd.notna(row['data_coleta']):
        date_disp = row['data_coleta'].strftime("%d/%m")
    
    # Gold Highlight
    border_style = "border-color: #fbbf24;" if row.get('is_gold') else ""
    glow_style = "box-shadow: 0 0 15px rgba(251, 191, 36, 0.15);" if row.get('is_gold') else ""
    
    tags_html = ""
    if row.get('is_gold'):
        tags_html += '<span class="tag tag-gold">GOLD</span>'
    tags_html += f'<span class="tag tag-level">{row["tag"]}</span>'

    st.html(f"""
    <div class="job-card" style="{border_style} {glow_style}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <a href="{row['link']}" target="_blank" class="job-title">{row['titulo']}</a>
                <div class="job-meta">
                    <span class="job-meta-item">🏢 {row['empresa']}</span>
                    <span class="job-meta-item">📍 {row['localizacao']}</span>
                    <span class="job-meta-item">🕒 {date_disp}</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="margin-bottom: 12px;">{tags_html}</div>
            </div>
        </div>
        <div style="display: flex; justify-content:space-between; align-items: flex-end; margin-top: 12px;">
            <div style="font-size: 0.75rem; color: #52525b; font-family: monospace;">PLATAFORMA: {row['plataforma'].upper()}</div>
            <a href="{row['link']}" target="_blank" class="btn-apply">APLICAR_</a>
        </div>
    </div>
    """)

# Pagination UI
if total_pages > 1:
    col_prev, col_pg, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("<< ANTERIOR", disabled=st.session_state.page <= 1, use_container_width=True):
            st.session_state.page -= 1
            st.rerun()
    with col_pg:
        st.html(f"<div style='text-align: center; color: #64748b; padding-top: 8px;'>PÁGINA {st.session_state.page} // {total_pages}</div>")
    with col_next:
        if st.button("PRÓXIMA >>", disabled=st.session_state.page >= total_pages, use_container_width=True):
            st.session_state.page += 1
            st.rerun()

# Floating Portfolio Badge
st.html("""
<a href="https://paulomoraes.cloud" target="_blank" class="portfolio-badge">
    <span>💎</span>
    <span>paulomoraes.cloud</span>
</a>
""")
