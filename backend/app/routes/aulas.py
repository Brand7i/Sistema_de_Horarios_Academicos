from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/aulas", tags=["Aulas"])

@router.get("/", response_model=list[schemas.AulaResponse])
def listar_aulas(db: Session = Depends(get_db)):
    return db.query(models.Aula).all()

@router.post("/", response_model=schemas.AulaResponse)
def crear_aula(aula: schemas.AulaCreate, db: Session = Depends(get_db)):
    nueva = models.Aula(**aula.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.delete("/{aula_id}")
def eliminar_aula(aula_id: int, db: Session = Depends(get_db)):
    aula = db.query(models.Aula).filter(models.Aula.id == aula_id).first()
    if not aula:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    db.delete(aula)
    db.commit()
    return {"mensaje": "Aula eliminada"}
