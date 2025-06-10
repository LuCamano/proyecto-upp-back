# Importacion de los modelos para facil acceso y orden de creacion en la base de datos
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship
from .ComunaModel import ComunaBase
from .TutorModel import TutorBase
from .CarreraModel import CarreraBase
from .DirectivoModel import DirectivoBase
from .EstablecimientoModel import EstablecimientoBase
from .NivelPracticaModel import NivelPracticaBase
from .EstudianteModel import EstudianteBase
from .CupoModel import CupoBase
from .FichaModel import FichaBase
from .ManyToMany import DirectivoEstablecimiento, DirectivoEstablecimientoBase

class Comuna(ComunaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
class Tutor(TutorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID del tutor")
    
class Carrera(CarreraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID de la carrera")
    
class Directivo(DirectivoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID del directivo")
    
class Establecimiento(EstablecimientoBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, description="ID del establecimiento")
    directivos: List["Directivo"] = Relationship(link_model=DirectivoEstablecimiento)
    
class NivelPractica(NivelPracticaBase, table=True):
    __tablename__ = "nivel_practica"
    id: Optional[int] = Field(default=None, primary_key=True, description="ID del nivel de práctica")
    
class Estudiante(EstudianteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID del estudiante")
    fichas: List["Ficha"] = Relationship(back_populates="estudiante")
class Cupo(CupoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID del cupo")
    nivel_practica: NivelPractica = Relationship()
    
class Ficha(FichaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="ID de la ficha")
    estudiante: Estudiante = Relationship(back_populates="fichas")
    establecimiento: Establecimiento = Relationship()
    cupo: Cupo = Relationship()