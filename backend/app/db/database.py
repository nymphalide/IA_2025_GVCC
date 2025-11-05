import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Citim URL-ul bazei de date din variabilele de mediu (setat în docker-compose.yml)
# Format: "postgresql://user:password@host:port/dbname"
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://admin:admin@localhost:5432/smartest")

# Creăm motorul SQLAlchemy
# 'pool_pre_ping=True' verifică conexiunile înainte de a le utiliza
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Creăm o sesiune locală (fabrică de sesiuni)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clasa de bază pentru modelele ORM
Base = declarative_base()

# Funcție utilitară pentru a obține o sesiune de DB (dependency injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()