from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID

class CupoBase(SQLModel):
    establecimiento_id: UUID = Field(foreign_key="establecimiento.id", description="ID del establecimiento asociado al cupo", nullable=False)
    nivel_practica_id: int = Field(foreign_key="nivel_practica.id", description="ID del nivel de práctica asociado al cupo", nullable=False)