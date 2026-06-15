from pydantic import BaseModel

class DocenteBase(BaseModel):
    nombre: str
    correo: str | None = None
    especialidad: str
    disponibilidad: str

class DocenteCreate(DocenteBase):
    pass

class DocenteResponse(DocenteBase):
    id: int

    class Config:
        from_attributes = True

class MateriaBase(BaseModel):
    nombre: str
    sigla: str
    semestre: int
    horas_semana: int
    tipo: str

class MateriaCreate(MateriaBase):
    pass

class MateriaResponse(MateriaBase):
    id: int

    class Config:
        from_attributes = True

class AulaBase(BaseModel):
    nombre: str
    capacidad: int
    tipo: str

class AulaCreate(AulaBase):
    pass

class AulaResponse(AulaBase):
    id: int

    class Config:
        from_attributes = True

class GrupoBase(BaseModel):
    nombre: str
    semestre: int
    cantidad_estudiantes: int

class GrupoCreate(GrupoBase):
    pass

class GrupoResponse(GrupoBase):
    id: int

    class Config:
        from_attributes = True

class HorarioResponse(BaseModel):
    id: int
    materia: str
    sigla: str
    docente: str
    aula: str
    grupo: str
    semestre: int
    dia: str
    bloque: str
    tipo: str

    class Config:
        from_attributes = True
