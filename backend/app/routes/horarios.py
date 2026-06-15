from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.genetic_algorithm.algoritmo import generar_horario_ag

router = APIRouter(prefix="/horarios", tags=["Horarios"])

@router.get("/", response_model=list[schemas.HorarioResponse])
def listar_horario(db: Session = Depends(get_db)):
    return db.query(models.HorarioGenerado).order_by(
        models.HorarioGenerado.semestre,
        models.HorarioGenerado.dia,
        models.HorarioGenerado.bloque
    ).all()

@router.delete("/")
def limpiar_horario(db: Session = Depends(get_db)):
    db.query(models.HorarioGenerado).delete()
    db.commit()
    return {"mensaje": "Horario eliminado"}

@router.post("/generar")
def generar_horario(db: Session = Depends(get_db)):
    docentes = db.query(models.Docente).all()
    materias = db.query(models.Materia).all()
    aulas = db.query(models.Aula).all()
    grupos = db.query(models.Grupo).all()

    if not docentes or not materias or not aulas or not grupos:
        raise HTTPException(
            status_code=400,
            detail="Debe registrar docentes, materias, aulas y grupos antes de generar el horario"
        )

    resultado = generar_horario_ag(
        docentes=docentes,
        materias=materias,
        aulas=aulas,
        grupos=grupos,
        poblacion_size=80,
        generaciones=120,
        prob_mutacion=0.12
    )

    db.query(models.HorarioGenerado).delete()

    for gen in resultado["mejor_horario"]:
        nuevo = models.HorarioGenerado(
            materia=gen["materia"],
            sigla=gen["sigla"],
            docente=gen["docente"],
            aula=gen["aula"],
            grupo=gen["grupo"],
            semestre=gen["semestre"],
            dia=gen["dia"],
            bloque=gen["bloque"],
            tipo=gen["tipo"]
        )
        db.add(nuevo)

    db.commit()

    return {
        "mensaje": "Horario generado correctamente",
        "fitness": resultado["fitness"],
        "conflictos": resultado["conflictos"],
        "total_clases": len(resultado["mejor_horario"]),
        "horario": resultado["mejor_horario"]
    }
