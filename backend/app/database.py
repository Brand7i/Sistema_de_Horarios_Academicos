import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No se encontro DATABASE_URL en backend/.env")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass


def run_startup_migrations():
    inspector = inspect(engine)
    if "horarios_generados" not in inspector.get_table_names():
        return

    columnas = {columna["name"] for columna in inspector.get_columns("horarios_generados")}

    with engine.begin() as conn:
        if "origen" not in columnas:
            conn.execute(text("ALTER TABLE horarios_generados ADD COLUMN origen VARCHAR DEFAULT 'importado'"))
            conn.execute(text("UPDATE horarios_generados SET origen = 'importado' WHERE origen IS NULL"))

        if "escenario" not in columnas:
            conn.execute(text("ALTER TABLE horarios_generados ADD COLUMN escenario VARCHAR"))
            conn.execute(text("UPDATE horarios_generados SET escenario = 'umss-importado' WHERE escenario IS NULL"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
