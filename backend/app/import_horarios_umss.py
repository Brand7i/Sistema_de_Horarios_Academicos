import json
from pathlib import Path

from app.database import Base, SessionLocal, engine
from app.models import Aula, Docente, Grupo, HorarioGenerado, Materia

Base.metadata.create_all(bind=engine)

DATA_PATH = Path(__file__).parent / "data" / "horarios_umss.json"

DIAS = {
    "LU": "Lunes",
    "MA": "Martes",
    "MI": "Miercoles",
    "JU": "Jueves",
    "VI": "Viernes",
    "SA": "Sabado",
}

NIVELES = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
}


def formatear_hora(valor):
    valor = str(valor).zfill(4)
    return f"{valor[:2]}:{valor[2:]}"


def detectar_tipo_aula(nombre_aula):
    nombre = nombre_aula.upper()
    if "LAB" in nombre or "INFLAB" in nombre:
        return "Laboratorio"
    return "Teorica"


def detectar_tipo_materia(nombre_materia):
    nombre = nombre_materia.upper()
    palabras_laboratorio = [
        "PROGRAMACION",
        "BASE DE DATOS",
        "TALLER",
        "GRAFICACION",
        "SISTEMAS OPERATIVOS",
    ]

    for palabra in palabras_laboratorio:
        if palabra in nombre:
            return "Laboratorio"

    return "Teorica"


def formatear_disponibilidad(slots):
    return " | ".join(sorted(slots))


def es_docente_tp(nombre_docente):
    nombre = (nombre_docente or "").strip().upper()
    return nombre.startswith("[P]") or nombre.startswith("[TP]")


def limpiar_nombre_docente(nombre_docente):
    nombre = (nombre_docente or "").strip()
    if nombre.upper().startswith("[P]"):
        return nombre[3:].strip()
    if nombre.upper().startswith("[TP]"):
        return nombre[4:].strip()
    return nombre


def es_fisica_general_con_practico(materia_codigo, grupo_codigo):
    return materia_codigo == "2006063" and grupo_codigo in {"B1", "B2", "B3", "B4", "B5", "B6"}


def construir_horarios_validos(materia_codigo, grupo_codigo, grupo_data):
    docente_grupo = (grupo_data.get("teacher") or "").strip()
    permitir_tp = es_fisica_general_con_practico(materia_codigo, grupo_codigo)

    if es_docente_tp(docente_grupo) and not permitir_tp:
        return []

    horarios_validos = []
    for item in grupo_data["schedule"]:
        if not item.get("isClass", False):
            continue
        if es_docente_tp(item.get("teacher")) and not permitir_tp:
            continue
        horarios_validos.append(item)

    return horarios_validos


def detectar_tipo_bloque(materia_codigo, grupo_codigo):
    if materia_codigo == "2006063":
        return "Teoria" if grupo_codigo == "B" else "Laboratorio"
    return "Clase"


def importar_horarios():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontro el archivo JSON en {DATA_PATH}")

    db = SessionLocal()

    with open(DATA_PATH, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)

    db.query(HorarioGenerado).delete()
    db.query(Grupo).delete()
    db.query(Aula).delete()
    db.query(Materia).delete()
    db.query(Docente).delete()
    db.commit()

    docentes_creados = {}
    docentes_info = {}
    materias_creadas = {}
    aulas_creadas = {}
    grupos_creados = {}

    for nivel in data["levels"]:
        nivel_codigo = nivel["code"]
        semestre = NIVELES.get(nivel_codigo, 1)

        for materia_data in nivel["subjects"]:
            materia_codigo = str(materia_data["code"])
            materia_nombre = materia_data["name"].strip()
            materia_tipo = detectar_tipo_materia(materia_nombre)

            horas_semana = 0
            for grupo_data in materia_data["groups"]:
                grupo_codigo = str(grupo_data["code"]).strip()
                horarios_validos = construir_horarios_validos(materia_codigo, grupo_codigo, grupo_data)
                total_grupo = sum(item["duration"] for item in horarios_validos)
                horas_semana = max(horas_semana, total_grupo)

            if materia_codigo not in materias_creadas:
                materia = Materia(
                    nombre=materia_nombre,
                    sigla=materia_codigo,
                    semestre=semestre,
                    horas_semana=horas_semana,
                    tipo=materia_tipo,
                )
                db.add(materia)
                db.flush()
                materias_creadas[materia_codigo] = materia

            materia = materias_creadas[materia_codigo]

            for grupo_data in materia_data["groups"]:
                grupo_codigo = str(grupo_data["code"]).strip()
                horarios_validos = construir_horarios_validos(materia_codigo, grupo_codigo, grupo_data)
                if not horarios_validos:
                    continue

                grupo_nombre = f"{nivel_codigo}-{materia_codigo}-G{grupo_codigo}"

                if grupo_nombre not in grupos_creados:
                    grupo = Grupo(
                        nombre=grupo_nombre,
                        semestre=semestre,
                        cantidad_estudiantes=40,
                    )
                    db.add(grupo)
                    db.flush()
                    grupos_creados[grupo_nombre] = grupo

                grupo = grupos_creados[grupo_nombre]
                tipo_bloque = detectar_tipo_bloque(materia_codigo, grupo_codigo)

                for horario in horarios_validos:
                    docente_nombre = limpiar_nombre_docente(horario["teacher"])
                    aula_nombre = horario["room"].strip()
                    dia = DIAS.get(horario["day"], horario["day"])
                    inicio = formatear_hora(horario["start"])
                    fin = formatear_hora(horario["end"])
                    slot = f"{dia} {inicio}-{fin}"

                    info = docentes_info.setdefault(docente_nombre, {
                        "especialidades": set(),
                        "slots": set(),
                    })
                    info["especialidades"].add(materia_nombre)
                    info["slots"].add(slot)

                    if docente_nombre not in docentes_creados:
                        docente = Docente(
                            nombre=docente_nombre,
                            correo="",
                            especialidad="",
                            disponibilidad="",
                        )
                        db.add(docente)
                        db.flush()
                        docentes_creados[docente_nombre] = docente

                    if aula_nombre not in aulas_creadas:
                        aula = Aula(
                            nombre=aula_nombre,
                            capacidad=40,
                            tipo=detectar_tipo_aula(aula_nombre),
                        )
                        db.add(aula)
                        db.flush()
                        aulas_creadas[aula_nombre] = aula

                    docente = docentes_creados[docente_nombre]
                    aula = aulas_creadas[aula_nombre]

                    horario_real = HorarioGenerado(
                        materia_id=materia.id,
                        docente_id=docente.id,
                        aula_id=aula.id,
                        grupo_id=grupo.id,
                        semestre=semestre,
                        dia=dia,
                        bloque=f"{inicio}-{fin}",
                        tipo=tipo_bloque,
                        origen="importado",
                        escenario="umss-importado",
                    )

                    db.add(horario_real)

    for docente_nombre, docente in docentes_creados.items():
        info = docentes_info[docente_nombre]
        docente.especialidad = " | ".join(sorted(info["especialidades"]))
        docente.disponibilidad = formatear_disponibilidad(info["slots"])

    db.commit()

    print("Horarios UMSS importados correctamente.")
    print(f"Docentes: {len(docentes_creados)}")
    print(f"Materias: {len(materias_creadas)}")
    print(f"Aulas: {len(aulas_creadas)}")
    print(f"Grupos: {len(grupos_creados)}")

    db.close()


if __name__ == "__main__":
    importar_horarios()
