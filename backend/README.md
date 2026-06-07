# GameLog - Backend (FastAPI)

REST API GameLog dibangun dengan **FastAPI + SQLAlchemy + SQLite + JWT Auth**.

## Struktur Folder

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py       # Settings & env vars
│   │   ├── deps.py         # Auth dependency (get_current_user)
│   │   └── security.py     # JWT & password hashing
│   ├── models/
│   │   ├── database.py     # SQLAlchemy engine + session
│   │   └── models.py       # ORM models: User, Game
│   ├── routers/
│   │   ├── auth.py         # POST /auth/register, /auth/login
│   │   └── games.py        # CRUD /games/ + /games/stats/summary
│   └── schemas/
│       └── schemas.py      # Pydantic v2 schemas
├── .env.example
├── .gitignore
├── main.py                 # FastAPI app entry point
└── requirements.txt
```

## Setup & Jalankan

```bash
# 1. Clone & masuk folder
cd backend

# 2. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt
pip install pydantic-settings    # tambahan untuk Settings

# 4. Salin .env
cp .env.example .env
# Edit SECRET_KEY dengan nilai acak (opsional untuk dev)

# 5. Jalankan server
uvicorn main:app --reload --port 8000
```

Server berjalan di: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

## Endpoint Utama

| Method | Path | Auth | Keterangan |
|--------|------|------|------------|
| POST | `/auth/register` | ✗ | Daftar akun baru |
| POST | `/auth/login` | ✗ | Login, dapat JWT token |
| GET | `/games/` | ✓ | List game (bisa filter: q, platform, status) |
| GET | `/games/{id}` | ✓ | Detail satu game |
| POST | `/games/` | ✓ | Tambah game baru |
| PUT | `/games/{id}` | ✓ | Update game |
| DELETE | `/games/{id}` | ✓ | Hapus game |
| GET | `/games/stats/summary` | ✓ | Statistik koleksi |

## Autentikasi

Menggunakan JWT Bearer token. Setelah login, sertakan header:
```
Authorization: Bearer <token>
```