import sqlite3
import bcrypt
from datetime import datetime, timedelta
import random

DB_NAME = "simotor.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE, password TEXT, role TEXT, cabang TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS motor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nopol TEXT UNIQUE, merek TEXT, jenis TEXT,
        tarif_jam REAL, tarif_hari REAL, status TEXT, cabang TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS pelanggan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT, ktp TEXT UNIQUE, alamat TEXT, telepon TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transaksi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pelanggan_id INTEGER, motor_id INTEGER,
        tgl_sewa TEXT, durasi INTEGER, satuan TEXT,
        total_biaya REAL, status TEXT, cabang TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS pengembalian (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaksi_id INTEGER, tgl_kembali TEXT,
        denda REAL, total_bayar REAL
    )''')
    
    # Seed data jika kosong
    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        seed_data(c)
    
    conn.commit()
    conn.close()

def seed_data(c):
    # Users (password: admin123 & petugas123)
    c.execute("INSERT INTO users VALUES (1,'admin',?,'admin','Pusat')",
              (bcrypt.hashpw(b'admin123', bcrypt.gensalt()),))
    c.execute("INSERT INTO users VALUES (2,'petugas1',?,'petugas','Cabang Asoka')",
              (bcrypt.hashpw(b'petugas123', bcrypt.gensalt()),))
    
    # Motor
    motors = [
        ('AB 1234 CD', 'Honda Vario', 'Matic', 10000, 80000, 'tersedia', 'Cabang Asoka'),
        ('AB 5678 EF', 'Yamaha NMAX', 'Matic', 15000, 120000, 'tersedia', 'Cabang Asoka'),
        ('AB 9012 GH', 'Honda Beat', 'Matic', 8000, 65000, 'disewa', 'Cabang Asoka'),
        ('AB 3456 IJ', 'Yamaha Mio', 'Matic', 8000, 65000, 'tersedia', 'Cabang Asoka'),
        ('AB 7890 KL', 'Honda PCX', 'Matic', 18000, 150000, 'servis', 'Cabang Asoka'),
        ('AB 2345 MN', 'Suzuki Address', 'Matic', 9000, 70000, 'tersedia', 'Cabang Asoka'),
        ('AB 6789 OP', 'Honda Scoopy', 'Matic', 10000, 80000, 'disewa', 'Cabang Asoka'),
        ('AB 1357 QR', 'Yamaha Lexi', 'Matic', 12000, 95000, 'tersedia', 'Cabang Asoka'),
    ]
    c.executemany("INSERT INTO motor (nopol,merek,jenis,tarif_jam,tarif_hari,status,cabang) VALUES (?,?,?,?,?,?,?)", motors)
    
    # Pelanggan
    pelanggan = [
        ('Budi Santoso', '3201012345670001', 'Jl. Merdeka 1', '081234567890'),
        ('Siti Aminah', '3201012345670002', 'Jl. Sudirman 5', '081234567891'),
        ('Ahmad Rizki', '3201012345670003', 'Jl. Diponegoro 10', '081234567892'),
        ('Dewi Lestari', '3201012345670004', 'Jl. Gatot Subroto 7', '081234567893'),
    ]
    c.executemany("INSERT INTO pelanggan (nama,ktp,alamat,telepon) VALUES (?,?,?,?)", pelanggan)
    
    # Transaksi (data 30 hari terakhir)
    today = datetime.now()
    trx_data = []
    trx_id = 1
    for i in range(30):
        date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
        n_trx = random.randint(2, 6)
        for _ in range(n_trx):
            pel_id = random.randint(1, 4)
            motor_id = random.randint(1, 8)
            durasi = random.choice([1, 2, 3, 24])
            satuan = 'hari' if durasi < 24 else 'jam'
            tarif = 80000 if satuan == 'hari' else 10000
            total = tarif * (durasi if satuan == 'hari' else durasi)
            status = 'selesai' if i > 0 else random.choice(['aktif', 'selesai'])
            trx_data.append((trx_id, pel_id, motor_id, date, durasi, satuan, total, status, 'Cabang Asoka'))
            trx_id += 1
    
    c.executemany("INSERT INTO transaksi VALUES (?,?,?,?,?,?,?,?,?)", trx_data)
    
    # Pengembalian
    for t in trx_data:
        if t[7] == 'selesai':
            denda = random.choice([0, 0, 0, 10000, 20000])
            c.execute("INSERT INTO pengembalian (transaksi_id,tgl_kembali,denda,total_bayar) VALUES (?,?,?,?)",
                      (t[0], t[3], denda, t[6] + denda))

def verify_login(username, password):
    conn = get_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()
    conn.close()

    if user:
        stored_password = user['password']

        if isinstance(stored_password, str):
            stored_password = stored_password.encode()

        if bcrypt.checkpw(password.encode(), stored_password):
            return dict(user)

    return None