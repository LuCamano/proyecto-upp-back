# Importacion de los modelos para facil acceso y orden de creacion en la base de datos
from .ComunaModel import Comuna, ComunaBase
from .TutorModel import Tutor, TutorBase
from .CarreraModel import Carrera, CarreraBase
from .DirectivoModel import Directivo, DirectivoBase
from .EstablecimientoModel import Establecimiento, EstablecimientoBase
from .NivelPracticaModel import NivelPractica, NivelPracticaBase
from .EstudianteModel import Estudiante, EstudianteBase
from .CupoModel import Cupo, CupoBase
from .FichaModel import Ficha, FichaBase
from .ManyToMany import DirectivoEstablecimiento, DirectivoEstablecimientoBase