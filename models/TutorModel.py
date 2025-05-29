from sqlmodel import SQLModel, Field
from typing import Optional

class TutorBase(SQLModel):
    nombre: str = Field(max_length=150, description="Nombre del tutor", nullable=False)
    email: str = Field(max_length=100, description="Email del tutor", nullable=False, unique=True)
    
class Tutor(TutorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID del tutor")