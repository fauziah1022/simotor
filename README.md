# 🏍️ SIMOTOR - Sistem Rental Motor Asoka

Dashboard rental motor modern dengan Python + Streamlit.

## 🚀 Fitur
- ✅ Login dengan Role-Based Access (Admin/Petugas)
- ✅ Dashboard statistik real-time dengan grafik interaktif
- ✅ Manajemen Motor (CRUD + filter status)
- ✅ Manajemen Pelanggan (validasi KTP unik)
- ✅ Transaksi Penyewaan dengan auto-hitung
- ✅ Pengembalian dengan auto-hitung denda
- ✅ Laporan dengan Export Excel
- ✅ Dashboard Admin Pusat
- ✅ UI Modern dengan custom CSS
- ✅ Responsive design

## 📦 Instalasi Lokal

```bash
# Clone atau download project
cd simotor-streamlit

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py