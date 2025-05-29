from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID

class DirectivoEstablecimientoBase(SQLModel):
    directivo_id: int = Field(foreign_key="directivo.id", description="ID del directivo", nullable=False)
    establecimiento_id: UUID = Field(foreign_key="establecimiento.id", description="ID del establecimiento", nullable=False)
    
class DirectivoEstablecimiento(DirectivoEstablecimientoBase, table=True):
    __tablename__ = "directivo_establecimiento"
    id: Optional[int] = Field(default=None, primary_key=True, description="ID de la relación directivo-establecimiento")
    