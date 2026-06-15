# Sistema de Horarios Académicos Automáticos - UMSS

Sistema base para generar horarios académicos usando un **Algoritmo Genético en Python**.

## Tecnologías

- Backend: Python + FastAPI
- Algoritmo genético: Python
- Base de datos: SQLite
- Frontend: React + Vite

## Estructura

```txt
sistema-horarios-ag/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── seed.py
│       ├── routes/
│       └── genetic_algorithm/
└── frontend/
    └── src/
        ├── pages/
        ├── components/
        └── services/
```

## Cómo ejecutar

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

El backend corre en:

```txt
http://127.0.0.1:8000
```

Documentación API:

```txt
http://127.0.0.1:8000/docs
```

### 2. Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

El frontend corre en:

```txt
http://localhost:5173
```

## Flujo del sistema

1. Registrar docentes.
2. Registrar materias.
3. Registrar aulas.
4. Registrar grupos.
5. Generar horario.
6. Visualizar conflictos y fitness.
7. Ver el horario final.

## Explicación del algoritmo genético

Cada cromosoma representa un horario completo.  
Cada gen representa una clase asignada a:

```txt
Materia + Grupo + Docente + Aula + Día + Bloque horario
```

El fitness penaliza:

- Choque de docente.
- Choque de aula.
- Choque de grupo.
- Aula con capacidad insuficiente.
- Materia de laboratorio asignada a aula teórica.
- Docente fuera de disponibilidad.

Mientras menos conflictos tenga el horario, mayor será su fitness.
