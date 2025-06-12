from sqlmodel import SQLModel, Field
from typing import Optional

class ComunaBase(SQLModel):
    nombre: str = Field(max_length=200, description="Nombre de la comuna", nullable=False, unique=True)
    