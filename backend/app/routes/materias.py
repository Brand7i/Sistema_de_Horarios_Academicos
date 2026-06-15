from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/materias", tags=["Materias"])

@router.get("/", response_model=list[schemas.MateriaResponse])
def listar_materias(db: Session = Depends(get_db)):
    return db.query(models.Materia).all()

@router.post("/", response_model=schemas.MateriaResponse)
def crear_materia(materia: schemas.MateriaCreate, db: Session = Depends(get_db)):
    nueva = models.Materia(**materia.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.delete("/{materia_id}")
def eliminar_materia(materia_id: int, db: Session = Depends(get_db)):
    materia = db.query(models.Materia).filter(models.Materia.id == materia_id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    db.delete(materia)
    db.commit()
    return {"mensaje": "Materia eliminada"}
