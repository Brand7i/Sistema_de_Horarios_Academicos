from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, run_startup_migrations
from app.routes import docentes, materias, aulas, grupos, horarios

Base.metadata.create_all(bind=engine)
run_startup_migrations()

app = FastAPI(
    title="Sistema de Horarios Académicos Automáticos",
    description="Backend para generar horarios usando Algoritmos Genéticos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docentes.router)
app.include_router(materias.router)
app.include_router(aulas.router)
app.include_router(grupos.router)
app.include_router(horarios.router)

@app.get("/")
def inicio():
    return {
        "mensaje": "Sistema de Horarios Académicos Automáticos - UMSS",
        "docs": "/docs"
    }
