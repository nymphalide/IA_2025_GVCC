from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import generation, evaluation
from app.db import database
from sqlalchemy import text # <--- 1. ADaugă ACEST IMPORT
from fastapi.middleware.cors import CORSMiddleware

# Crearea instanței aplicației FastAPI
app = FastAPI(
    title="SmarTest AI Project",
    description="API pentru generarea și evaluarea problemelor de IA (L6 - MinMax)",
    version="0.1.0"
)

origins = [
    "http://localhost:3000",  # frontend React
    "http://127.0.0.1:3000",  # fallback pentru macOS / alte setup-uri
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # cine are voie să facă request-uri
    allow_credentials=True,
    allow_methods=["*"],             # GET, POST, etc.
    allow_headers=["*"],             # toate headerele
)

# Configurare CORS
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@app.on_event("startup")
async def startup_event():
    try:
        database.Base.metadata.create_all(bind=database.engine)
        db = database.SessionLocal()
        # db.execute("SELECT 1") # <-- Linia veche
        db.execute(text("SELECT 1")) # <--- 2. MODIFICĂ LINIA ACEASTA
        db.close()
        print("INFO:     Conexiunea la baza de date PostgreSQL a fost stabilită cu succes.")
    except Exception as e:
        print(f"EROARE:   Nu s-a putut stabili conexiunea la baza de date: {e}")


# Includem routerele definite în /api
app.include_router(generation.router, prefix="/api", tags=["1. Generation (L6)"])
app.include_router(evaluation.router, prefix="/api", tags=["2. Evaluation (L6)"])

# Un endpoint simplu pentru a verifica dacă API-ul funcționează
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bun venit la SmarTest API. Accesați /docs pentru documentația API."}