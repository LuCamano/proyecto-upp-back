from sqlmodel import SQLModel, Field, TEXT
from typing import Optional

class EstudianteBase(SQLModel):
    rut: str = Field(max_length=12, description="RUT del estudiante", nullable=False, unique=True, index=True)
    nombre: str = Field(max_length=150, description="Nombre del estudiante", nullable=False)
    ap_paterno: str = Field(max_length=150, description="Apellido paterno del estudiante", nullable=False)
    ap_materno: str = Field(max_length=150, description="Apellido materno del estudiante", nullable=False)
    email: str = Field(max_length=100, description="Correo electrónico del estudiante", nullable=False, unique=True)
    cond_especial: Optional[str] = Field(default=None, nullable=True, sa_type=TEXT, description="Condición especial del estudiante (opcional)")
    carrera_id: int = Field(foreign_key="carrera.id", description="ID de la carrera del estudiante", nullable=False)
    comuna_id: int = Field(foreign_key="comuna.id", description="ID de la comuna del estudiante", nullable=False)
    tutor_id: Optional[int] = Field(default=None, foreign_key="tutor.id", description="ID del tutor del estudiante (opcional)", nullable=True)