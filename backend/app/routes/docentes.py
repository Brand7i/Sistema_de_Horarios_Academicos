from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/docentes", tags=["Docentes"])

@router.get("/", response_model=list[schemas.DocenteResponse])
def listar_docentes(db: Session = Depends(get_db)):
    return db.query(models.Docente).all()

@router.post("/", response_model=schemas.DocenteResponse)
def crear_docente(docente: schemas.DocenteCreate, db: Session = Depends(get_db)):
    nuevo = models.Docente(**docente.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.delete("/{docente_id}")
def eliminar_docente(docente_id: int, db: Session = Depends(get_db)):
    docente = db.query(models.Docente).filter(models.Docente.id == docente_id).first()
    if not docente:
        raise HTTPException(status_code=404, detail="Docente no encontrado")
    db.delete(docente)
    db.commit()
    return {"mensaje": "Docente eliminado"}
