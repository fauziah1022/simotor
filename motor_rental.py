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

# ============ CUSTOM CSS + HTML ============
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%);
    color: white;
}
[data-testid="stSidebar"] .stMarkdown { color: white; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3 { color: white !important; }

/* Header */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.main-header h1 { margin: 0; font-weight: 700; }
.main-header p { margin: 0.5rem 0 0 0; opacity: 0.9; }

/* Stat Cards */
.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border-left: 5px solid #667eea;
    transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-3px); }
.stat-card.green { border-left-color: #10b981; }
.stat-card.orange { border-left-color: #f59e0b; }
.stat-card.red { border-left-color: #ef4444; }
.stat-card.purple { border-left-color: #8b5cf6; }

.stat-card h3 { font-size: 0.85rem; color: #6b7280; margin: 0; text-transform: uppercase; letter-spacing: 0.5px; }
.stat-card .value { font-size: 2rem; font-weight: 700; color: #111827; margin: 0.5rem 0; }
.stat-card .icon { font-size: 2rem; float: right; opacity: 0.3; }

/* Table Styling */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}

/* Login Box */
.login-box {
    max-width: 450px;
    margin: 5rem auto;
    padding: 3rem;
    background: white;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
}
.login-logo {
    text-align: center;
    font-size: 4rem;
    margin-bottom: 1rem;
}

/* Badge */
.badge {
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
}
.badge-success { background: #d1fae5; color: #065f46; }
.badge-warning { background: #fef3c7; color: #92400e; }
.badge-danger { background: #fee2e2; color: #991b1b; }
.badge-info { background: #dbeafe; color: #1e40af; }

/* Hide default Streamlit elements */
#MainMenu, header, footer { visibility: hidden; }
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
def show_toast(msg, type="success"):
    if type == "success":
        st.success(msg)
    elif type == "error":
        st.error(msg)
    elif type == "info":
        st.info(msg)

def format_rp(num):
    return f"Rp {int(num):,}".replace(",", ".")

def get_df(query):
    conn = db.get_connection()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# ============ LOGIN PAGE ============
def login_page():
    st.markdown("""
    <div class="login-box">
        <div class="login-logo">🏍️</div>
        <h2 style="text-align:center; color:#1e3a8a;">SIMOTOR</h2>
        <p style="text-align:center; color:#6b7280;">Sistem Rental Motor Asoka Terdistribusi</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            submitted = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submitted:
                user = db.verify_login(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
        
        st.info("""
        **Demo Login:**
        - Admin: `admin` / `admin123`
        - Petugas: `petugas1` / `petugas123`
        """)

# ============ DASHBOARD PAGE ============
def dashboard_page():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Dashboard</h1>
        <p>Ringkasan operasional rental motor hari ini</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    today = datetime.now().strftime('%Y-%m-%d')
    trx_hari_ini = get_df(f"SELECT COUNT(*) c FROM transaksi WHERE tgl_sewa='{today}'").iloc[0]['c']
    motor_tersedia = get_df("SELECT COUNT(*) c FROM motor WHERE status='tersedia'").iloc[0]['c']
    motor_disewa = get_df("SELECT COUNT(*) c FROM motor WHERE status='disewa'").iloc[0]['c']
    pendapatan = get_df("SELECT COALESCE(SUM(total_bayar),0) t FROM pengembalian").iloc[0]['t']
    total_pelanggan = get_df("SELECT COUNT(*) c FROM pelanggan").iloc[0]['c']
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="stat-card">
            <span class="icon">📋</span>
            <h3>Transaksi Hari Ini</h3>
            <div class="value">{trx_hari_ini}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card green">
            <span class="icon">✅</span>
            <h3>Motor Tersedia</h3>
            <div class="value">{motor_tersedia}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card orange">
            <span class="icon">🏍️</span>
            <h3>Motor Disewa</h3>
            <div class="value">{motor_disewa}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-card purple">
            <span class="icon">💰</span>
            <h3>Total Pendapatan</h3>
            <div class="value" style="font-size:1.3rem;">{format_rp(pendapatan)}</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class="stat-card red">
            <span class="icon">👥</span>
            <h3>Total Pelanggan</h3>
            <div class="value">{total_pelanggan}</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Transaksi 7 Hari Terakhir")
        df_trx = get_df("""
            SELECT tgl_sewa, COUNT(*) as jumlah 
            FROM transaksi 
            WHERE tgl_sewa >= date('now', '-7 days')
            GROUP BY tgl_sewa ORDER BY tgl_sewa
        """)
        fig = px.line(df_trx, x='tgl_sewa', y='jumlah', markers=True,
                      labels={'tgl_sewa':'Tanggal','jumlah':'Jumlah Transaksi'})
        fig.update_traces(line=dict(color='#667eea', width=3))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏍️ Status Motor")
        df_status = get_df("SELECT status, COUNT(*) as jumlah FROM motor GROUP BY status")
        colors = {'tersedia':'#10b981','disewa':'#f59e0b','rusak':'#ef4444','servis':'#6b7280'}
        fig = px.pie(df_status, values='jumlah', names='status',
                     color='status', color_discrete_map=colors, hole=0.5)
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    # Pendapatan 30 hari
    st.subheader("💵 Pendapatan 30 Hari Terakhir")
    df_pendapatan = get_df("""
        SELECT tgl_kembali as tanggal, SUM(total_bayar) as pendapatan
        FROM pengembalian
        WHERE tgl_kembali >= date('now', '-30 days')
        GROUP BY tgl_kembali ORDER BY tgl_kembali
    """)
    fig = px.area(df_pendapatan, x='tanggal', y='pendapatan',
                  labels={'tanggal':'Tanggal','pendapatan':'Pendapatan (Rp)'})
    fig.update_traces(fillcolor='rgba(102,126,234,0.3)', line=dict(color='#667eea', width=2))
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    # Transaksi terbaru
    st.subheader("📝 Transaksi Terbaru")
    df_recent = get_df("""
        SELECT t.id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.pelanggan_id = p.id
        JOIN motor m ON t.motor_id = m.id
        ORDER BY t.tgl_sewa DESC LIMIT 10
    """)
    df_recent['total_biaya'] = df_recent['total_biaya'].apply(format_rp)
    st.dataframe(df_recent, use_container_width=True, hide_index=True)

# ============ MOTOR PAGE ============
def motor_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏍️ Manajemen Motor</h1>
        <p>Kelola data armada motor rental</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Cari motor (nopol/merek)")
    with col2:
        filter_status = st.selectbox("Filter Status", ["semua","tersedia","disewa","rusak","servis"])
    
    query = "SELECT * FROM motor WHERE 1=1"
    if search:
        query += f" AND (nopol LIKE '%{search}%' OR merek LIKE '%{search}%')"
    if filter_status != "semua":
        query += f" AND status = '{filter_status}'"
    
    df = get_df(query)
    
    if st.button("➕ Tambah Motor Baru"):
        st.session_state.show_motor_form = True
    
    if st.session_state.get('show_motor_form'):
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
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.form_submit_button("💾 Simpan", use_container_width=True):
                    if nopol and merek:
                        conn = db.get_connection()
                        try:
                            conn.execute("INSERT INTO motor (nopol,merek,jenis,tarif_jam,tarif_hari,status,cabang) VALUES (?,?,?,?,?,?,?)",
                                        (nopol, merek, jenis, tarif_jam, tarif_hari, status, 'Cabang Asoka'))
                            conn.commit()
                            st.success("✅ Motor berhasil ditambahkan!")
                            st.session_state.show_motor_form = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                        finally:
                            conn.close()
            with col_b:
                if st.form_submit_button("❌ Batal", use_container_width=True):
                    st.session_state.show_motor_form = False
                    st.rerun()
    
    # Display table with status badge
    if not df.empty:
        df_display = df.copy()
        df_display['total_biaya_display'] = df_display['tarif_hari'].apply(format_rp)
        st.dataframe(
            df_display[['nopol','merek','jenis','tarif_jam','tarif_hari','status']],
            use_container_width=True, hide_index=True
        )
        
        # Edit/Delete
        st.markdown("### ✏️ Edit / Hapus Motor")
        selected = st.selectbox("Pilih Motor", df['nopol'].tolist())
        if selected:
            motor = df[df['nopol']==selected].iloc[0]
            c1, c2, c3 = st.columns(3)
            with c1:
                new_status = st.selectbox("Ubah Status", 
                    ["tersedia","disewa","rusak","servis"],
                    index=["tersedia","disewa","rusak","servis"].index(motor['status']))
                if st.button("💾 Update Status"):
                    conn = db.get_connection()
                    conn.execute("UPDATE motor SET status=? WHERE id=?", (new_status, motor['id']))
                    conn.commit()
                    conn.close()
                    st.success("Status updated!")
                    st.rerun()
            with c2:
                if st.button("🗑️ Hapus Motor"):
                    conn = db.get_connection()
                    conn.execute("DELETE FROM motor WHERE id=?", (motor['id'],))
                    conn.commit()
                    conn.close()
                    st.success("Motor dihapus!")
                    st.rerun()
    else:
        st.info("Tidak ada data motor yang cocok.")

# ============ PELANGGAN PAGE ============
def pelanggan_page():
    st.markdown("""
    <div class="main-header">
        <h1>👥 Manajemen Pelanggan</h1>
        <p>Kelola data pelanggan rental</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📋 Daftar Pelanggan", "➕ Tambah Pelanggan"])
    
    with tab1:
        search = st.text_input("🔍 Cari pelanggan")
        query = "SELECT * FROM pelanggan"
        if search:
            query += f" WHERE nama LIKE '%{search}%' OR ktp LIKE '%{search}%'"
        df = get_df(query)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data pelanggan")
    
    with tab2:
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

# ============ TRANSAKSI PAGE ============
def transaksi_page():
    st.markdown("""
    <div class="main-header">
        <h1>🧾 Transaksi Penyewaan</h1>
        <p>Buat transaksi sewa motor baru</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["➕ Sewa Baru", "🔄 Pengembalian", "📋 Riwayat"])
    
    with tab1:
        pel_list = get_df("SELECT id, nama, ktp FROM pelanggan")
        motor_list = get_df("SELECT id, nopol, merek, tarif_jam, tarif_hari FROM motor WHERE status='tersedia'")
        
        if pel_list.empty or motor_list.empty:
            st.warning("Data pelanggan atau motor tersedia kosong!")
            return
        
        with st.form("trx_form"):
            c1, c2 = st.columns(2)
            with c1:
                pel_id = st.selectbox("Pilih Pelanggan", 
                    pel_list['nama'] + ' (' + pel_list['ktp'] + ')')
                pel_id = pel_list.iloc[[i for i,x in enumerate(pel_list['nama'] + ' (' + pel_list['ktp'] + ')') if x==pel_id][0]]['id']
                
                motor_sel = st.selectbox("Pilih Motor", 
                    motor_list['nopol'] + ' - ' + motor_list['merek'])
                motor_id = motor_list.iloc[[i for i,x in enumerate(motor_list['nopol'] + ' - ' + motor_list['merek']) if x==motor_sel][0]]
            with c2:
                durasi = st.number_input("Durasi", min_value=1, value=1)
                satuan = st.selectbox("Satuan", ["hari","jam"])
                
                tarif = motor_id['tarif_hari'] if satuan == 'hari' else motor_id['tarif_jam']
                total = tarif * durasi
                st.metric("💰 Total Biaya", format_rp(total))
            
            if st.form_submit_button("✅ Simpan Transaksi"):
                conn = db.get_connection()
                conn.execute("""INSERT INTO transaksi (pelanggan_id,motor_id,tgl_sewa,durasi,satuan,total_biaya,status,cabang) 
                               VALUES (?,?,?,?,?,?,?,?)""",
                            (pel_id, motor_id['id'], datetime.now().strftime('%Y-%m-%d'), 
                             durasi, satuan, total, 'aktif', 'Cabang Asoka'))
                conn.execute("UPDATE motor SET status='disewa' WHERE id=?", (motor_id['id'],))
                conn.commit()
                conn.close()
                st.success("✅ Transaksi berhasil disimpan!")
                
                # Struk
                st.markdown(f"""
                <div style="background:#f9fafb; padding:20px; border-radius:10px; margin-top:20px; border:2px dashed #667eea;">
                    <h3 style="text-align:center;">🧾 STRUK SEWA MOTOR</h3>
                    <hr>
                    <p><b>Tanggal:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
                    <p><b>Motor:</b> {motor_sel}</p>
                    <p><b>Durasi:</b> {durasi} {satuan}</p>
                    <p><b>Total:</b> {format_rp(total)}</p>
                    <p style="text-align:center; margin-top:20px;"><i>Terima kasih telah menggunakan layanan kami!</i></p>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()
    
    with tab2:
        trx_aktif = get_df("""
            SELECT t.id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id = p.id
            JOIN motor m ON t.motor_id = m.id
            WHERE t.status = 'aktif'
        """)
        if trx_aktif.empty:
            st.info("Tidak ada transaksi aktif")
        else:
            st.dataframe(trx_aktif, use_container_width=True, hide_index=True)
            selected = st.selectbox("Pilih Transaksi untuk Dikembalikan", trx_aktif['id'].tolist())
            tgl_kembali = st.date_input("Tanggal Kembali", datetime.now())
            
            if st.button("🔄 Proses Pengembalian"):
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
                conn.execute("UPDATE transaksi SET status='selesai' WHERE id=?", (selected,))
                conn.execute("UPDATE motor SET status='tersedia' WHERE id=?", (trx['merek'],))
                conn.execute("INSERT INTO pengembalian (transaksi_id,tgl_kembali,denda,total_bayar) VALUES (?,?,?,?)",
                            (selected, tgl_kembali.strftime('%Y-%m-%d'), denda, total_bayar))
                conn.commit()
                conn.close()
                
                st.success(f"✅ Pengembalian berhasil! Denda: {format_rp(denda)} | Total: {format_rp(total_bayar)}")
                st.rerun()
    
    with tab3:
        df = get_df("""
            SELECT t.id, p.nama, m.nopol, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
            FROM transaksi t
            JOIN pelanggan p ON t.pelanggan_id = p.id
            JOIN motor m ON t.motor_id = m.id
            ORDER BY t.tgl_sewa DESC
        """)
        df['total_biaya'] = df['total_biaya'].apply(format_rp)
        st.dataframe(df, use_container_width=True, hide_index=True)

# ============ LAPORAN PAGE ============
def laporan_page():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Laporan Cabang</h1>
        <p>Laporan transaksi dan pendapatan</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        periode = st.selectbox("Periode", ["Harian","Mingguan","Bulanan"])
    with c2:
        tanggal = st.date_input("Tanggal", datetime.now())
    with c3:
        st.write("")
        st.write("")
        export = st.button("📥 Export Excel")
    
    # Query berdasarkan periode
    if periode == "Harian":
        filter_date = f"DATE(tgl_sewa) = '{tanggal}'"
    elif periode == "Mingguan":
        start = (tanggal - timedelta(days=7)).strftime('%Y-%m-%d')
        filter_date = f"tgl_sewa BETWEEN '{start}' AND '{tanggal}'"
    else:
        start = tanggal.replace(day=1).strftime('%Y-%m-%d')
        filter_date = f"tgl_sewa BETWEEN '{start}' AND '{tanggal}'"
    
    df = get_df(f"""
        SELECT t.id, p.nama, m.nopol, m.merek, t.tgl_sewa, t.durasi, t.satuan, t.total_biaya, t.status
        FROM transaksi t
        JOIN pelanggan p ON t.pelanggan_id = p.id
        JOIN motor m ON t.motor_id = m.id
        WHERE {filter_date}
        ORDER BY t.tgl_sewa DESC
    """)
    
    # Summary
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Transaksi", len(df))
    with c2: st.metric("Total Pendapatan", format_rp(df['total_biaya'].sum()))
    with c3: st.metric("Rata-rata/Transaksi", format_rp(df['total_biaya'].mean() if len(df)>0 else 0))
    with c4: st.metric("Motor Tersewa", df['motor_id'].nunique() if 'motor_id' in df.columns else 0)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    if export and not df.empty:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Laporan')
        st.download_button("⬇️ Download Excel", buffer.getvalue(),
                          f"laporan_{periode.lower()}_{tanggal}.xlsx",
                          "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# ============ ADMIN PAGE ============
def admin_page():
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Dashboard Admin Pusat</h1>
        <p>Monitoring seluruh cabang rental motor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Nasional
    total_cabang = 1  # Simplified
    total_trx = get_df("SELECT COUNT(*) c FROM transaksi").iloc[0]['c']
    total_pelanggan = get_df("SELECT COUNT(*) c FROM pelanggan").iloc[0]['c']
    total_pendapatan = get_df("SELECT COALESCE(SUM(total_bayar),0) t FROM pengembalian").iloc[0]['t']
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-card">
            <h3>Total Cabang</h3><div class="value">{total_cabang}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card green">
            <h3>Total Transaksi</h3><div class="value">{total_trx}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card orange">
            <h3>Total Pelanggan</h3><div class="value">{total_pelanggan}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-card purple">
            <h3>Total Pendapatan</h3><div class="value" style="font-size:1.2rem;">{format_rp(total_pendapatan)}</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Tren Transaksi Bulanan")
        df_monthly = get_df("""
            SELECT strftime('%Y-%m', tgl_sewa) as bulan, COUNT(*) as jumlah
            FROM transaksi GROUP BY bulan ORDER BY bulan
        """)
        fig = px.bar(df_monthly, x='bulan', y='jumlah')
        fig.update_traces(marker_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏍️ Motor Terpopuler")
        df_pop = get_df("""
            SELECT m.merek, COUNT(*) as jumlah 
            FROM transaksi t JOIN motor m ON t.motor_id = m.id
            GROUP BY m.merek ORDER BY jumlah DESC LIMIT 5
        """)
        fig = px.bar(df_pop, x='jumlah', y='merek', orientation='h')
        fig.update_traces(marker_color='#10b981')
        st.plotly_chart(fig, use_container_width=True)
    
    # Monitoring Sync
    st.subheader("🔄 Status Sinkronisasi Cabang")
    sync_data = pd.DataFrame({
        'Cabang': ['Cabang Asoka', 'Cabang Pusat'],
        'Status': ['🟢 Online', '🟢 Online'],
        'Last Sync': [datetime.now().strftime('%Y-%m-%d %H:%M'), 
                      (datetime.now() - timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')],
        'Data Pending': [0, 2]
    })
    st.dataframe(sync_data, use_container_width=True, hide_index=True)

# ============ MAIN APP ============
def main():
    if not st.session_state.logged_in:
        login_page()
        return
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center; padding:1rem 0;">
            <div style="font-size:3rem;">🏍️</div>
            <h2 style="color:white; margin:0;">SIMOTOR</h2>
            <p style="color:#cbd5e1; font-size:0.85rem;">Rental Motor Asoka</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"👤 **{st.session_state.user['username']}**")
        st.markdown(f"🏷️ Role: `{st.session_state.user['role']}`")
        st.markdown(f"🏢 Cabang: `{st.session_state.user['cabang']}`")
        st.markdown("---")
        
        if st.session_state.user['role'] == 'admin':
            menu = st.radio(
                "📋 Menu",
                ["📊 Dashboard", "🏍️ Motor", "👥 Pelanggan",
                "🧾 Transaksi", "📈 Laporan", "🏢 Admin Pusat"],
                label_visibility="collapsed"
            )
        else:
            menu = st.radio(
                "📋 Menu",
                ["📊 Dashboard", "🏍️ Motor", "👥 Pelanggan",
                "🧾 Transaksi", "📈 Laporan"],
                label_visibility="collapsed"
            )   
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
        
        st.markdown("""
        <div style="position:fixed; bottom:20px; left:20px; color:#cbd5e1; font-size:0.75rem;">
            SIMOTOR v1.0<br>© 2024 Asoka Rental
        </div>
        """, unsafe_allow_html=True)
    
    # Route pages
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