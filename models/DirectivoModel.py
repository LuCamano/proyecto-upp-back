from sqlmodel import SQLModel, Field

class DirectivoBase(SQLModel):
    nombre: str = Field(max_length=150, description="Nombre del directivo", nullable=False)
    email: str = Field(max_length=100, description="Email del directivo", nullable=False, unique=True)
    cargo: str = Field(max_length=150, description="Cargo del directivo", nullable=False)