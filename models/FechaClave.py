from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

class FechaClave(SQLModel, table=True):
    nombre: str = Field(max_length=150, description="Nombre de la fecha clave", primary_key=True)
    fecha: date = Field(description="Fecha de la fecha clave", nullable=False)
    descripcion: Optional[str] = Field(default=None, max_length=500, description="Descripción de la fecha clave", nullable=True)