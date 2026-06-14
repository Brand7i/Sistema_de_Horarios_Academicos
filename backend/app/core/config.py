from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Sistema de Horarios Academicos"
    app_version: str = "0.1.0"
    population_size: int = 40
    generations: int = 120
    mutation_rate: float = 0.12
    elite_size: int = 6


settings = Settings()
