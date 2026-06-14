# Sistema de Horarios Academicos

Proyecto base para generar horarios de clases de la carrera de Ingenieria Informatica usando algoritmos geneticos.

## Objetivo

Construir una aplicacion que genere horarios automaticamente evitando conflictos entre:

- aulas
- profesores
- grupos de estudiantes

## Enfoque con algoritmos geneticos

Cada solucion candidata representa un horario completo. El algoritmo genetico trabaja asi:

1. Genera una poblacion inicial de horarios aleatorios.
2. Evalua cada horario con una funcion de fitness.
3. Penaliza conflictos duros:
   - un profesor en dos clases al mismo tiempo
   - un aula ocupada por dos clases al mismo tiempo
   - un grupo de estudiantes en dos clases al mismo tiempo
   - aulas con capacidad insuficiente
4. Penaliza reglas blandas:
   - distribucion poco equilibrada de clases
   - exceso de huecos
   - asignaciones poco convenientes
5. Selecciona los mejores horarios.
6. Cruza y muta soluciones para crear nuevas generaciones.
7. Repite hasta encontrar una solucion aceptable.

## Estructura del proyecto

```text
Sistema_de_Horarios_Academicos/
├── backend/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── domain/
│       ├── genetic/
│       └── services/
├── frontend/
│   ├── assets/
│   └── index.html
├── .gitignore
├── README.md
└── requirements.txt
```

## Backend

- `api/`: rutas HTTP
- `core/`: configuracion base
- `domain/`: entidades y modelos del problema
- `genetic/`: logica del algoritmo genetico
- `services/`: orquestacion del caso de uso

## Frontend

- interfaz base para lanzar la generacion
- vista simple para mostrar el resultado

## Flujo esperado del sistema

1. Registrar materias, docentes, aulas, grupos y franjas horarias.
2. Enviar esos datos al backend.
3. Ejecutar el algoritmo genetico.
4. Devolver el mejor horario encontrado con su puntaje y conflictos.

## Ejecucion futura

Cuando instales dependencias, el backend se podra ejecutar con:

```bash
uvicorn backend.app.main:app --reload
```

Luego abre `frontend/index.html` en navegador o sirve esa carpeta con un servidor estatico.

## Proximo paso recomendado

Cuando me mandes los horarios reales, materias, docentes, aulas y restricciones, se reemplaza la data de ejemplo y se ajusta el fitness con las reglas exactas de tu carrera.
