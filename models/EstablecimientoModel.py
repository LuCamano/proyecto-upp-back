from sqlmodel import SQLModel, Field

class EstablecimientoBase(SQLModel):
    rbd: str = Field(max_length=10, description="RBD del establecimiento", nullable=False, unique=True)
    nombre: str = Field(max_length=300, description="Nombre del establecimiento", nullable=False)
    dependencia: str = Field(max_length=50, description="Dependencia del establecimiento", nullable=False)
    comuna_id: int = Field(foreign_key="comuna.id", description="ID de la comuna del establecimiento", nullable=False)
    
