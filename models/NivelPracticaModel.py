from sqlmodel import SQLModel, Field
from typing import Optional

class NivelPracticaBase(SQLModel):
    nombre: str = Field(max_length=100, description="Nombre del nivel de práctica", nullable=False)
    carrera_id: int = Field(foreign_key="carrera.id", description="ID de la carrera asociada al nivel de práctica", nullable=False)
