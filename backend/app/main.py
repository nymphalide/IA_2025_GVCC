from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.router import router as api_router
from app.db import database


app = FastAPI(
    title="SmarTest AI Project",
    description="API pentru generarea și evaluarea problemelor de IA",
    version="1.0.0"
)


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
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
        db.execute(text("SELECT 1"))
        db.close()
        print("INFO: Conexiunea la DB a fost stabilită.")
    except Exception as e:
        print(f"EROARE: Nu s-a putut conecta la DB: {e}")


app.include_router(
    api_router,
    prefix="/api"
)


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "SmarTest API este gata. Vizitează /docs pentru documentație."
    }
