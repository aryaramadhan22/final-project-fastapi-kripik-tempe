# GameLog - Frontend (Streamlit)

Interface GameLog dibangun dengan **Streamlit + httpx + Plotly**.

## Struktur Folder

```
frontend/
├── utils/
│   ├── api.py              # HTTP client ke FastAPI backend
│   └── styles.py           # CSS global + helper badge/chip
├── views/
│   ├── game_form.py        # Form tambah & edit game
│   ├── game_list.py        # Halaman daftar game + filter + hapus
│   └── statistics.py       # Halaman statistik + grafik Plotly
├── .gitignore
├── app.py                  # Entry point, auth guard & routing
└── requirements.txt
```

## Setup & Jalankan

```bash
# 1. Pastikan Backend sudah berjalan di port 8000

# 2. Masuk folder frontend
cd frontend

# 3. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Jalankan Streamlit
streamlit run app.py
```

App berjalan di: http://localhost:8501

## Fitur

- **Login / Register** - autentikasi dengan JWT token
- **Daftar Game** - grid card bergaya dark mode mirip desain Django asli
- **Filter** - pencarian judul, filter platform & status
- **Tambah Game** - form lengkap dengan validasi
- **Edit Game** - form pre-filled data game yang dipilih
- **Hapus Game** - konfirmasi sebelum hapus
- **Statistik** - donut chart platform, bar chart status, bar chart avg rating per genre

## Catatan

Jika backend ada di host lain, ubah `BASE_URL` di `utils/api.py`:
```python
BASE_URL = "http://<host-backend>:8000"
```
