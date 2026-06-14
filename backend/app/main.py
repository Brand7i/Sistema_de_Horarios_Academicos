from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.schedules import router as schedules_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Generador de horarios academicos con algoritmos geneticos.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(schedules_router, prefix="/api")
