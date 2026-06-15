import random
from copy import deepcopy

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

BLOQUES = [
    "08:00-10:00",
    "10:00-12:00",
    "14:00-16:00",
    "16:00-18:00"
]

def docente_para_materia(materia, docentes):
    nombre_materia = materia.nombre.lower()
    candidatos = [
        d for d in docentes
        if d.especialidad.lower() in nombre_materia or nombre_materia in d.especialidad.lower()
    ]
    return random.choice(candidatos if candidatos else docentes)

def aula_para_materia(materia, aulas):
    if materia.tipo.lower() == "laboratorio":
        laboratorios = [a for a in aulas if a.tipo.lower() == "laboratorio"]
        return random.choice(laboratorios if laboratorios else aulas)
    return random.choice(aulas)

def crear_horario_aleatorio(docentes, materias, aulas, grupos):
    horario = []

    for grupo in grupos:
        materias_semestre = [m for m in materias if m.semestre == grupo.semestre]

        for materia in materias_semestre:
            cantidad_bloques = max(1, materia.horas_semana // 2)

            for _ in range(cantidad_bloques):
                docente = docente_para_materia(materia, docentes)
                aula = aula_para_materia(materia, aulas)

                horario.append({
                    "materia_id": materia.id,
                    "materia": materia.nombre,
                    "sigla": materia.sigla,
                    "tipo": materia.tipo,
                    "semestre": materia.semestre,

                    "docente_id": docente.id,
                    "docente": docente.nombre,
                    "disponibilidad_docente": docente.disponibilidad,

                    "aula_id": aula.id,
                    "aula": aula.nombre,
                    "tipo_aula": aula.tipo,
                    "capacidad_aula": aula.capacidad,

                    "grupo_id": grupo.id,
                    "grupo": grupo.nombre,
                    "cantidad_estudiantes": grupo.cantidad_estudiantes,

                    "dia": random.choice(DIAS),
                    "bloque": random.choice(BLOQUES)
                })

    return horario

def seleccionar_padres(poblacion):
    torneo = random.sample(poblacion, k=min(5, len(poblacion)))
    torneo.sort(key=lambda x: x["fitness"], reverse=True)
    return torneo[0]["horario"], torneo[1]["horario"]

def cruzar(padre1, padre2):
    if len(padre1) <= 1:
        return deepcopy(padre1)

    punto = random.randint(1, len(padre1) - 1)
    hijo = deepcopy(padre1[:punto] + padre2[punto:])
    return hijo

def mutar(horario, docentes, aulas, prob_mutacion):
    hijo = deepcopy(horario)

    for clase in hijo:
        if random.random() < prob_mutacion:
            cambio = random.choice(["dia", "bloque", "aula", "docente"])

            if cambio == "dia":
                clase["dia"] = random.choice(DIAS)

            elif cambio == "bloque":
                clase["bloque"] = random.choice(BLOQUES)

            elif cambio == "aula":
                aulas_validas = aulas
                if clase["tipo"].lower() == "laboratorio":
                    labs = [a for a in aulas if a.tipo.lower() == "laboratorio"]
                    aulas_validas = labs if labs else aulas
                aula = random.choice(aulas_validas)
                clase["aula_id"] = aula.id
                clase["aula"] = aula.nombre
                clase["tipo_aula"] = aula.tipo
                clase["capacidad_aula"] = aula.capacidad

            elif cambio == "docente":
                docente = random.choice(docentes)
                clase["docente_id"] = docente.id
                clase["docente"] = docente.nombre
                clase["disponibilidad_docente"] = docente.disponibilidad

    return hijo
