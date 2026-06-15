# Backend - FastAPI

## Ejecutar

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload
```

## Endpoints principales

```txt
GET  /docentes
POST /docentes

GET  /materias
POST /materias

GET  /aulas
POST /aulas

GET  /grupos
POST /grupos

POST /horarios/generar
GET  /horarios
```
