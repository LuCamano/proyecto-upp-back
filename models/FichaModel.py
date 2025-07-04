from sqlmodel import SQLModel, Field, TIMESTAMP
from typing import Optional
from uuid import UUID
from datetime import date, datetime

class FichaBase(SQLModel):
    estudiante_id: int = Field(foreign_key="estudiante.id", description="ID del estudiante asociado a la ficha", nullable=False)
    establecimiento_id: UUID = Field(foreign_key="establecimiento.id", description="ID del establecimiento asociado a la ficha", nullable=False)
    cupo_id: int = Field(foreign_key="cupo.id", description="ID del cupo asociado a la ficha", nullable=False, unique=True)
    fecha_inicio: date = Field(description="Fecha de inicio de la ficha", nullable=False)
    fecha_termino: Optional[date] = Field(default=None, description="Fecha de término de la ficha", nullable=True)
    fecha_envio: datetime = Field(description="Fecha de envío de la ficha al estudiante", sa_type=TIMESTAMP, nullable=False)