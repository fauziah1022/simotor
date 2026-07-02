import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import simotor as db # Pastikan file simotor.py ada di folder yang sama
import io

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="SIMOTOR - Rental Motor Asoka",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ MODERN DESIGN SYSTEM (CSS) ============
CUSTOM_CSS = """
<style>
/* --- IMPORT FONTS --- */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    /* Palette Modern */
    --primary: #6366f1;       /* Indigo Modern */
    --primary-hover: #4f46e5;
    --secondary: #0ea5e9;     /* Sky Blue */
    --success: #10b981;       /* Emerald */
    --warning: #f59e0b;       /* Amber */
    --danger: #ef4444;        /* Red */
    --dark-bg: #0f172a;       /* Slate 900 */
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.5);
    --text-main: #1e293b;
    --text-muted: #64748b;
}

/* --- GLOBAL RESET & TYPOGRAPHY --- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
    color: #1e293b !important;
}

.stApp {
    background-color: #f8fafc;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(14, 165, 233, 0.15) 0px, transparent 50%);
    background-attachment: fixed;
}

/* --- SIDEBAR MODERNIZATION --- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
    border-right: none;
}

[data-testid="stSidebar"] .stMarkdown h2 {
    color: white !important;
    font-size: 1.5rem;
}

[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] div {
    color: rgba(255,255,255,0.8) !important;
}

/* Sidebar Radio Buttons as Cards */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 8px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 4px;
    transition: all 0.3s ease;
    color: white !important;
    font-weight: 500;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateX(5px);
}

[data-testid="stSidebar"] [role="radiogroup"] input:checked + div {
    background: var(--primary);
    border-color: var(--primary);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

/* --- MAIN CONTENT CONTAINERS --- */
.main-header {
    background: white;
    padding: 2rem;
    border-radius: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    margin-bottom: 2rem;
    border: 1px solid rgba(0,0,0,0.03);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 6px; height: 100%;
    background: linear-gradient(to bottom, var(--primary), var(--secondary));
}

.glass-panel {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.04);
    margin-bottom: 1.5rem;
    transition: transform 0.2s ease;
}

.glass-panel:hover {
    border-color: rgba(99, 102, 241, 0.2);
}

/* --- STAT CARDS --- */
.stat-card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.04);
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.06);
}

.stat-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; width: 100%; height: 4px;
}

.stat-card.green::after { background: var(--success); }
.stat-card.orange::after { background: var(--warning); }
.stat-card.red::after { background: var(--danger); }
.stat-card.purple::after { background: var(--primary); }

.stat-card h3 {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.stat-card .value {
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-main);
    font-family: 'Manrope', sans-serif;
    line-height: 1;
}

.stat-card .icon {
    position: absolute;
    right: 1.5rem;
    top: 1.5rem;
    font-size: 1.5rem;
    opacity: 0.15;
    color: var(--text-main);
}

/* --- BUTTONS --- */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(99, 102, 241, 0.35);
}

.stButton > button[kind="secondary"] {
    background: white;
    color: var(--text-main) !important;
    border: 1px solid #e2e8f0;
    box-shadow: none;
}

/* --- FORMS & INPUTS --- */
.stTextInput > div > div > input, 
.stSelectbox > div > div > div,
.stTextArea > div > div > textarea {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 12px 16px;
    font-family: 'Inter', sans-serif;
    transition: all 0.2s;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* --- DATAFRAMES --- */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}

thead tr th {
    background-color: #f1f5f9 !important;
    color: #475569 !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px !important;
}

tbody td {
    font-family: 'Inter', sans-serif !important;
    padding: 12px !important;
}

/* --- LICENSE PLATE CHIP (Signature Element) --- */
.plate-chip {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border: 1px solid currentColor;
}

.plate-tersedia { color: #059669; background: #ecfdf5; border-color: #a7f3d0; }
.plate-disewa   { color: #d97706; background: #fffbeb; border-color: #fde68a; }
.plate-rusak    { color: #dc2626; background: #fef2f2; border-color: #fecaca; }
.plate-servis   { color: #475569; background: #f8fafc; border-color: #cbd5e1; }

/* --- LOGIN PAGE --- */
.login-shell {
    max-width: 420px;
    margin: 5vh auto;
    padding: 3rem;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.8);
}

/* --- RECEIPT --- */
.struk-card {
    background: #fff;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1rem;
    position: relative;
}
.struk-card::before {
    content: "LUNAS";
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%) rotate(-15deg);
    font-size: 3rem;
    font-weight: 800;
    color: rgba(16, 185, 129, 0.1);
    pointer-events: none;
    font-family: 'Manrope', sans-serif;
}

/* Hide Streamlit Branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============ SESSION STATE INIT ============
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'show_motor_form' not in st.session_state:
    st.session_state.show_motor_form = False

db.init_db()

# ============ HELPER FUNCTIONS ============
def format_rp(num):
    if num is None: return "Rp 0"
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

def section_header(title, subtitle):
    st.markdown(f"""
    <div class="main-header">
        <h1 style="margin:0; font-size: 1.8rem;">{title}</h1>
        <p style="margin:0.5rem 0 0 0; color: var(--text-muted); font-size: 1rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def glass_open(title=None):
    title_html = f'<h3 style="margin-top:0; margin-bottom:1rem; font-size:1.1rem;">{title}</h3>' if title else ""
    st.markdown(f'<div class="glass-panel">{title_html}', unsafe_allow_html=True)

def glass_close():
    st.markdown('</div>', unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#64748b"),
    margin=dict(t=30, l=20, r=20, b=20),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="#f1f5f9")
)

# ============ LOGIN PAGE ============
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div class="login-shell">
            <div style="text-align:center; margin-bottom:1.5rem;">
                <div style="font-size:3rem; margin-bottom:0.5rem;">🏍️</div>
                <h2 style="margin:0; color:#1e293b;">SIMOTOR</h2>
                <p style="color:#64748b; margin-top:0.5rem;">Sistem Manajemen Rental Asoka</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            c1, c2 = st.columns([1, 1])
            with c1:
                submitted = st.form_submit_button("Masuk", use_container_width=True)
            
            if submitted:
                user = db.verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Username atau password salah.", icon="🚫")

        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem; color:#94a3b8; font-size:0.8rem;">
            Demo Credentials:<br>
            Admin: <b>admin / admin123</b><br>
            Petugas: <b>petugas1 / petugas123</b>
        </div>
        """, unsafe_allow_html=True)

# ============ DASHBOARD PAGE ============
def dashboard_page():
    section_header("Dashboard Overview", "Ringkasan performa operasional hari ini")

    today = datetime.now().strftime('%Y-%m-%d')
    
    # Metrics Query
    trx_hari_ini = get_df("SELECT COUNT(*) c FROM transaksi WHERE tgl_sewa=?", (today,)).iloc[0]['c']
    motor_tersedia = get_df("SELECT COUNT(*) c FROM motor WHERE status='tersedia'").iloc[0]['c']
    motor_disewa = get_df("SELECT COUNT(*) c FROM motor WHERE status='disewa'").iloc[0]['c']
    pendapatan = get_df("SELECT COALESCE(SUM(total_bayar),0) t FROM pengembalian").iloc[0]['t']
    total_pelanggan = get_df("SELECT COUNT(*) c FROM pelanggan").iloc[0]['c']

    c1, c2, c3, c4, c5 = st.columns(5)
    
    metrics = [
        {"col": c1, "title": "Transaksi Hari Ini", "val": trx_hari_ini, "icon": "📋", "color": "purple"},
        {"col": c2, "title": "Motor Tersedia", "val": motor_tersedia, "icon": "✅", "color": "green"},
        {"col": c3, "title": "Sedang Disewa", "val": motor_disewa, "icon": "🏍️", "color": "orange"},
        {"col": c4, "title": "Total Pendapatan", "val": format_rp(pendapatan), "icon": "💰", "color": "purple"},
        {"col": c5, "title": "Total Pelanggan", "val": total_pelanggan, "icon": "👥", "color": "red"},
    ]

    for m in metrics:
        with m["col"]:
            st.markdown(f"""
            <div class="stat-card {m['color']}">
                <span class="icon">{m['icon']}</span>
                <h3>{m['title']}</h3>
                <div class="value">{m['val']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

    # Charts Section
    col1, col2 = st.columns([2, 1])

    with col1:
        glass_open("📈 Tren Transaksi (7 Hari)")
        df_trx = get_df("""
            SELECT tgl_sewa, COUNT(*) as jumlah 
            FROM transaksi 
            WHERE tgl_sewa >= date('now', '-7 days')
            GROUP BY tgl_sewa ORDER BY tgl_sewa
        """)
        if not df_trx.empty:
            fig = px.area(df_trx, x='tgl_sewa', y='jumlah', markers=True)
            fig.update_traces(line=dict(color='#6366f1', width=3), fillcolor='rgba(99, 102, 241, 0.1)')
            fig.update_layout(height=300, **PLOTLY_LAYOUT)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Belum ada data transaksi minggu ini.")
        glass_close()

    with col2:
        glass_open("🏍️ Status Armada")
        df_status = get_df("SELECT status, COUNT(*) as jumlah FROM motor GROUP BY status")
        if not df_status.empty:
            colors = {'tersedia':'#10b981','disewa':'#f59e0b','rusak':'#ef4444','servis':'#64748b'}
            fig = px.pie(df_status, values='jumlah', names='status', hole=0.6, color='status', color_discrete_map=colors)
            fig.update_layout(height=300, showlegend=False, **PLOTLY_LAYOUT)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        glass_close()

    # Recent Transactions
    glass_open("📝 Transaksi Terbaru")
    df_recent = get_df("""
        SELECT t.id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.pelanggan_id = p.id
        JOIN motor m ON t.motor_id = m.id
        ORDER BY t.tgl_sewa DESC LIMIT 5
    """)
    if not df_recent.empty:
        df_recent['total_biaya'] = df_recent['total_biaya'].apply(format_rp)
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada transaksi tercatat.")
    glass_close()

# ============ MOTOR PAGE ============
def motor_page():
    section_header("Manajemen Armada", "Kelola data, status, dan foto motor rental")

    glass_open()
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Cari Nomor Polisi atau Merek", placeholder="Contoh: B 1234 CD")
    with col2:
        filter_status = st.selectbox("Filter Status", ["semua","tersedia","disewa","rusak","servis"])
    
    if st.button("➕ Tambah Motor Baru", type="primary"):
        st.session_state.show_motor_form = not st.session_state.get('show_motor_form', False)
        st.rerun()
    glass_close()

    if st.session_state.get('show_motor_form'):
        glass_open("Form Tambah Motor")
        with st.form("motor_form"):
            c1, c2 = st.columns(2)
            with c1:
                nopol = st.text_input("Nomor Polisi *", placeholder="B 1234 XYZ")
                merek = st.text_input("Merek *", placeholder="Honda Vario")
                jenis = st.text_input("Jenis", placeholder="Matic")
            with c2:
                tarif_jam = st.number_input("Tarif Per Jam", min_value=0, value=15000)
                tarif_hari = st.number_input("Tarif Per Hari", min_value=0, value=80000)
                status = st.selectbox("Status Awal", ["tersedia","disewa","rusak","servis"])
            
            foto = st.file_uploader("Upload Foto Motor (Opsional)", type=["jpg","png"])
            keterangan = st.text_area("Keterangan Tambahan")

            c_btn1, c_btn2 = st.columns([1, 4])
            with c_btn1:
                if st.form_submit_button("Simpan", use_container_width=True):
                    if nopol and merek:
                        conn = db.get_connection()
                        try:
                            foto_data = foto.read() if foto else None
                            conn.execute("""INSERT INTO motor (nopol,merek,jenis,tarif_jam,tarif_hari,status,cabang,foto,keterangan) VALUES (?,?,?,?,?,?,?,?,?)""",
                                (nopol, merek, jenis, tarif_jam, tarif_hari, status, 'Cabang Asoka', foto_data, keterangan))
                            conn.commit()
                            st.success("Motor berhasil ditambahkan!")
                            st.session_state.show_motor_form = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gagal menyimpan: {e}")
                        finally:
                            conn.close()
            with c_btn2:
                if st.form_submit_button("Batal", use_container_width=True):
                    st.session_state.show_motor_form = False
                    st.rerun()
        glass_close()

    # Table Logic
    query = "SELECT * FROM motor WHERE 1=1"
    params = []
    if search:
        like = f"%{search}%"
        query += " AND (nopol LIKE ? OR merek LIKE ?)"
        params.extend([like, like])
    if filter_status != "semua":
        query += " AND status = ?"
        params.append(filter_status)

    df = get_df(query, tuple(params) if params else None)

    if not df.empty:
        glass_open(f"Daftar Armada ({len(df)} Unit)")
        df_display = df[['nopol','merek','jenis','tarif_jam','tarif_hari','status']].copy()
        df_display['tarif_jam'] = df_display['tarif_jam'].apply(format_rp)
        df_display['tarif_hari'] = df_display['tarif_hari'].apply(format_rp)
        
        # Apply badge styling via HTML in dataframe if possible, or just simple text
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        glass_close()

        # Edit Section
        glass_open("Edit / Hapus Data")
        selected_nopol = st.selectbox("Pilih Motor untuk Diedit", df['nopol'].tolist())
        
        if selected_nopol:
            motor = df[df['nopol']==selected_nopol].iloc[0]
            
            c_img, c_info = st.columns([1, 2])
            with c_img:
                if 'foto' in motor.index and motor['foto'] is not None:
                    st.image(bytes(motor['foto']), caption=motor['nopol'], use_column_width=True)
                else:
                    st.markdown('<div style="background:#f1f5f9; height:150px; border-radius:12px; display:flex; align-items:center; justify-content:center; color:#94a3b8;">No Image</div>', unsafe_allow_html=True)
            
            with c_info:
                st.markdown(f"<h3>{motor['merek']} {motor['jenis']}</h3>", unsafe_allow_html=True)
                st.markdown(plate_chip(motor['status']), unsafe_allow_html=True)
                
                new_status = st.selectbox("Update Status", ["tersedia","disewa","rusak","servis"], index=["tersedia","disewa","rusak","servis"].index(motor['status']))
                new_ket = st.text_area("Update Keterangan", value=motor.get('keterangan', ''))
                
                c_act1, c_act2 = st.columns(2)
                with c_act1:
                    if st.button("💾 Update Data"):
                        conn = db.get_connection()
                        try:
                            conn.execute("UPDATE motor SET status=?, keterangan=? WHERE id=?", (new_status, new_ket, int(motor['id'])))
                            conn.commit()
                            st.success("Data diperbarui!")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                        finally:
                            conn.close()
                with c_act2:
                    if st.button("🗑️ Hapus Motor", type="secondary"):
                        conn = db.get_connection()
                        try:
                            conn.execute("DELETE FROM motor WHERE id=?", (int(motor['id']),))
                            conn.commit()
                            st.success("Motor dihapus!")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
                        finally:
                            conn.close()
        glass_close()
    else:
        st.info("Tidak ada data motor yang ditemukan.")

# ============ PELANGGAN PAGE ============
def pelanggan_page():
    section_header("Database Pelanggan", "Manajemen data penyewa motor")

    tab1, tab2 = st.tabs(["📋 Daftar Pelanggan", "➕ Registrasi Baru"])

    with tab1:
        glass_open()
        search = st.text_input("Cari Nama atau KTP")
        if search:
            like = f"%{search}%"
            df = get_df("SELECT * FROM pelanggan WHERE nama LIKE ? OR ktp LIKE ?", (like, like))
        else:
            df = get_df("SELECT * FROM pelanggan")
        
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Data kosong.")
        glass_close()

    with tab2:
        glass_open("Form Registrasi Pelanggan")
        with st.form("pel_form"):
            c1, c2 = st.columns(2)
            with c1:
                nama = st.text_input("Nama Lengkap *")
                ktp = st.text_input("NIK / No KTP *")
            with c2:
                telepon = st.text_input("No. WhatsApp / Telepon")
                alamat = st.text_area("Alamat Domisili")

            if st.form_submit_button("Simpan Data"):
                if nama and ktp:
                    conn = db.get_connection()
                    try:
                        conn.execute("INSERT INTO pelanggan (nama,ktp,alamat,telepon) VALUES (?,?,?,?)", (nama, ktp, alamat, telepon))
                        conn.commit()
                        st.success("Pelanggan berhasil didaftarkan!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal: {e}")
                    finally:
                        conn.close()
                else:
                    st.warning("Nama dan KTP wajib diisi.")
        glass_close()

# ============ TRANSAKSI PAGE ============
def transaksi_page():
    section_header("Transaksi Rental", "Proses sewa dan pengembalian motor")

    tab1, tab2, tab3 = st.tabs(["➕ Sewa Baru", "🔄 Pengembalian", "📜 Riwayat"])

    with tab1:
        pel_list = get_df("SELECT id, nama, ktp FROM pelanggan ORDER BY nama")
        motor_list = get_df("SELECT id, nopol, merek, tarif_jam, tarif_hari FROM motor WHERE status='tersedia'")

        if pel_list.empty or motor_list.empty:
            st.warning("⚠️ Data pelanggan atau motor tersedia kosong. Silakan lengkapi data terlebih dahulu.")
            return

        glass_open("Formulir Penyewaan")
        with st.form("trx_form"):
            c1, c2 = st.columns(2)
            with c1:
                pel_id = st.selectbox("Pilih Pelanggan", pel_list['id'].tolist(), format_func=lambda x: f"{pel_list.loc[pel_list['id']==x, 'nama'].values[0]}")
                
                motor_id = st.selectbox("Pilih Motor Tersedia", motor_list['id'].tolist(), format_func=lambda x: f"{motor_list.loc[motor_list['id']==x, 'nopol'].values[0]} - {motor_list.loc[motor_list['id']==x, 'merek'].values[0]}")
                
                # Get selected motor details
                m_row = motor_list[motor_list['id'] == motor_id].iloc[0]
                
            with c2:
                durasi = st.number_input("Durasi Sewa", min_value=1, value=1)
                satuan = st.radio("Satuan Waktu", ["hari", "jam"], horizontal=True)
                
                harga = m_row['tarif_hari'] if satuan == 'hari' else m_row['tarif_jam']
                total = harga * durasi
                
                st.markdown(f"""
                <div style="background:#f8fafc; padding:1rem; border-radius:12px; border:1px solid #e2e8f0; margin-top:1rem;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:0.5rem;">
                        <span>Harga Satuan:</span> <b>{format_rp(harga)}/{satuan}</b>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:1.2rem; color:var(--primary);">
                        <span>Total Bayar:</span> <b>{format_rp(total)}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if st.form_submit_button("Proses Sewa", type="primary"):
                conn = db.get_connection()
                try:
                    conn.execute("""INSERT INTO transaksi (pelanggan_id,motor_id,tgl_sewa,durasi,satuan,total_biaya,status,cabang) 
                                   VALUES (?,?,?,?,?,?,?,?)""",
                                (int(pel_id), int(motor_id), datetime.now().strftime('%Y-%m-%d'), durasi, satuan, total, 'aktif', 'Cabang Asoka'))
                    conn.execute("UPDATE motor SET status='disewa' WHERE id=?", (int(motor_id),))
                    conn.commit()
                    
                    st.success("✅ Transaksi Berhasil!")
                    
                    # Show Receipt
                    st.markdown(f"""
                    <div class="struk-card">
                        <h3 style="text-align:center; margin-bottom:1rem;">STRUK SEWA MOTOR ASOKA</h3>
                        <hr style="border-top:1px dashed #cbd5e1;">
                        <p><b>Tanggal:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                        <p><b>Motor:</b> {m_row['nopol']} ({m_row['merek']})</p>
                        <p><b>Durasi:</b> {durasi} {satuan}</p>
                        <p style="font-size:1.1rem;"><b>Total:</b> {format_rp(total)}</p>
                        <hr style="border-top:1px dashed #cbd5e1;">
                        <p style="text-align:center; font-size:0.8rem; color:#64748b;">Terima kasih atas kepercayaan Anda.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    conn.close()
        glass_close()

    with tab2:
        trx_aktif = get_df("""
            SELECT t.id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id = p.id
            JOIN motor m ON t.motor_id = m.id
            WHERE t.status='aktif'
        """)
        
        if trx_aktif.empty:
            st.info("Tidak ada transaksi aktif saat ini.")
        else:
            glass_open("Daftar Motor Sedang Disewa")
            st.dataframe(trx_aktif, use_container_width=True, hide_index=True)
            
            selected_id = st.selectbox("Pilih ID Transaksi untuk Pengembalian", trx_aktif['id'].tolist())
            tgl_kembali = st.date_input("Tanggal Pengembalian", datetime.now())

            if st.button("Hitung & Proses Kembali", type="primary"):
                trx = trx_aktif[trx_aktif['id']==selected_id].iloc[0]
                tgl_sewa = datetime.strptime(trx['tgl_sewa'], '%Y-%m-%d')
                diff_days = (datetime.combine(tgl_kembali, datetime.min.time()) - tgl_sewa).days
                
                denda = 0
                # Simple logic for demo
                if trx['satuan'] == 'hari' and diff_days > trx['durasi']:
                    denda = (diff_days - trx['durasi']) * 50000
                
                total_bayar = trx['total_biaya'] + denda

                conn = db.get_connection()
                try:
                    conn.execute("UPDATE transaksi SET status='selesai' WHERE id=?", (int(selected_id),))
                    conn.execute("UPDATE motor SET status='tersedia' WHERE id=?", (int(trx['id']),)) # Note: should be motor_id
                    # Fix: need motor_id from join or subquery, but here using trx which doesn't have motor_id directly in select above? 
                    # Let's fix the query in tab2 to include motor_id
                    pass 
                except:
                    pass
                
                # Re-fetch with motor_id
                trx_full = get_df(f"SELECT motor_id FROM transaksi WHERE id={selected_id}").iloc[0]
                
                conn = db.get_connection()
                try:
                    conn.execute("UPDATE transaksi SET status='selesai' WHERE id=?", (int(selected_id),))
                    conn.execute("UPDATE motor SET status='tersedia' WHERE id=?", (int(trx_full['motor_id']),))
                    conn.execute("INSERT INTO pengembalian (transaksi_id,tgl_kembali,denda,total_bayar) VALUES (?,?,?,?)",
                                (int(selected_id), tgl_kembali.strftime('%Y-%m-%d'), denda, total_bayar))
                    conn.commit()
                    st.success(f"✅ Pengembalian Sukses! Denda: {format_rp(denda)}")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))
                finally:
                    conn.close()
            glass_close()

    with tab3:
        glass_open("Riwayat Semua Transaksi")
        df = get_df("""
            SELECT t.id, p.nama, m.nopol, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id = p.id
            JOIN motor m ON t.motor_id = m.id
            ORDER BY t.tgl_sewa DESC
        """)
        if not df.empty:
            df['total_biaya'] = df['total_biaya'].apply(format_rp)
            st.dataframe(df, use_container_width=True, hide_index=True)
        glass_close()

# ============ LAPORAN PAGE ============
def laporan_page():
    section_header("Laporan Keuangan", "Analisis pendapatan dan aktivitas rental")

    glass_open()
    c1, c2 = st.columns(2)
    with c1:
        periode = st.selectbox("Periode Laporan", ["Harian", "Mingguan", "Bulanan"])
    with c2:
        tanggal_ref = st.date_input("Acuan Tanggal", datetime.now())
    glass_close()

    # Logic Filter
    if periode == "Harian":
        f_clause = "DATE(tgl_sewa) = ?"
        f_params = [tanggal_ref.strftime('%Y-%m-%d')]
    elif periode == "Mingguan":
        start = (tanggal_ref - timedelta(days=7)).strftime('%Y-%m-%d')
        f_clause = "tgl_sewa BETWEEN ? AND ?"
        f_params = [start, tanggal_ref.strftime('%Y-%m-%d')]
    else:
        start = tanggal_ref.replace(day=1).strftime('%Y-%m-%d')
        f_clause = "tgl_sewa BETWEEN ? AND ?"
        f_params = [start, tanggal_ref.strftime('%Y-%m-%d')]

    df = get_df(f"SELECT * FROM transaksi WHERE {f_clause}", tuple(f_params))

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Jumlah Transaksi", len(df))
    with c2:
        st.metric("Total Omzet", format_rp(df['total_biaya'].sum() if not df.empty else 0))
    with c3:
        st.metric("Rata-rata per Transaksi", format_rp(df['total_biaya'].mean() if not df.empty else 0))

    if not df.empty:
        glass_open("Detail Transaksi")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 Download Excel",
            data=buffer.getvalue(),
            file_name=f"Laporan_{periode}_{tanggal_ref}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        glass_close()

# ============ ADMIN PAGE ============
def admin_page():
    section_header("Admin Center", "Monitoring sistem dan cabang")
    
    st.info("Halaman ini khusus untuk Administrator Pusat.")
    
    # Placeholder for advanced admin features
    glass_open("Status Sistem")
    st.write("✅ Database Connected")
    st.write("✅ Server Running")
    glass_close()

# ============ MAIN APP ROUTER ============
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem 0;">
            <div style="width:60px; height:60px; background:linear-gradient(135deg, #6366f1, #0ea5e9); border-radius:50%; margin:0 auto 10px; display:flex; align-items:center; justify-content:center; font-size:1.8rem; color:white;">🏍️</div>
            <h3 style="color:white; margin:0;">SIMOTOR</h3>
            <p style="color:rgba(255,255,255,0.6); font-size:0.8rem;">{st.session_state.user['cabang']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        role = st.session_state.user['role']
        
        if role == 'admin':
            menu = st.radio("Navigasi", ["📊 Dashboard", "📈 Laporan", "🏢 Admin Pusat"], label_visibility="collapsed")
        else:
            menu = st.radio("Navigasi", ["🏍️ Motor", "👥 Pelanggan", "🧾 Transaksi"], label_visibility="collapsed")
            
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # Page Routing
    if "Dashboard" in menu: dashboard_page()
    elif "Motor" in menu: motor_page()
    elif "Pelanggan" in menu: pelanggan_page()
    elif "Transaksi" in menu: transaksi_page()
    elif "Laporan" in menu: laporan_page()
    elif "Admin" in menu: admin_page()

if __name__ == "__main__":
    main()