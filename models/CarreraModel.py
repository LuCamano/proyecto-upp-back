from sqlmodel import SQLModel, Field
from typing import Optional

class CarreraBase(SQLModel):
    nombre: str = Field(max_length=300, description="Nombre de la carrera", nullable=False, unique=True)
    
class Carrera(CarreraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID de la carrera")