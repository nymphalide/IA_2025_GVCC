from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api import generation, evaluation
from app.db import database

# --- NEW IMPORTS FOR STRATEGY MODULE ---
from app.api.strategy_generation import router as strategy_generation_router
from app.api.strategy_evaluation import router as strategy_evaluation_router


# =====================================================
#                FASTAPI INSTANCE
# =====================================================
app = FastAPI(
    title="SmarTest AI Project",
    description="API pentru generarea și evaluarea problemelor de IA",
    version="1.0.0"
)


# =====================================================
#                      CORS
# =====================================================
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


# =====================================================
#                   STARTUP EVENT
# =====================================================
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


# =====================================================
#                     ROUTERS
# =====================================================

# MinMax (existing)
app.include_router(
    generation.router,
    prefix="/api",
    tags=["MinMax - Generation"]
)

app.include_router(
    evaluation.router,
    prefix="/api",
    tags=["MinMax - Evaluation"]
)

# Strategy (NEW)
app.include_router(
    strategy_generation_router,
    prefix="/api",
    tags=["Strategy - Generation"]
)

app.include_router(
    strategy_evaluation_router,
    prefix="/api",
    tags=["Strategy - Evaluation"]
)


# =====================================================
#                     ROOT ENDPOINT
# =====================================================
@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "SmarTest API este gata. Vizitează /docs pentru documentație."
    }
