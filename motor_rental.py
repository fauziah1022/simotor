import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import simotor as db
import io

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="SIMOTOR - Rental Motor Asoka",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ MODERN DESIGN SYSTEM ============
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap');

:root {
    --ink: #0f172a;
    --violet: #6366f1;
    --violet-soft: #818cf8;
    --violet-dark: #4f46e5;
    --cyan: #06b6d4;
    --cyan-soft: #22d3ee;
    --amber: #f59e0b;
    --amber-soft: #fbbf24;
    --rose: #f43f5e;
    --rose-soft: #fb7185;
    --emerald: #10b981;
    --emerald-soft: #34d399;
    --slate: #475569;
    --slate-dark: #1e293b;
    --slate-light: #94a3b8;
    --surface: #ffffff;
    --surface-glass: rgba(255, 255, 255, 0.72);
    --border-glass: rgba(255, 255, 255, 0.6);
    --border-subtle: rgba(15, 23, 42, 0.08);
    --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.04), 0 1px 2px rgba(15, 23, 42, 0.06);
    --shadow-md: 0 4px 16px rgba(15, 23, 42, 0.06), 0 2px 4px rgba(15, 23, 42, 0.04);
    --shadow-lg: 0 12px 40px rgba(15, 23, 42, 0.08), 0 4px 12px rgba(15, 23, 42, 0.04);
    --shadow-xl: 0 24px 64px rgba(15, 23, 42, 0.12);
    --radius-sm: 8px;
    --radius-md: 14px;
    --radius-lg: 20px;
    --radius-xl: 28px;
}

/* ---------- Base ---------- */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--ink);
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: 
        radial-gradient(ellipse 80% 60% at 10% 0%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse 60% 50% at 90% 10%, rgba(6, 182, 212, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse 70% 50% at 50% 100%, rgba(245, 158, 11, 0.04) 0%, transparent 50%),
        linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    background-attachment: fixed;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Manrope', sans-serif !important;
    letter-spacing: -0.02em;
    color: var(--ink) !important;
}

p, span, label, div {
    font-family: 'Inter', sans-serif !important;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.1) !important;
}

[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label { 
    color: rgba(255, 255, 255, 0.92) !important; 
}

[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { 
    color: white !important; 
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] hr { 
    border-color: rgba(255, 255, 255, 0.1) !important;
    margin: 1rem 0 !important;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 6px !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1rem !important;
    margin-bottom: 4px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.18) !important;
    transform: translateX(4px);
}

[data-testid="stSidebar"] [role="radiogroup"] input:checked + div {
    background: linear-gradient(135deg, var(--violet), var(--violet-dark)) !important;
    border-color: transparent !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4) !important;
    color: white !important;
}

/* ========== LOGOUT BUTTON - SIDEBAR ========== */
/* Tombol logout dengan background merah gelap */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3) !important;
    letter-spacing: 0.3px !important;
}

/* Hover: lebih terang */
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    transform: translateY(-2px) !important;
}

/* Active */
[data-testid="stSidebar"] .stButton > button:active {
    background: linear-gradient(135deg, #b91c1c 0%, #991b1b 100%) !important;
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3) !important;
}

/* ========== HEADER BANNER ========== */
.main-header {
    position: relative;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 40%, #06b6d4 100%);
    padding: 2rem 2.5rem;
    border-radius: var(--radius-xl);
    color: white;
    margin-bottom: 2rem;
    box-shadow: 
        0 20px 48px rgba(99, 102, 241, 0.25),
        0 8px 16px rgba(99, 102, 241, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.main-header::before {
    content: "";
    position: absolute;
    top: -50%; right: -10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
    pointer-events: none;
}

.main-header::after {
    content: "";
    position: absolute;
    bottom: -30%; left: 20%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(6, 182, 212, 0.3) 0%, transparent 70%);
    pointer-events: none;
}

.main-header h1 {
    margin: 0; 
    font-weight: 800; 
    font-size: 1.8rem;
    font-family: 'Manrope', sans-serif;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 1;
}

.main-header p { 
    margin: 0.5rem 0 0 0; 
    opacity: 0.95; 
    font-size: 0.95rem;
    position: relative;
    z-index: 1;
    font-weight: 400;
}

.main-header .eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    opacity: 0.85;
    display: block;
    margin-bottom: 0.4rem;
    position: relative;
    z-index: 1;
    font-weight: 600;
}

/* ========== GLASS PANELS ========== */
.glass-panel {
    background: var(--surface-glass);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 1.5rem 1.75rem;
    box-shadow: var(--shadow-lg);
    margin-bottom: 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-panel:hover {
    box-shadow: var(--shadow-xl);
    border-color: rgba(99, 102, 241, 0.15);
}

.glass-panel h3, 
.glass-panel .panel-title {
    margin-top: 0;
    margin-bottom: 1rem;
    font-family: 'Manrope', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ========== SCROLLABLE STATS CONTAINER ========== */
.stats-scroll-container {
    display: flex;
    gap: 1.2rem;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 1rem 0.5rem 1.5rem 0.5rem;
    margin: 0 -0.5rem;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
    scrollbar-color: rgba(99, 102, 241, 0.3) transparent;
}

.stats-scroll-container::-webkit-scrollbar {
    height: 6px;
}

.stats-scroll-container::-webkit-scrollbar-track {
    background: rgba(15, 23, 42, 0.04);
    border-radius: 3px;
}

.stats-scroll-container::-webkit-scrollbar-thumb {
    background: linear-gradient(90deg, var(--violet), var(--cyan));
    border-radius: 3px;
}

.stats-scroll-container::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(90deg, var(--violet-dark), var(--cyan-soft));
}

/* ========== STAT CARDS ========== */
.stat-card {
    position: relative;
    background: var(--surface);
    backdrop-filter: blur(16px);
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    border: 1px solid var(--border-subtle);
    box-shadow: var(--shadow-md);
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    min-width: 220px;
    max-width: 220px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 150px;
}

.stat-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; 
    height: 4px;
    background: linear-gradient(90deg, var(--violet), var(--cyan));
}

.stat-card.green::before  { background: linear-gradient(90deg, var(--emerald), var(--cyan-soft)); }
.stat-card.orange::before { background: linear-gradient(90deg, var(--amber), var(--amber-soft)); }
.stat-card.red::before    { background: linear-gradient(90deg, var(--rose), var(--rose-soft)); }
.stat-card.purple::before { background: linear-gradient(90deg, var(--violet), var(--violet-soft)); }

.stat-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-xl);
    border-color: rgba(99, 102, 241, 0.2);
}

.stat-card h3 {
    font-size: 0.78rem; 
    color: var(--slate); 
    margin: 0;
    text-transform: uppercase; 
    letter-spacing: 0.05em; 
    font-weight: 700;
    font-family: 'Inter', sans-serif !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
}

.stat-card .value {
    font-size: 2.2rem; 
    font-weight: 800; 
    color: var(--ink); 
    margin: 0.5rem 0 0 0;
    font-family: 'Manrope', sans-serif;
    line-height: 1;
}

.stat-card .icon {
    font-size: 1.6rem; 
    opacity: 0.6;
    flex-shrink: 0;
}

/* ========== FORM LABELS ========== */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stTextArea label,
.stDateInput label,
.stFileUploader label {
    color: #0f172a !important;
    font-weight: 800 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 0.6rem !important;
    display: block !important;
}

/* ========== FORM INPUTS ========== */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    background: var(--surface) !important;
    border: 2px solid rgba(15, 23, 42, 0.12) !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stSelectbox > div > div > div:focus-within,
.stTextArea > div > div > textarea:focus,
.stDateInput > div > div > input:focus {
    border-color: var(--violet) !important;
    box-shadow: 
        0 0 0 4px rgba(99, 102, 241, 0.12),
        0 4px 12px rgba(99, 102, 241, 0.1) !important;
    outline: none !important;
}

/* ========== LICENSE PLATE CHIP ========== */
.plate-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    padding: 0.35rem 0.75rem;
    border-radius: var(--radius-sm);
    border: 1.5px solid currentColor;
    text-transform: uppercase;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
}

.plate-chip::before { 
    content: "●"; 
    font-size: 0.55rem;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.plate-tersedia { color: #059669; background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); }
.plate-disewa   { color: #d97706; background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.3); }
.plate-rusak    { color: #e11d48; background: rgba(244, 63, 94, 0.1); border-color: rgba(244, 63, 94, 0.3); }
.plate-servis   { color: #475569; background: rgba(100, 116, 139, 0.1); border-color: rgba(100, 116, 139, 0.3); }
.plate-aktif    { color: #6366f1; background: rgba(99, 102, 241, 0.1); border-color: rgba(99, 102, 241, 0.3); }
.plate-selesai  { color: #059669; background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); }

/* ========== TABLES ========== */
.stDataFrame { 
    border-radius: var(--radius-md); 
    overflow: hidden;
    border: 1px solid var(--border-subtle);
}

[data-testid="stDataFrame"] {
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border-subtle);
}

[data-testid="stDataFrame"] thead tr th {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%) !important;
    color: var(--slate-dark) !important;
    font-weight: 700 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 0.9rem 1rem !important;
    border-bottom: 2px solid rgba(99, 102, 241, 0.1) !important;
}

[data-testid="stDataFrame"] tbody tr:hover {
    background: rgba(99, 102, 241, 0.03) !important;
}

[data-testid="stDataFrame"] tbody td {
    padding: 0.75rem 1rem !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    font-size: 0.88rem !important;
}

/* ========== BUTTONS (MAIN CONTENT) ========== */
.stButton > button {
    background: linear-gradient(135deg, var(--violet) 0%, var(--violet-dark) 100%);
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.65rem 1.6rem !important;
    font-weight: 700 !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 0.9rem !important;
    box-shadow: 
        0 4px 12px rgba(99, 102, 241, 0.3),
        0 2px 4px rgba(99, 102, 241, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.01em;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 
        0 8px 24px rgba(99, 102, 241, 0.4),
        0 4px 8px rgba(99, 102, 241, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

.stButton > button:active { 
    transform: translateY(0) !important;
    box-shadow: 
        0 2px 8px rgba(99, 102, 241, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
}

/* ========== LOGIN BOX ========== */
.login-shell {
    max-width: 440px;
    margin: 5vh auto 0;
    padding: 2.8rem 3rem;
    background: var(--surface-glass);
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-xl);
}

.login-logo-wrap {
    width: 72px; 
    height: 72px;
    border-radius: var(--radius-lg);
    background: linear-gradient(135deg, var(--violet), var(--cyan));
    display: flex; 
    align-items: center; 
    justify-content: center;
    font-size: 2rem;
    margin: 0 auto 1.2rem;
    box-shadow: 
        0 12px 32px rgba(99, 102, 241, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transition: transform 0.3s ease;
}

.login-logo-wrap:hover {
    transform: scale(1.05) rotate(-3deg);
}

.login-shell h2 {
    text-align: center; 
    color: var(--ink); 
    margin: 0;
    font-family: 'Manrope', sans-serif; 
    font-weight: 800;
    font-size: 1.8rem;
    letter-spacing: -0.02em;
}

.login-shell .sub {
    text-align: center; 
    color: var(--slate); 
    margin: 0.4rem 0 1.8rem 0; 
    font-size: 0.9rem;
    font-weight: 400;
}

/* Demo pills */
.demo-pill {
    display: inline-flex;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    background: rgba(99, 102, 241, 0.08);
    color: var(--violet-dark);
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    margin: 0 0.2rem;
    font-weight: 600;
    border: 1px solid rgba(99, 102, 241, 0.15);
}

/* ========== RECEIPT / STRUK ========== */
.struk-card {
    background: linear-gradient(160deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.7));
    backdrop-filter: blur(16px);
    padding: 1.8rem 2rem;
    border-radius: var(--radius-lg);
    margin-top: 1.5rem;
    border: 2px dashed rgba(99, 102, 241, 0.3);
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.struk-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--violet), var(--cyan));
}

.struk-card h3 { 
    text-align: center; 
    font-family: 'Manrope', sans-serif; 
    color: var(--ink);
    font-weight: 800;
    margin-bottom: 1rem;
}

.struk-card hr { 
    border-color: rgba(99, 102, 241, 0.2);
    margin: 1rem 0;
}

.struk-card .struk-total {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    color: var(--ink);
    font-size: 1.1rem;
}

/* ========== SECTION DIVIDERS ========== */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.2), transparent);
    margin: 2rem 0;
    border: none;
}

/* ========== TABS ========== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    background: rgba(255, 255, 255, 0.5) !important;
    padding: 6px !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: var(--surface) !important;
    box-shadow: var(--shadow-md) !important;
    color: var(--violet) !important;
}

/* ========== METRICS ========== */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    padding: 1.2rem 1.4rem !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-md) !important;
    border: 1px solid var(--border-subtle) !important;
    transition: all 0.25s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-lg) !important;
}

[data-testid="stMetric"] label {
    color: var(--slate-dark) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-weight: 700 !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    font-family: 'Manrope', sans-serif !important;
}

/* ========== ALERTS / MESSAGES ========== */
.stAlert {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 1rem 1.2rem !important;
}

/* ========== FILE UPLOADER ========== */
.stFileUploader > div {
    background: var(--surface) !important;
    border: 2px dashed rgba(99, 102, 241, 0.25) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.5rem !important;
    transition: all 0.2s ease !important;
}

.stFileUploader > div:hover {
    border-color: var(--violet) !important;
    background: rgba(99, 102, 241, 0.02) !important;
}

/* ========== HIDE STREAMLIT BRANDING ========== */
#MainMenu, header, footer { 
    visibility: hidden !important;
}

/* ========== SCROLLBAR STYLING ========== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(99, 102, 241, 0.2);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(99, 102, 241, 0.4);
}

/* ========== PLOTLY CHARTS CONTAINER ========== */
.js-plotly-plot {
    border-radius: var(--radius-md);
    overflow: hidden;
}

/* ========== RESPONSIVE ADJUSTMENTS ========== */
@media (max-width: 768px) {
    .main-header {
        padding: 1.5rem 1.8rem;
    }
    
    .main-header h1 {
        font-size: 1.4rem;
    }
    
    .stat-card {
        min-width: 200px;
        max-width: 200px;
    }
    
    .stat-card .value {
        font-size: 1.8rem;
    }
    
    .glass-panel {
        padding: 1.2rem 1.4rem;
    }
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============ SESSION STATE INIT ============
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

db.init_db()

# ============ HELPER FUNCTIONS ============
def format_rp(num):
    return f"Rp {int(num):,}".replace(",", ".")

def get_df(query, params=None):
    conn = db.get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()
    return df

def plate_chip(status):
    status_key = str(status).lower().strip()
    label_map = {
        'tersedia': 'Tersedia', 'disewa': 'Disewa', 'rusak': 'Rusak',
        'servis': 'Servis', 'aktif': 'Aktif', 'selesai': 'Selesai',
    }
    label = label_map.get(status_key, status)
    css_class = f"plate-{status_key}" if status_key in label_map else "plate-servis"
    return f'<span class="plate-chip {css_class}">{label}</span>'

def section_header(eyebrow, title, subtitle):
    st.markdown(f"""
    <div class="main-header">
        <span class="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def glass_open(title=None):
    title_html = f'<div class="panel-title">{title}</div>' if title else ""
    st.markdown(f'<div class="glass-panel">{title_html}', unsafe_allow_html=True)

def glass_close():
    st.markdown('</div>', unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#3A3F5C", size=12),
    margin=dict(t=20, l=10, r=10, b=10),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(15, 23, 42, 0.06)', zeroline=False),
    hoverlabel=dict(bgcolor='rgba(255, 255, 255, 0.95)', bordercolor='rgba(99, 102, 241, 0.2)', font=dict(size=13)),
)

# ============ LOGIN PAGE ============
def login_page():
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("""
        <div class="login-shell">
            <div class="login-logo-wrap">🏍️</div>
            <h2>SIMOTOR</h2>
            <p class="sub">Sistem Rental Motor Asoka &middot; Terdistribusi</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="cth. admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Masuk ke Dashboard →", use_container_width=True)

            if submitted:
                user = db.verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Username atau password salah. Coba lagi.")

        st.markdown("""
        <div style="text-align:center; margin-top:1rem; color:#64748B; font-size:0.85rem;">
            Demo &middot; Admin <span class="demo-pill">admin / admin123</span><br>
            Petugas <span class="demo-pill">petugas1 / petugas123</span>
        </div>
        """, unsafe_allow_html=True)

# ============ DASHBOARD PAGE ============
def dashboard_page():
    section_header("Ringkasan Operasional", " Dashboard", "Pantau performa rental hari ini secara langsung")

    today = datetime.now().strftime('%Y-%m-%d')
    trx_hari_ini = get_df("SELECT COUNT(*) c FROM transaksi WHERE tgl_sewa=?", (today,)).iloc[0]['c']
    motor_tersedia = get_df("SELECT COUNT(*) c FROM motor WHERE status='tersedia'").iloc[0]['c']
    motor_disewa = get_df("SELECT COUNT(*) c FROM motor WHERE status='disewa'").iloc[0]['c']
    pendapatan = get_df("SELECT COALESCE(SUM(total_bayar),0) t FROM pengembalian").iloc[0]['t']
    total_pelanggan = get_df("SELECT COUNT(*) c FROM pelanggan").iloc[0]['c']

    st.markdown(f"""
    <div class="stats-scroll-container">
        <div class="stat-card">
            <h3>Transaksi Hari Ini <span class="icon">📋</span></h3>
            <div class="value">{trx_hari_ini}</div>
        </div>
        <div class="stat-card green">
            <h3>Motor Tersedia <span class="icon">✅</span></h3>
            <div class="value">{motor_tersedia}</div>
        </div>
        <div class="stat-card orange">
            <h3>Motor Disewa <span class="icon">🏍️</span></h3>
            <div class="value">{motor_disewa}</div>
        </div>
        <div class="stat-card purple">
            <h3>Pendapatan <span class="icon">💰</span></h3>
            <div class="value" style="font-size:1.4rem;">{format_rp(pendapatan)}</div>
        </div>
        <div class="stat-card red">
            <h3>Pelanggan <span class="icon"></span></h3>
            <div class="value">{total_pelanggan}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        glass_open(" Transaksi 7 Hari Terakhir")
        df_trx = get_df("""
            SELECT tgl_sewa, COUNT(*) as jumlah 
            FROM transaksi 
            WHERE tgl_sewa >= date('now', '-7 days')
            GROUP BY tgl_sewa ORDER BY tgl_sewa
        """)
        if df_trx.empty:
            st.info("Belum ada transaksi dalam 7 hari terakhir.")
        else:
            fig = px.line(df_trx, x='tgl_sewa', y='jumlah', markers=True,
                          labels={'tgl_sewa':'Tanggal','jumlah':'Jumlah Transaksi'})
            fig.update_traces(line=dict(color='#6366f1', width=3), marker=dict(size=8, color='#06b6d4', line=dict(width=2, color='white')))
            fig.update_layout(height=320, **PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        glass_close()

    with col2:
        glass_open("️ Status Motor")
        df_status = get_df("SELECT status, COUNT(*) as jumlah FROM motor GROUP BY status")
        if df_status.empty:
            st.info("Belum ada data motor.")
        else:
            colors = {'tersedia':'#10b981','disewa':'#f59e0b','rusak':'#f43f5e','servis':'#64748b'}
            fig = px.pie(df_status, values='jumlah', names='status',
                         color='status', color_discrete_map=colors, hole=0.65)
            fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=13)
            fig.update_layout(height=320, showlegend=False, **PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        glass_close()

    glass_open("💵 Pendapatan 30 Hari Terakhir")
    df_pendapatan = get_df("""
        SELECT tgl_kembali as tanggal, SUM(total_bayar) as pendapatan
        FROM pengembalian
        WHERE tgl_kembali >= date('now', '-30 days')
        GROUP BY tgl_kembali ORDER BY tgl_kembali
    """)
    if df_pendapatan.empty:
        st.info("Belum ada data pendapatan dalam 30 hari terakhir.")
    else:
        fig = px.area(df_pendapatan, x='tanggal', y='pendapatan',
                      labels={'tanggal':'Tanggal','pendapatan':'Pendapatan (Rp)'})
        fig.update_traces(fillcolor='rgba(99, 102, 241, 0.15)', line=dict(color='#6366f1', width=2.5))
        fig.update_layout(height=320, **PLOTLY_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    glass_close()

    glass_open(" Transaksi Terbaru")
    df_recent = get_df("""
        SELECT t.id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.pelanggan_id = p.id
        JOIN motor m ON t.motor_id = m.id
        ORDER BY t.tgl_sewa DESC LIMIT 10
    """)
    if df_recent.empty:
        st.info("Belum ada transaksi.")
    else:
        df_recent['total_biaya'] = df_recent['total_biaya'].apply(format_rp)
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    glass_close()

# ============ MOTOR PAGE ============
def motor_page():
    section_header("Armada", "🏍️ Manajemen Motor", "Kelola data, status, dan foto armada motor rental")

    glass_open()
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Cari motor (nopol/merek)")
    with col2:
        filter_status = st.selectbox("Filter Status", ["semua","tersedia","disewa","rusak","servis"])
    glass_close()

    query = "SELECT * FROM motor WHERE 1=1"
    params = []
    if search:
        query += " AND (nopol LIKE ? OR merek LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like])
    if filter_status != "semua":
        query += " AND status = ?"
        params.append(filter_status)

    df = get_df(query, tuple(params) if params else None)

    if st.button("➕ Tambah Motor Baru"):
        st.session_state.show_motor_form = True

    if st.session_state.get('show_motor_form'):
        glass_open("Tambah Motor Baru")
        with st.form("motor_form"):
            c1, c2 = st.columns(2)
            with c1:
                nopol = st.text_input("Nomor Polisi *")
                merek = st.text_input("Merek *")
                jenis = st.text_input("Jenis Motor")
            with c2:
                tarif_jam = st.number_input("Tarif/Jam", min_value=0, value=10000)
                tarif_hari = st.number_input("Tarif/Hari", min_value=0, value=80000)
                status = st.selectbox("Status", ["tersedia","disewa","rusak","servis"])
                foto = st.file_uploader("Upload Foto Motor", type=["jpg","jpeg","png"])
                keterangan = st.text_area("Keterangan Motor")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.form_submit_button("💾 Simpan", use_container_width=True):
                    if nopol and merek:
                        conn = db.get_connection()
                        try:
                            foto_data = foto.read() if foto else None
                            conn.execute("""
                            INSERT INTO motor
                            (nopol,merek,jenis,tarif_jam,tarif_hari,status,cabang,foto,keterangan)
                            VALUES (?,?,?,?,?,?,?,?,?)
                            """,
                            (nopol, merek, jenis, tarif_jam, tarif_hari, status, 'Cabang Asoka', foto_data, keterangan))
                            conn.commit()
                            st.success("✅ Motor berhasil ditambahkan!")
                            st.session_state.show_motor_form = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                        finally:
                            conn.close()
                    else:
                        st.error("Nomor Polisi dan Merek wajib diisi!")
            with col_b:
                if st.form_submit_button("❌ Batal", use_container_width=True):
                    st.session_state.show_motor_form = False
                    st.rerun()
        glass_close()

    if not df.empty:
        glass_open(f"Daftar Motor ({len(df)})")
        df_display = df[['nopol','merek','jenis','tarif_jam','tarif_hari','status']].copy()
        df_display['tarif_jam'] = df_display['tarif_jam'].apply(format_rp)
        df_display['tarif_hari'] = df_display['tarif_hari'].apply(format_rp)
        df_display['status'] = df_display['status'].apply(lambda s: s.upper())
        st.dataframe(
            df_display,
            use_container_width=True, hide_index=True,
            column_config={
                "nopol": "Nopol", "merek": "Merek", "jenis": "Jenis",
                "tarif_jam": "Tarif/Jam", "tarif_hari": "Tarif/Hari", "status": "Status",
            }
        )
        glass_close()

        glass_open("✏️ Edit / Hapus Motor")
        selected = st.selectbox("Pilih Motor", df['nopol'].tolist())
        if selected:
            motor = df[df['nopol']==selected].iloc[0]
            st.markdown(plate_chip(motor['status']), unsafe_allow_html=True)
            st.write("")

            if 'foto' in motor.index and motor['foto'] is not None:
                st.image(bytes(motor['foto']), width=250, caption=motor['nopol'])
            
            c1, c2, c3 = st.columns(3)
            with c1:
                new_status = st.selectbox("Ubah Status", ["tersedia","disewa","rusak","servis"],
                    index=["tersedia","disewa","rusak","servis"].index(motor['status']))
                new_foto = st.file_uploader("Ganti Foto Motor", type=["jpg","jpeg","png"], key="edit_foto")
                new_keterangan = st.text_area("Keterangan Motor",
                    value=motor['keterangan'] if ('keterangan' in motor.index and motor['keterangan'] is not None) else "")
                if st.button("💾 Update Motor"):
                    conn = db.get_connection()
                    try:
                        if new_foto:
                            foto_data = new_foto.read()
                            conn.execute("UPDATE motor SET status=?, foto=?, keterangan=? WHERE id=?",
                                (new_status, foto_data, new_keterangan, int(motor['id'])))
                        else:
                            conn.execute("UPDATE motor SET status=?, keterangan=? WHERE id=?",
                                (new_status, new_keterangan, int(motor['id'])))
                        conn.commit()
                        st.success("✅ Data motor berhasil diperbarui!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        conn.close()
            with c2:
                if st.button("🗑️ Hapus Motor"):
                    conn = db.get_connection()
                    try:
                        conn.execute("DELETE FROM motor WHERE id=?", (int(motor['id']),))
                        conn.commit()
                        st.success("Motor dihapus!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        conn.close()
        glass_close()
    else:
        st.info("Tidak ada data motor yang cocok.")

# ============ PELANGGAN PAGE ============
def pelanggan_page():
    section_header("Database", " Manajemen Pelanggan", "Kelola data pelanggan rental")

    tab1, tab2 = st.tabs([" Daftar Pelanggan", "➕ Tambah Pelanggan"])

    with tab1:
        glass_open()
        search = st.text_input("Cari pelanggan")
        if search:
            like = f"%{search}%"
            df = get_df("SELECT * FROM pelanggan WHERE nama LIKE ? OR ktp LIKE ?", (like, like))
        else:
            df = get_df("SELECT * FROM pelanggan")
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pelanggan")
        glass_close()

    with tab2:
        glass_open()
        with st.form("pel_form"):
            c1, c2 = st.columns(2)
            with c1:
                nama = st.text_input("Nama Lengkap *")
                ktp = st.text_input("Nomor KTP *")
            with c2:
                telepon = st.text_input("Nomor Telepon")
                alamat = st.text_area("Alamat")

            if st.form_submit_button("💾 Simpan Pelanggan"):
                if nama and ktp:
                    conn = db.get_connection()
                    try:
                        conn.execute("INSERT INTO pelanggan (nama,ktp,alamat,telepon) VALUES (?,?,?,?)",
                                    (nama, ktp, alamat, telepon))
                        conn.commit()
                        st.success("✅ Pelanggan berhasil ditambahkan!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e} (KTP mungkin sudah terdaftar)")
                    finally:
                        conn.close()
                else:
                    st.error("Nama dan KTP wajib diisi!")
        glass_close()

# ============ TRANSAKSI PAGE ============
def transaksi_page():
    section_header("Operasional", "🧾 Transaksi Penyewaan", "Buat transaksi sewa motor baru")

    tab1, tab2, tab3 = st.tabs(["➕ Sewa Baru", " Pengembalian", "📋 Riwayat"])

    with tab1:
        pel_list = get_df("SELECT id, nama, ktp FROM pelanggan")
        motor_list = get_df("SELECT id, nopol, merek, tarif_jam, tarif_hari FROM motor WHERE status='tersedia'")

        if pel_list.empty or motor_list.empty:
            st.warning("Data pelanggan atau motor tersedia kosong!")
            return

        glass_open()
        with st.form("trx_form"):
            c1, c2 = st.columns(2)
            with c1:
                pel_choice_id = st.selectbox("Pilih Pelanggan", pel_list['id'].tolist(),
                    format_func=lambda pid: f"{pel_list.loc[pel_list['id']==pid, 'nama'].values[0]} ({pel_list.loc[pel_list['id']==pid, 'ktp'].values[0]})")
                pel_id = int(pel_choice_id)

                motor_choice_id = st.selectbox("Pilih Motor", motor_list['id'].tolist(),
                    format_func=lambda mid: f"{motor_list.loc[motor_list['id']==mid, 'nopol'].values[0]} - {motor_list.loc[motor_list['id']==mid, 'merek'].values[0]}")
                motor_row = motor_list[motor_list['id'] == motor_choice_id].iloc[0]
                motor_sel = f"{motor_row['nopol']} - {motor_row['merek']}"
            with c2:
                durasi = st.number_input("Durasi", min_value=1, value=1)
                satuan = st.selectbox("Satuan", ["hari","jam"])
                tarif = motor_row['tarif_hari'] if satuan == 'hari' else motor_row['tarif_jam']
                total = tarif * durasi
                st.metric("Total Biaya", format_rp(total))

            if st.form_submit_button("✅ Simpan Transaksi"):
                conn = db.get_connection()
                try:
                    conn.execute("""INSERT INTO transaksi (pelanggan_id,motor_id,tgl_sewa,durasi,satuan,total_biaya,status,cabang) 
                                   VALUES (?,?,?,?,?,?,?,?)""",
                                (pel_id, int(motor_row['id']), datetime.now().strftime('%Y-%m-%d'), 
                                 durasi, satuan, total, 'aktif', 'Cabang Asoka'))
                    conn.execute("UPDATE motor SET status='disewa' WHERE id=?", (int(motor_row['id']),))
                    conn.commit()
                    st.success("✅ Transaksi berhasil disimpan!")

                    st.markdown(f"""
                    <div class="struk-card">
                        <h3> STRUK SEWA MOTOR</h3>
                        <hr>
                        <p><b>Tanggal:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
                        <p><b>Motor:</b> {motor_sel}</p>
                        <p><b>Durasi:</b> {durasi} {satuan}</p>
                        <p class="struk-total"><b>Total:</b> {format_rp(total)}</p>
                        <p style="text-align:center; margin-top:18px; color:#64748B;"><i>Terima kasih telah menggunakan layanan kami!</i></p>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
                st.rerun()
        glass_close()

    with tab2:
        trx_aktif = get_df("""
            SELECT t.id, t.motor_id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id = p.id
            JOIN motor m ON t.motor_id = m.id
            WHERE t.status='aktif'
        """)
        if trx_aktif.empty:
            st.info("Tidak ada transaksi aktif")
        else:
            glass_open(f"Transaksi Aktif ({len(trx_aktif)})")
            st.dataframe(trx_aktif, use_container_width=True, hide_index=True)
            selected = st.selectbox("Pilih Transaksi untuk Dikembalikan", trx_aktif['id'].tolist())
            tgl_kembali = st.date_input("Tanggal Kembali", datetime.now())

            if st.button(" Proses Pengembalian"):
                trx = trx_aktif[trx_aktif['id']==selected].iloc[0]
                tgl_sewa = datetime.strptime(trx['tgl_sewa'], '%Y-%m-%d')
                diff = (datetime.combine(tgl_kembali, datetime.min.time()) - tgl_sewa).days

                denda = 0
                if trx['satuan'] == 'hari' and diff > trx['durasi']:
                    denda = (diff - trx['durasi']) * 50000
                elif trx['satuan'] == 'jam' and diff * 24 > trx['durasi']:
                    denda = (diff * 24 - trx['durasi']) * 10000

                total_bayar = trx['total_biaya'] + denda

                conn = db.get_connection()
                try:
                    conn.execute("UPDATE transaksi SET status='selesai' WHERE id=?", (int(selected),))
                    conn.execute("UPDATE motor SET status='tersedia' WHERE id=?", (int(trx['motor_id']),))
                    conn.execute("INSERT INTO pengembalian (transaksi_id,tgl_kembali,denda,total_bayar) VALUES (?,?,?,?)",
                                (int(selected), tgl_kembali.strftime('%Y-%m-%d'), denda, total_bayar))
                    conn.commit()
                    st.success(f"✅ Pengembalian berhasil! Denda: {format_rp(denda)} | Total: {format_rp(total_bayar)}")
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
                st.rerun()
            glass_close()

    with tab3:
        df = get_df("""
            SELECT t.id, p.nama, m.nopol, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id = p.id
            JOIN motor m ON t.motor_id = m.id
            ORDER BY t.tgl_sewa DESC
        """)
        glass_open("Riwayat Transaksi")
        if df.empty:
            st.info("Belum ada riwayat transaksi.")
        else:
            df['total_biaya'] = df['total_biaya'].apply(format_rp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        glass_close()

# ============ LAPORAN PAGE ============
def laporan_page():
    section_header("Insight", " Laporan Cabang", "Laporan transaksi dan pendapatan per periode")

    glass_open()
    c1, c2, c3 = st.columns(3)
    with c1:
        periode = st.selectbox("Periode", ["Harian","Mingguan","Bulanan"])
    with c2:
        tanggal = st.date_input("Tanggal", datetime.now())
    with c3:
        st.write("")
        st.write("")
        export = st.button("📥 Export Excel")
    glass_close()

    tanggal_str = tanggal.strftime('%Y-%m-%d')
    if periode == "Harian":
        filter_clause = "DATE(t.tgl_sewa) = ?"
        filter_params = [tanggal_str]
    elif periode == "Mingguan":
        start = (tanggal - timedelta(days=7)).strftime('%Y-%m-%d')
        filter_clause = "t.tgl_sewa BETWEEN ? AND ?"
        filter_params = [start, tanggal_str]
    else:
        start = tanggal.replace(day=1).strftime('%Y-%m-%d')
        filter_clause = "t.tgl_sewa BETWEEN ? AND ?"
        filter_params = [start, tanggal_str]

    df = get_df(f"""
        SELECT t.id, t.motor_id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.pelanggan_id = p.id
        JOIN motor m ON t.motor_id = m.id
        WHERE {filter_clause}
        ORDER BY t.tgl_sewa DESC
    """, tuple(filter_params))

    st.markdown(f"""
    <div class="stats-scroll-container">
        <div class="stat-card">
            <h3>Total Transaksi <span class="icon"></span></h3>
            <div class="value">{len(df)}</div>
        </div>
        <div class="stat-card purple">
            <h3>Pendapatan <span class="icon">💰</span></h3>
            <div class="value" style="font-size:1.2rem;">{format_rp(df['total_biaya'].sum() if len(df) > 0 else 0)}</div>
        </div>
        <div class="stat-card orange">
            <h3>Rata-rata <span class="icon">📈</span></h3>
            <div class="value" style="font-size:1.2rem;">{format_rp(df['total_biaya'].mean() if len(df)>0 else 0)}</div>
        </div>
        <div class="stat-card green">
            <h3>Motor Tersewa <span class="icon">🏍️</span></h3>
            <div class="value">{df['motor_id'].nunique() if not df.empty else 0}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    glass_open(f"Detail Transaksi · {periode}")
    if df.empty:
        st.info("Tidak ada transaksi pada periode ini.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
    glass_close()

    if export and not df.empty:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Laporan')
        st.download_button("️ Download Excel", buffer.getvalue(),
                          f"laporan_{periode.lower()}_{tanggal}.xlsx",
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    elif export and df.empty:
        st.warning("Tidak ada data untuk diexport pada periode ini.")

# ============ ADMIN PAGE ============
def admin_page():
    section_header("Pusat Kendali", "🏢 Dashboard Admin Pusat", "Monitoring seluruh cabang rental motor")

    total_cabang = 1
    total_trx = get_df("SELECT COUNT(*) c FROM transaksi").iloc[0]['c']
    total_pelanggan = get_df("SELECT COUNT(*) c FROM pelanggan").iloc[0]['c']
    total_pendapatan = get_df("SELECT COALESCE(SUM(total_bayar),0) t FROM pengembalian").iloc[0]['t']

    st.markdown(f"""
    <div class="stats-scroll-container">
        <div class="stat-card">
            <h3>Total Cabang <span class="icon"></span></h3>
            <div class="value">{total_cabang}</div>
        </div>
        <div class="stat-card green">
            <h3>Total Transaksi <span class="icon">📋</span></h3>
            <div class="value">{total_trx}</div>
        </div>
        <div class="stat-card orange">
            <h3>Total Pelanggan <span class="icon">👥</span></h3>
            <div class="value">{total_pelanggan}</div>
        </div>
        <div class="stat-card purple">
            <h3>Pendapatan <span class="icon"></span></h3>
            <div class="value" style="font-size:1.15rem;">{format_rp(total_pendapatan)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        glass_open("📈 Tren Transaksi Bulanan")
        df_monthly = get_df("""
            SELECT strftime('%Y-%m', tgl_sewa) as bulan, COUNT(*) as jumlah
            FROM transaksi GROUP BY bulan ORDER BY bulan
        """)
        if df_monthly.empty:
            st.info("Belum ada data transaksi.")
        else:
            fig = px.bar(df_monthly, x='bulan', y='jumlah')
            fig.update_traces(marker_color='#6366f1', marker_line_width=0)
            fig.update_layout(height=300, **PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        glass_close()

    with col2:
        glass_open("🏍️ Motor Terpopuler")
        df_pop = get_df("""
            SELECT m.merek, COUNT(*) as jumlah 
            FROM transaksi t JOIN motor m ON t.motor_id = m.id
            GROUP BY m.merek ORDER BY jumlah DESC LIMIT 5
        """)
        if df_pop.empty:
            st.info("Belum ada data transaksi.")
        else:
            fig = px.bar(df_pop, x='jumlah', y='merek', orientation='h')
            fig.update_traces(marker_color='#06b6d4', marker_line_width=0)
            fig.update_layout(height=300, **PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        glass_close()

    glass_open(" Status Sinkronisasi Cabang")
    sync_data = pd.DataFrame({
        'Cabang': ['Cabang Asoka', 'Cabang Pusat'],
        'Status': ['🟢 Online', '🟢 Online'],
        'Last Sync': [datetime.now().strftime('%Y-%m-%d %H:%M'), 
                      (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')],
        'Data Pending': [0, 2]
    })
    st.dataframe(sync_data, use_container_width=True, hide_index=True)
    glass_close()

    glass_open("📷 Monitoring Motor Cabang")
    motor_df = get_df("SELECT id,nopol,merek,status,keterangan,foto FROM motor")

    if motor_df.empty:
        st.info("Belum ada data motor.")
    else:
        for idx, row in motor_df.iterrows():
            col1, col2 = st.columns([1,2])
            with col1:
                if row["foto"] is not None:
                    st.image(bytes(row["foto"]), width=220, caption=row["nopol"])
                else:
                    st.markdown("*Tidak ada foto*")
            with col2:
                st.write(f"**Motor:** {row['merek']}")
                st.markdown(plate_chip(row['status']), unsafe_allow_html=True)
                st.write(f"**Keterangan:** {row['keterangan'] if row['keterangan'] else '-'}")
                if row["foto"] is not None:
                    st.download_button("️ Download Foto", data=bytes(row["foto"]),
                        file_name=f"{row['nopol']}.jpg", mime="image/jpeg", key=f"dl_{row['id']}")
            if idx < len(motor_df) - 1:
                st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    glass_close()

# ============ MAIN APP ============
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding:1.2rem 0 0.6rem;">
            <div style="font-size:2.6rem;">🏍️</div>
            <h2 style="color:white; margin:0; font-size:1.3rem;">SIMOTOR</h2>
            <p style="color:#FFFFFF; opacity:0.85; font-size:0.82rem; margin-top:0.2rem;">Rental Motor Asoka</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px; padding:0.8rem 1rem; margin-bottom:0.8rem;">
            <div style="color:#FFFFFF; font-weight:700; font-size:0.95rem;">👤 {st.session_state.user['username']}</div>
            <div style="color:#FFFFFF; opacity:0.85; font-size:0.8rem; margin-top:0.25rem;">🏷️ {st.session_state.user['role'].capitalize()}</div>
            <div style="color:#FFFFFF; opacity:0.85; font-size:0.8rem;"> {st.session_state.user['cabang']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        if st.session_state.user['role'] == 'admin':
            menu = st.radio("Menu", [" Dashboard", " Laporan", " Admin Pusat"], label_visibility="collapsed")
        else:
            menu = st.radio("Menu", ["️ Motor", "👥 Pelanggan", "🧾 Transaksi"], label_visibility="collapsed")

        st.markdown("---")
        
        # Logout button - TANPA ICON PINTU
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

        st.markdown("""
        <div style="position:fixed; bottom:18px; left:24px; color:#FFFFFF; opacity:0.6; font-size:0.72rem;">
            SIMOTOR v2.0<br>© 2024 Asoka Rental
        </div>
        """, unsafe_allow_html=True)

    if "Dashboard" in menu: dashboard_page()
    elif "Motor" in menu: motor_page()
    elif "Pelanggan" in menu: pelanggan_page()
    elif "Transaksi" in menu: transaksi_page()
    elif "Laporan" in menu: laporan_page()
    elif "Admin" in menu:
        if st.session_state.user['role'] == 'admin':
            admin_page()
        else:
            st.error("❌ Akses ditolak! Hanya admin yang dapat mengakses halaman ini.")

if __name__ == "__main__":
    main()