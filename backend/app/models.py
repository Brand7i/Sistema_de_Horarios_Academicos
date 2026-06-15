from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=True)
    especialidad = Column(String, nullable=False)
    disponibilidad = Column(String, nullable=False)

class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    sigla = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    horas_semana = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)

class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    cantidad_estudiantes = Column(Integer, nullable=False)

class HorarioGenerado(Base):
    __tablename__ = "horarios_generados"

    id = Column(Integer, primary_key=True, index=True)
    materia = Column(String, nullable=False)
    sigla = Column(String, nullable=False)
    docente = Column(String, nullable=False)
    aula = Column(String, nullable=False)
    grupo = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    dia = Column(String, nullable=False)
    bloque = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
