from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Docente(Base):
    __tablename__ = "docentes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, nullable=True)
    especialidad = Column(String, nullable=False)
    disponibilidad = Column(String, nullable=False)
    horarios = relationship("HorarioGenerado", back_populates="docente")

class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    sigla = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    horas_semana = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    horarios = relationship("HorarioGenerado", back_populates="materia")

class Aula(Base):
    __tablename__ = "aulas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    horarios = relationship("HorarioGenerado", back_populates="aula")

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    semestre = Column(Integer, nullable=False)
    cantidad_estudiantes = Column(Integer, nullable=False)
    horarios = relationship("HorarioGenerado", back_populates="grupo")

class HorarioGenerado(Base):
    __tablename__ = "horarios_generados"

    id = Column(Integer, primary_key=True, index=True)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False, index=True)
    docente_id = Column(Integer, ForeignKey("docentes.id"), nullable=False, index=True)
    aula_id = Column(Integer, ForeignKey("aulas.id"), nullable=False, index=True)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), nullable=False, index=True)
    semestre = Column(Integer, nullable=False)
    dia = Column(String, nullable=False)
    bloque = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    origen = Column(String, nullable=False, default="importado")
    escenario = Column(String, nullable=True)

    materia = relationship("Materia", back_populates="horarios")
    docente = relationship("Docente", back_populates="horarios")
    aula = relationship("Aula", back_populates="horarios")
    grupo = relationship("Grupo", back_populates="horarios")
