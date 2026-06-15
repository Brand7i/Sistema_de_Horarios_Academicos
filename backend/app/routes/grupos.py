from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/grupos", tags=["Grupos"])

@router.get("/", response_model=list[schemas.GrupoResponse])
def listar_grupos(db: Session = Depends(get_db)):
    return db.query(models.Grupo).all()

@router.post("/", response_model=schemas.GrupoResponse)
def crear_grupo(grupo: schemas.GrupoCreate, db: Session = Depends(get_db)):
    nuevo = models.Grupo(**grupo.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.delete("/{grupo_id}")
def eliminar_grupo(grupo_id: int, db: Session = Depends(get_db)):
    grupo = db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    db.delete(grupo)
    db.commit()
    return {"mensaje": "Grupo eliminado"}
