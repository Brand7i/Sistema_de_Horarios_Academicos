from app.genetic_algorithm.fitness import calcular_fitness
from app.genetic_algorithm.operadores import (
    crear_horario_aleatorio,
    seleccionar_padres,
    cruzar,
    mutar
)

def evaluar_horario(horario):
    fitness, conflictos = calcular_fitness(horario)
    return {
        "horario": horario,
        "fitness": fitness,
        "conflictos": conflictos
    }

def generar_horario_ag(
    docentes,
    materias,
    aulas,
    grupos,
    poblacion_size=80,
    generaciones=120,
    prob_mutacion=0.12
):
    poblacion = []

    for _ in range(poblacion_size):
        horario = crear_horario_aleatorio(docentes, materias, aulas, grupos)
        poblacion.append(evaluar_horario(horario))

    for _ in range(generaciones):
        poblacion.sort(key=lambda x: x["fitness"], reverse=True)

        nueva_poblacion = poblacion[:10]

        while len(nueva_poblacion) < poblacion_size:
            padre1, padre2 = seleccionar_padres(poblacion)
            hijo = cruzar(padre1, padre2)
            hijo = mutar(hijo, docentes, aulas, prob_mutacion)
            nueva_poblacion.append(evaluar_horario(hijo))

        poblacion = nueva_poblacion

    poblacion.sort(key=lambda x: x["fitness"], reverse=True)
    mejor = poblacion[0]

    horario_limpio = []
    for clase in mejor["horario"]:
        horario_limpio.append({
            "materia": clase["materia"],
            "sigla": clase["sigla"],
            "docente": clase["docente"],
            "aula": clase["aula"],
            "grupo": clase["grupo"],
            "semestre": clase["semestre"],
            "dia": clase["dia"],
            "bloque": clase["bloque"],
            "tipo": clase["tipo"]
        })

    return {
        "mejor_horario": horario_limpio,
        "fitness": mejor["fitness"],
        "conflictos": mejor["conflictos"][:20]
    }
