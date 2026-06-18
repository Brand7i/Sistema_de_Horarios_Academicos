import random
from copy import deepcopy


def aulas_para_materia(materia, aulas):
    if materia.tipo.lower() == "laboratorio":
        laboratorios = [aula for aula in aulas if aula.tipo.lower() == "laboratorio"]
        return laboratorios if laboratorios else aulas
    return aulas


def slots_disponibles_docente(disponibilidad):
    disponibilidad = (disponibilidad or "").strip()
    if not disponibilidad:
        return []
    if "|" not in disponibilidad and ":" not in disponibilidad:
        return []
    return [item.strip() for item in disponibilidad.split("|") if item.strip()]


def disponibilidad_permite(disponibilidad, dia, bloque):
    slots = slots_disponibles_docente(disponibilidad)
    if slots:
        return f"{dia} {bloque}" in slots
    return dia.lower() in disponibilidad.lower()


def construir_variantes_materia(materias, docentes, aulas, grupo, horarios_importados, docentes_fijos=None):
    docentes_fijos = docentes_fijos or {}
    docentes_por_id = {docente.id: docente for docente in docentes}
    aulas_por_id = {aula.id: aula for aula in aulas}

    importados_por_materia = {}
    for horario in horarios_importados or []:
        importados_por_materia.setdefault(horario["materia_id"], []).append(horario)

    variantes_por_materia = {}

    for materia in materias:
        horarios_materia = importados_por_materia.get(materia.id, [])
        permitidos = {docente.id for docente in docentes_fijos.get(materia.id, [])}

        if materia.sigla == "2006063" and permitidos:
            teoria_items = []
            laboratorio_por_grupo = {}

            for item in horarios_materia:
                if item["docente_id"] not in permitidos:
                    continue
                if item["grupo"].endswith("-GB"):
                    teoria_items.append(item)
                elif "-GB" in item["grupo"]:
                    laboratorio_por_grupo.setdefault(item["grupo_id"], []).append(item)

            teoria_items = sorted(teoria_items, key=lambda x: (x["dia"], x["bloque"], x["docente_id"]))
            variantes = []
            for grupo_id, items in sorted(laboratorio_por_grupo.items()):
                clases = []
                for item in sorted([*teoria_items, *items], key=lambda x: (x["dia"], x["bloque"], x["docente_id"], x["grupo_id"])):
                    docente = docentes_por_id[item["docente_id"]]
                    aula = aulas_por_id[item["aula_id"]]
                    clases.append({
                        "materia_id": materia.id,
                        "materia": materia.nombre,
                        "sigla": materia.sigla,
                        "tipo": item.get("tipo") or materia.tipo,
                        "semestre": materia.semestre,
                        "docente_id": docente.id,
                        "docente": docente.nombre,
                        "disponibilidad_docente": docente.disponibilidad,
                        "aula_id": aula.id,
                        "aula": aula.nombre,
                        "tipo_aula": aula.tipo,
                        "capacidad_aula": aula.capacidad,
                        "grupo_id": item["grupo_id"],
                        "grupo": item["grupo"],
                        "cantidad_estudiantes": grupo.cantidad_estudiantes,
                        "dia": item["dia"],
                        "bloque": item["bloque"],
                    })
                variantes.append({
                    "clave": f"{materia.id}-{grupo_id}",
                    "clases": clases,
                })
            if variantes:
                variantes_por_materia[materia.id] = variantes
                continue

        if permitidos and len(permitidos) == 1:
            horarios_filtrados = [item for item in horarios_materia if item["docente_id"] in permitidos]
            clases = []
            for item in sorted(horarios_filtrados, key=lambda x: (x["dia"], x["bloque"], x["docente_id"], x["grupo_id"])):
                docente = docentes_por_id[item["docente_id"]]
                aula = aulas_por_id[item["aula_id"]]
                clases.append({
                    "materia_id": materia.id,
                    "materia": materia.nombre,
                    "sigla": materia.sigla,
                    "tipo": item.get("tipo") or materia.tipo,
                    "semestre": materia.semestre,
                    "docente_id": docente.id,
                    "docente": docente.nombre,
                    "disponibilidad_docente": docente.disponibilidad,
                    "aula_id": aula.id,
                    "aula": aula.nombre,
                    "tipo_aula": aula.tipo,
                    "capacidad_aula": aula.capacidad,
                    "grupo_id": item["grupo_id"],
                    "grupo": item["grupo"],
                    "cantidad_estudiantes": grupo.cantidad_estudiantes,
                    "dia": item["dia"],
                    "bloque": item["bloque"],
                })
            variantes_por_materia[materia.id] = [{
                "clave": f"{materia.id}-seleccion-fija",
                "clases": clases,
            }]
            continue

        variantes_por_grupo = {}
        for item in horarios_materia:
            if permitidos and item["docente_id"] not in permitidos:
                continue
            variantes_por_grupo.setdefault(item["grupo_id"], []).append(item)

        variantes = []
        for grupo_id, items in sorted(variantes_por_grupo.items()):
            clases = []
            for item in sorted(items, key=lambda x: (x["dia"], x["bloque"], x["docente_id"])):
                docente = docentes_por_id[item["docente_id"]]
                aula = aulas_por_id[item["aula_id"]]
                clases.append({
                    "materia_id": materia.id,
                    "materia": materia.nombre,
                    "sigla": materia.sigla,
                    "tipo": item.get("tipo") or materia.tipo,
                    "semestre": materia.semestre,
                    "docente_id": docente.id,
                    "docente": docente.nombre,
                    "disponibilidad_docente": docente.disponibilidad,
                    "aula_id": aula.id,
                    "aula": aula.nombre,
                    "tipo_aula": aula.tipo,
                    "capacidad_aula": aula.capacidad,
                    "grupo_id": item["grupo_id"],
                    "grupo": item["grupo"],
                    "cantidad_estudiantes": grupo.cantidad_estudiantes,
                    "dia": item["dia"],
                    "bloque": item["bloque"],
                })
            variantes.append({
                "clave": f"{materia.id}-{grupo_id}",
                "clases": clases,
            })

        if not variantes and horarios_materia:
            clases = []
            for item in sorted(horarios_materia, key=lambda x: (x["dia"], x["bloque"], x["docente_id"], x["grupo_id"])):
                docente = docentes_por_id[item["docente_id"]]
                aula = aulas_por_id[item["aula_id"]]
                clases.append({
                    "materia_id": materia.id,
                    "materia": materia.nombre,
                    "sigla": materia.sigla,
                    "tipo": item.get("tipo") or materia.tipo,
                    "semestre": materia.semestre,
                    "docente_id": docente.id,
                    "docente": docente.nombre,
                    "disponibilidad_docente": docente.disponibilidad,
                    "aula_id": aula.id,
                    "aula": aula.nombre,
                    "tipo_aula": aula.tipo,
                    "capacidad_aula": aula.capacidad,
                    "grupo_id": item["grupo_id"],
                    "grupo": item["grupo"],
                    "cantidad_estudiantes": grupo.cantidad_estudiantes,
                    "dia": item["dia"],
                    "bloque": item["bloque"],
                })
            variantes = [{"clave": f"{materia.id}-fallback", "clases": clases}]

        variantes_por_materia[materia.id] = variantes

    return variantes_por_materia


def crear_individuo(variantes_por_materia):
    individuo = {}
    for materia_id, variantes in variantes_por_materia.items():
        individuo[materia_id] = random.randrange(len(variantes)) if variantes else 0
    return individuo


def decodificar_individuo(individuo, variantes_por_materia):
    horario = []
    for materia_id, indice in individuo.items():
        variantes = variantes_por_materia.get(materia_id, [])
        if not variantes:
            continue
        horario.extend(deepcopy(variantes[indice]["clases"]))
    return horario


def calcular_fitness_semestre(horario):
    penalizacion = 0
    conflictos = []
    ocupacion_docente = {}
    ocupacion_aula = {}
    ocupacion_nivel = {}

    for clase in horario:
        clave_tiempo = (clase["dia"], clase["bloque"])
        clave_docente = (clase["docente_id"], *clave_tiempo)
        clave_aula = (clase["aula_id"], *clave_tiempo)
        clave_nivel = (clase["semestre"], *clave_tiempo)

        if clave_docente in ocupacion_docente:
            penalizacion += 80
            conflictos.append(f"Choque de docente: {clase['docente']} en {clase['dia']} {clase['bloque']}")
        else:
            ocupacion_docente[clave_docente] = True

        if clave_aula in ocupacion_aula:
            penalizacion += 80
            conflictos.append(f"Choque de aula: {clase['aula']} en {clase['dia']} {clase['bloque']}")
        else:
            ocupacion_aula[clave_aula] = True

        if clave_nivel in ocupacion_nivel:
            clase_previa = ocupacion_nivel[clave_nivel]
            penalizacion += 90
            conflictos.append(
                f"Choque de horario: {clase_previa['materia']} y {clase['materia']} en {clase['dia']} {clase['bloque']}"
            )
        else:
            ocupacion_nivel[clave_nivel] = clase

        if clase["cantidad_estudiantes"] > clase["capacidad_aula"]:
            penalizacion += 25
            conflictos.append(f"Aula insuficiente: {clase['aula']} para {clase['materia']}")

        # Las combinaciones provienen del horario real importado. Si un bloque
        # ya existe en el horario base, no se penaliza por la clasificacion
        # local del aula porque eso introduce conflictos artificiales.

        if not disponibilidad_permite(clase["disponibilidad_docente"], clase["dia"], clase["bloque"]):
            penalizacion += 20
            conflictos.append(f"Docente fuera de disponibilidad: {clase['docente']} - {clase['dia']}")

    fitness = max(1, 10000 - penalizacion)
    return fitness, conflictos


def evaluar_individuo(individuo, variantes_por_materia):
    horario = decodificar_individuo(individuo, variantes_por_materia)
    fitness, conflictos = calcular_fitness_semestre(horario)
    return {
        "individuo": deepcopy(individuo),
        "horario": horario,
        "fitness": fitness,
        "conflictos": conflictos,
    }


def clave_candidato(candidato):
    return (len(candidato["conflictos"]), -candidato["fitness"])


def seleccionar_padres(poblacion):
    torneo = random.sample(poblacion, k=min(4, len(poblacion)))
    torneo.sort(key=clave_candidato)
    return torneo[0]["individuo"], torneo[1]["individuo"]


def cruzar(padre1, padre2):
    hijo = {}
    for materia_id in padre1:
        hijo[materia_id] = padre1[materia_id] if random.random() < 0.5 else padre2[materia_id]
    return hijo


def mutar(individuo, variantes_por_materia, prob_mutacion):
    hijo = deepcopy(individuo)
    for materia_id, variantes in variantes_por_materia.items():
        if len(variantes) <= 1:
            continue
        if random.random() < prob_mutacion:
            opciones = [i for i in range(len(variantes)) if i != hijo[materia_id]]
            if opciones:
                hijo[materia_id] = random.choice(opciones)
    return hijo


def serializar_horario(horario):
    return [
        {
            "materia_id": clase["materia_id"],
            "materia": clase["materia"],
            "sigla": clase["sigla"],
            "docente_id": clase["docente_id"],
            "docente": clase["docente"],
            "aula_id": clase["aula_id"],
            "aula": clase["aula"],
            "grupo_id": clase["grupo_id"],
            "grupo": clase["grupo"],
            "semestre": clase["semestre"],
            "dia": clase["dia"],
            "bloque": clase["bloque"],
            "tipo": clase["tipo"],
        }
        for clase in horario
    ]


def generar_horario_semestre_ag(
    materias,
    docentes,
    aulas,
    grupo,
    docentes_fijos=None,
    horarios_importados=None,
    poblacion_size=80,
    generaciones=120,
    prob_mutacion=0.28,
    max_alternativas=25,
):
    variantes_por_materia = construir_variantes_materia(
        materias=materias,
        docentes=docentes,
        aulas=aulas,
        grupo=grupo,
        horarios_importados=horarios_importados,
        docentes_fijos=docentes_fijos,
    )

    candidatos_globales = []

    for _ in range(8):
        poblacion = []
        while len(poblacion) < poblacion_size:
            individuo = crear_individuo(variantes_por_materia)
            poblacion.append(evaluar_individuo(individuo, variantes_por_materia))

        for _ in range(generaciones):
            poblacion.sort(key=clave_candidato)
            nueva_poblacion = poblacion[: max(2, poblacion_size // 4)]

            while len(nueva_poblacion) < poblacion_size:
                padre1, padre2 = seleccionar_padres(poblacion)
                hijo = cruzar(padre1, padre2)
                hijo = mutar(hijo, variantes_por_materia, prob_mutacion)
                nueva_poblacion.append(evaluar_individuo(hijo, variantes_por_materia))

            poblacion = nueva_poblacion

        poblacion.sort(key=clave_candidato)
        candidatos_globales.extend(poblacion[: max(max_alternativas * 3, 50)])

    candidatos_globales.sort(key=clave_candidato)

    agrupadas = {0: [], 1: [], 2: [], 3: [], "resto": []}
    firmas = set()
    for candidato in candidatos_globales:
        firma = tuple(sorted(candidato["individuo"].items()))
        if firma in firmas:
            continue
        firmas.add(firma)
        alternativa = {
            "fitness": candidato["fitness"],
            "conflictos": candidato["conflictos"][:20],
            "horario": serializar_horario(candidato["horario"]),
        }
        cantidad_conflictos = len(candidato["conflictos"])
        if cantidad_conflictos in agrupadas:
            agrupadas[cantidad_conflictos].append(alternativa)
        else:
            agrupadas["resto"].append(alternativa)

    alternativas = []
    for clave in [0, 1, 2, 3, "resto"]:
        for alternativa in agrupadas[clave]:
            alternativas.append(alternativa)
            if len(alternativas) >= max_alternativas:
                break
        if len(alternativas) >= max_alternativas:
            break

    mejor = alternativas[0] if alternativas else {"fitness": 1, "conflictos": [], "horario": []}
    return {
        "mejor_horario": mejor["horario"],
        "fitness": mejor["fitness"],
        "conflictos": mejor["conflictos"],
        "alternativas": alternativas,
    }
