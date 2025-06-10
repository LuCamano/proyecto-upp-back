from sqlmodel import SQLModel, Field

class CarreraBase(SQLModel):
    nombre: str = Field(max_length=300, description="Nombre de la carrera", nullable=False, unique=True)
