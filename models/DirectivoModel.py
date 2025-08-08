from sqlmodel import SQLModel, Field
from uuid import UUID

class DirectivoBase(SQLModel):
    nombre: str = Field(max_length=150, description="Nombre del directivo", nullable=False)
    email: str = Field(max_length=100, description="Email del directivo", nullable=False)
    cargo: str = Field(max_length=150, description="Cargo del directivo", nullable=False)
    establecimiento_id: UUID = Field(foreign_key="establecimiento.id", description="ID del establecimiento al que pertenece el directivo", nullable=False)