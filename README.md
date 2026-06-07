# GameLog - FastAPI + Streamlit

Aplikasi pencatatan koleksi game pribadi, GameLog dibangun menggunakan **FastAPI** (backend) dan **Streamlit** (frontend).

## Struktur Proyek

```
final-project-fastapi-kripik-tempe/
├── backend/
└── frontend/
```

## Cara Menjalankan (Development)

Buka **dua terminal** secara bersamaan:

```bash
# Terminal 1 — Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt pydantic-settings
uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

| Service | URL |
|---------|-----|
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| Frontend App | http://localhost:8501 |

## Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Backend API | FastAPI 0.115 |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Validasi | Pydantic v2 |
| ORM | SQLAlchemy 2.x |
| Database | SQLite |
| Server | Uvicorn |
| Frontend | Streamlit 1.36 |
| HTTP Client | httpx |
| Visualisasi | Plotly |
