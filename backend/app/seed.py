from app.database import Base, engine, SessionLocal
from app.models import Docente, Materia, Aula, Grupo

Base.metadata.create_all(bind=engine)

db = SessionLocal()

if db.query(Docente).count() == 0:
    docentes = [
        Docente(nombre="Ing. Carlos Pérez", correo="carlos@umss.edu", especialidad="Programación", disponibilidad="Lunes Martes Miércoles Jueves"),
        Docente(nombre="Ing. Ana Rojas", correo="ana@umss.edu", especialidad="Base de Datos", disponibilidad="Lunes Miércoles Viernes"),
        Docente(nombre="Ing. Marco López", correo="marco@umss.edu", especialidad="Sistemas Operativos", disponibilidad="Martes Jueves Viernes"),
        Docente(nombre="Ing. Laura Vargas", correo="laura@umss.edu", especialidad="Redes", disponibilidad="Lunes Martes Viernes"),
    ]
    db.add_all(docentes)

if db.query(Materia).count() == 0:
    materias = [
        Materia(nombre="Programación I", sigla="INF-111", semestre=1, horas_semana=4, tipo="Laboratorio"),
        Materia(nombre="Cálculo I", sigla="MAT-101", semestre=1, horas_semana=4, tipo="Teórica"),
        Materia(nombre="Base de Datos I", sigla="INF-221", semestre=3, horas_semana=4, tipo="Laboratorio"),
        Materia(nombre="Sistemas Operativos", sigla="INF-331", semestre=5, horas_semana=4, tipo="Laboratorio"),
        Materia(nombre="Redes de Computadoras", sigla="INF-342", semestre=6, horas_semana=4, tipo="Laboratorio"),
    ]
    db.add_all(materias)

if db.query(Aula).count() == 0:
    aulas = [
        Aula(nombre="Aula 201", capacidad=60, tipo="Teórica"),
        Aula(nombre="Aula 202", capacidad=45, tipo="Teórica"),
        Aula(nombre="Lab 1", capacidad=35, tipo="Laboratorio"),
        Aula(nombre="Lab 2", capacidad=30, tipo="Laboratorio"),
    ]
    db.add_all(aulas)

if db.query(Grupo).count() == 0:
    grupos = [
        Grupo(nombre="1A", semestre=1, cantidad_estudiantes=45),
        Grupo(nombre="1B", semestre=1, cantidad_estudiantes=40),
        Grupo(nombre="3A", semestre=3, cantidad_estudiantes=35),
        Grupo(nombre="5A", semestre=5, cantidad_estudiantes=30),
        Grupo(nombre="6A", semestre=6, cantidad_estudiantes=30),
    ]
    db.add_all(grupos)

db.commit()
db.close()

print("Datos iniciales cargados correctamente.")
