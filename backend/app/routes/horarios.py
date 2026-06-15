from collections import defaultdict

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db
from app.genetic_algorithm.semestre_ag import generar_horario_semestre_ag

router = APIRouter(prefix="/horarios", tags=["Horarios"])

NIVELES = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "E",
    6: "F",
    7: "G",
    8: "H",
    9: "I",
}


def es_fisica_general(materia: models.Materia) -> bool:
    return materia.sigla == "2006063"


def serializar_horario(horario: models.HorarioGenerado) -> schemas.HorarioResponse:
    return schemas.HorarioResponse(
        id=horario.id,
        materia_id=horario.materia_id,
        materia=horario.materia.nombre,
        sigla=horario.materia.sigla,
        docente_id=horario.docente_id,
        docente=horario.docente.nombre,
        aula_id=horario.aula_id,
        aula=horario.aula.nombre,
        grupo_id=horario.grupo_id,
        grupo=horario.grupo.nombre,
        semestre=horario.semestre,
        dia=horario.dia,
        bloque=horario.bloque,
        tipo=horario.tipo,
        origen=horario.origen,
        escenario=horario.escenario,
    )


def etiqueta_nivel(semestre: int) -> str:
    return NIVELES.get(semestre, str(semestre))


@router.get("/", response_model=list[schemas.HorarioResponse])
def listar_horario(
    origen: str = Query("importado"),
    semestre: int | None = Query(None),
    db: Session = Depends(get_db),
):
    consulta = db.query(models.HorarioGenerado).options(
        joinedload(models.HorarioGenerado.materia),
        joinedload(models.HorarioGenerado.docente),
        joinedload(models.HorarioGenerado.aula),
        joinedload(models.HorarioGenerado.grupo),
    ).filter(models.HorarioGenerado.origen == origen)

    if semestre is not None:
        consulta = consulta.filter(models.HorarioGenerado.semestre == semestre)

    horarios = consulta.order_by(
        models.HorarioGenerado.semestre,
        models.HorarioGenerado.dia,
        models.HorarioGenerado.bloque,
    ).all()
    return [serializar_horario(horario) for horario in horarios]


@router.delete("/")
def limpiar_horario(origen: str = Query("ag"), db: Session = Depends(get_db)):
    db.query(models.HorarioGenerado).filter(models.HorarioGenerado.origen == origen).delete()
    db.commit()
    return {"mensaje": f"Horarios {origen} eliminados"}


@router.get("/configuracion", response_model=schemas.HorarioConfiguracionResponse)
def configuracion_horario(semestre: int = Query(..., ge=1, le=9), db: Session = Depends(get_db)):
    materias = (
        db.query(models.Materia)
        .filter(models.Materia.semestre == semestre)
        .order_by(models.Materia.nombre)
        .all()
    )
    if not materias:
        raise HTTPException(status_code=404, detail=f"No hay materias para el semestre {semestre}")

    horarios_importados = (
        db.query(models.HorarioGenerado)
        .options(
            joinedload(models.HorarioGenerado.materia),
            joinedload(models.HorarioGenerado.docente),
            joinedload(models.HorarioGenerado.grupo),
        )
        .filter(
            models.HorarioGenerado.origen == "importado",
            models.HorarioGenerado.semestre == semestre,
        )
        .all()
    )

    docentes_por_materia = defaultdict(dict)
    for horario in horarios_importados:
        referencia = horario.grupo.nombre if horario.grupo else f"Nivel {etiqueta_nivel(semestre)}"
        docentes_por_materia[horario.materia_id][horario.docente_id] = schemas.DocenteOpcion(
            id=horario.docente_id,
            nombre=horario.docente.nombre,
            grupo_referencia=referencia,
        )

    materias_config = []
    for materia in materias:
        docentes = list(docentes_por_materia.get(materia.id, {}).values())

        materias_config.append(schemas.MateriaConfiguracion(
            materia_id=materia.id,
            nombre=materia.nombre,
            sigla=materia.sigla,
            tipo=materia.tipo,
            horas_semana=materia.horas_semana,
            docentes=docentes,
        ))

    return schemas.HorarioConfiguracionResponse(
        semestre=semestre,
        nivel=etiqueta_nivel(semestre),
        materias=materias_config,
    )


def construir_horarios_importados_semestre(db: Session, semestre: int, materias):
    materia_ids = [materia.id for materia in materias]
    if not materia_ids:
        return []

    horarios = (
        db.query(models.HorarioGenerado)
        .options(
            joinedload(models.HorarioGenerado.materia),
            joinedload(models.HorarioGenerado.docente),
            joinedload(models.HorarioGenerado.aula),
            joinedload(models.HorarioGenerado.grupo),
        )
        .filter(
            models.HorarioGenerado.origen == "importado",
            models.HorarioGenerado.semestre == semestre,
            models.HorarioGenerado.materia_id.in_(materia_ids),
        )
        .order_by(
            models.HorarioGenerado.materia_id,
            models.HorarioGenerado.grupo_id,
            models.HorarioGenerado.dia,
            models.HorarioGenerado.bloque,
        )
        .all()
    )

    importados = []
    for horario in horarios:
        importados.append({
            "materia_id": horario.materia_id,
            "docente_id": horario.docente_id,
            "dia": horario.dia,
            "bloque": horario.bloque,
            "aula_id": horario.aula_id,
            "grupo_id": horario.grupo_id,
            "grupo": horario.grupo.nombre,
            "tipo": horario.tipo,
        })
    return importados


def obtener_o_crear_grupo_semestre(db: Session, semestre: int):
    nivel = NIVELES.get(semestre, str(semestre))
    nombre = f"NIVEL-{nivel}"
    grupo = db.query(models.Grupo).filter(models.Grupo.nombre == nombre).first()
    if grupo:
        return grupo

    legado = db.query(models.Grupo).filter(models.Grupo.nombre == f"SEMESTRE-{semestre}").first()
    if legado:
        legado.nombre = nombre
        db.flush()
        return legado

    cantidad_estudiantes = (
        db.query(models.Grupo)
        .filter(models.Grupo.semestre == semestre)
        .order_by(models.Grupo.cantidad_estudiantes.desc())
        .first()
    )
    grupo = models.Grupo(
        nombre=nombre,
        semestre=semestre,
        cantidad_estudiantes=cantidad_estudiantes.cantidad_estudiantes if cantidad_estudiantes else 40,
    )
    db.add(grupo)
    db.flush()
    return grupo


@router.post("/generar")
def generar_horario(payload: schemas.HorarioGeneracionRequest = Body(...), db: Session = Depends(get_db)):
    semestre = payload.semestre
    materias = (
        db.query(models.Materia)
        .filter(models.Materia.semestre == semestre)
        .order_by(models.Materia.nombre)
        .all()
    )
    docentes = db.query(models.Docente).all()
    aulas = db.query(models.Aula).all()

    if not materias:
        raise HTTPException(status_code=400, detail=f"No hay materias registradas para el semestre {semestre}")
    if not docentes or not aulas:
        raise HTTPException(status_code=400, detail="Debe registrar docentes y aulas antes de generar")

    grupo = obtener_o_crear_grupo_semestre(db, semestre)
    total_clases_estimadas = sum(max(1, materia.horas_semana // 2) for materia in materias)
    docentes_por_id = {docente.id: docente for docente in docentes}
    docentes_fijos = {}

    for materia in materias:
        seleccion_docente = payload.docentes_por_materia.get(materia.id)
        if seleccion_docente is None:
            continue

        docente_ids = seleccion_docente if isinstance(seleccion_docente, list) else [seleccion_docente]
        docentes_materia = []

        for docente_id in docente_ids:
            docente = docentes_por_id.get(docente_id)
            if not docente:
                raise HTTPException(status_code=400, detail=f"Docente invalido para la materia {materia.nombre}")
            docentes_materia.append(docente)

        if docentes_materia:
            docentes_fijos[materia.id] = docentes_materia

    for materia in materias:
        if not es_fisica_general(materia):
            continue
        if materia.id in docentes_fijos:
            continue

        horarios_materia = (
            db.query(models.HorarioGenerado)
            .options(
                joinedload(models.HorarioGenerado.grupo),
                joinedload(models.HorarioGenerado.docente),
            )
            .filter(
                models.HorarioGenerado.origen == "importado",
                models.HorarioGenerado.semestre == semestre,
                models.HorarioGenerado.materia_id == materia.id,
            )
            .all()
        )

        teoria = None
        laboratorios = []
        for horario in horarios_materia:
            nombre_grupo = horario.grupo.nombre if horario.grupo else ""
            if nombre_grupo.endswith("-GB"):
                teoria = horario.docente
            elif "-GB" in nombre_grupo:
                laboratorios.append(horario.docente)

        docentes_unicos = []
        vistos = set()
        for docente in [teoria, *laboratorios]:
            if docente and docente.id not in vistos:
                vistos.add(docente.id)
                docentes_unicos.append(docente)

        if docentes_unicos:
            docentes_fijos[materia.id] = docentes_unicos

    horarios_importados = construir_horarios_importados_semestre(db, semestre, materias)

    resultado = generar_horario_semestre_ag(
        materias=materias,
        docentes=docentes,
        aulas=aulas,
        grupo=grupo,
        docentes_fijos=docentes_fijos,
        horarios_importados=horarios_importados,
        poblacion_size=80,
        generaciones=120,
        prob_mutacion=0.28,
        max_alternativas=25,
    )

    db.query(models.HorarioGenerado).filter(
        models.HorarioGenerado.origen == "ag",
        models.HorarioGenerado.semestre == semestre,
    ).delete()

    for gen in resultado["mejor_horario"]:
        db.add(models.HorarioGenerado(
            materia_id=gen["materia_id"],
            docente_id=gen["docente_id"],
            aula_id=gen["aula_id"],
            grupo_id=gen["grupo_id"],
            semestre=gen["semestre"],
            dia=gen["dia"],
            bloque=gen["bloque"],
            tipo=gen["tipo"],
            origen="ag",
            escenario=f"semestre-{semestre}",
        ))

    db.commit()

    return {
        "mensaje": f"Horario generado correctamente para el semestre {semestre}",
        "fitness": resultado["fitness"],
        "conflictos": resultado["conflictos"],
        "total_clases": len(resultado["mejor_horario"]),
        "parametros": {
            "semestre": semestre,
            "materias": len(materias),
            "clases_estimadas": total_clases_estimadas,
            "clases_base_importadas": len(horarios_importados),
            "poblacion_size": 80,
            "generaciones": 120,
            "prob_mutacion": 0.28,
            "alternativas": len(resultado["alternativas"]),
        },
        "horario": resultado["mejor_horario"],
        "alternativas": resultado["alternativas"],
    }
