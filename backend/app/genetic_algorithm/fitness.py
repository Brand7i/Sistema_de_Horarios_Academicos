def calcular_fitness(horario):
    penalizacion = 0
    conflictos = []

    ocupacion_docente = {}
    ocupacion_aula = {}
    ocupacion_grupo = {}

    for clase in horario:
        clave_tiempo = (clase["dia"], clase["bloque"])

        clave_docente = (clase["docente_id"], *clave_tiempo)
        clave_aula = (clase["aula_id"], *clave_tiempo)
        clave_grupo = (clase["grupo_id"], *clave_tiempo)

        if clave_docente in ocupacion_docente:
            penalizacion += 50
            conflictos.append(f"Choque de docente: {clase['docente']} en {clase['dia']} {clase['bloque']}")
        else:
            ocupacion_docente[clave_docente] = True

        if clave_aula in ocupacion_aula:
            penalizacion += 50
            conflictos.append(f"Choque de aula: {clase['aula']} en {clase['dia']} {clase['bloque']}")
        else:
            ocupacion_aula[clave_aula] = True

        if clave_grupo in ocupacion_grupo:
            penalizacion += 60
            conflictos.append(f"Choque de grupo: {clase['grupo']} en {clase['dia']} {clase['bloque']}")
        else:
            ocupacion_grupo[clave_grupo] = True

        if clase["cantidad_estudiantes"] > clase["capacidad_aula"]:
            penalizacion += 25
            conflictos.append(f"Aula insuficiente: {clase['aula']} para {clase['grupo']}")

        if clase["tipo"].lower() == "laboratorio" and clase["tipo_aula"].lower() != "laboratorio":
            penalizacion += 35
            conflictos.append(f"Materia de laboratorio en aula no válida: {clase['materia']}")

        disponibilidad = clase["disponibilidad_docente"].lower()
        if clase["dia"].lower() not in disponibilidad:
            penalizacion += 15
            conflictos.append(f"Docente fuera de disponibilidad: {clase['docente']} - {clase['dia']}")

    fitness = max(1, 1000 - penalizacion)
    return fitness, conflictos
