from sqlmodel import SQLModel, Field

class TutorBase(SQLModel):
    nombre: str = Field(max_length=150, description="Nombre del tutor", nullable=False)
    email: str = Field(max_length=100, description="Email del tutor", nullable=False, unique=True)
    