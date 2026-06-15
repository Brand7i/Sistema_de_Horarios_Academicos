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
    materia_id: int
    materia: str
    sigla: str
    docente_id: int
    docente: str
    aula_id: int
    aula: str
    grupo_id: int
    grupo: str
    semestre: int
    dia: str
    bloque: str
    tipo: str
    origen: str
    escenario: str | None = None

    class Config:
        from_attributes = True


class DocenteOpcion(BaseModel):
    id: int
    nombre: str
    grupo_referencia: str


class MateriaConfiguracion(BaseModel):
    materia_id: int
    nombre: str
    sigla: str
    tipo: str
    horas_semana: int
    docentes: list[DocenteOpcion]


class HorarioConfiguracionResponse(BaseModel):
    semestre: int
    nivel: str
    materias: list[MateriaConfiguracion]


class HorarioGeneracionRequest(BaseModel):
    semestre: int
    docentes_por_materia: dict[int, int | list[int]]
