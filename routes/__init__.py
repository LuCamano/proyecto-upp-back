from uuid import UUID
from fastapi import APIRouter, HTTPException
from services import BaseCrudService, DirectivoService
from app.db import SessionDep
import models

router = APIRouter()

## Comuna Routes
# CRUD operations for Comuna model
@router.post("/comunas", response_model=models.Comuna)
async def create_comuna(session: SessionDep, comuna: models.ComunaBase):
    controller = BaseCrudService(models.Comuna)
    try:
        db_comuna = controller.create(session, comuna)
        return db_comuna
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/comunas/{comuna_id}", response_model=models.Comuna)
async def read_comuna(comuna_id: int, session: SessionDep):
    controller = BaseCrudService(models.Comuna)
    try:
        db_comuna = controller.read(session, comuna_id)
        return db_comuna
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/comunas", response_model=list[models.Comuna])
async def read_all_comunas(session: SessionDep):
    controller = BaseCrudService(models.Comuna)
    try:
        comunas = controller.all(session)
        return comunas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/comunas/{comuna_id}", response_model=models.Comuna)
async def update_comuna(comuna_id: int, comuna: models.ComunaBase, session: SessionDep):
    controller = BaseCrudService(models.Comuna)
    try:
        updated_comuna = controller.update(session, comuna_id, comuna)
        return updated_comuna
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/comunas/{comuna_id}")
async def delete_comuna(comuna_id: int, session: SessionDep):
    controller = BaseCrudService(models.Comuna)
    try:
        result = controller.delete(session, comuna_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## Carrera Routes
# CRUD operations for Carrera model
@router.post("/carreras", response_model=models.Carrera)
async def create_carrera(session: SessionDep, carrera: models.CarreraBase):
    controller = BaseCrudService(models.Carrera)
    try:
        db_carrera = controller.create(session, carrera)
        return db_carrera
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/carreras/{carrera_id}", response_model=models.Carrera)
async def read_carrera(carrera_id: int, session: SessionDep):
    controller = BaseCrudService(models.Carrera)
    try:
        db_carrera = controller.read(session, carrera_id)
        return db_carrera
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/carreras", response_model=list[models.Carrera])
async def read_all_carreras(session: SessionDep):
    controller = BaseCrudService(models.Carrera)
    try:
        carreras = controller.all(session)
        return carreras
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/carreras/{carrera_id}", response_model=models.Carrera)
async def update_carrera(carrera_id: int, carrera: models.CarreraBase, session: SessionDep):
    controller = BaseCrudService(models.Carrera)
    try:
        updated_carrera = controller.update(session, carrera_id, carrera)
        return updated_carrera
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/carreras/{carrera_id}")
async def delete_carrera(carrera_id: int, session: SessionDep):
    controller = BaseCrudService(models.Carrera)
    try:
        result = controller.delete(session, carrera_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

## Tutor Routes
# CRUD operations for Tutor model
@router.post("/tutores", response_model=models.Tutor)
async def create_tutor(session: SessionDep, tutor: models.TutorBase):
    controller = BaseCrudService(models.Tutor)
    try:
        db_tutor = controller.create(session, tutor)
        return db_tutor
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tutores/{tutor_id}", response_model=models.Tutor)
async def read_tutor(tutor_id: int, session: SessionDep):
    controller = BaseCrudService(models.Tutor)
    try:
        db_tutor = controller.read(session, tutor_id)
        return db_tutor
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/tutores", response_model=list[models.Tutor])
async def read_all_tutores(session: SessionDep):
    controller = BaseCrudService(models.Tutor)
    try:
        tutores = controller.all(session)
        return tutores
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/tutores/{tutor_id}", response_model=models.Tutor)
async def update_tutor(tutor_id: int, tutor: models.TutorBase, session: SessionDep):
    controller = BaseCrudService(models.Tutor)
    try:
        updated_tutor = controller.update(session, tutor_id, tutor)
        return updated_tutor
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/tutores/{tutor_id}")
async def delete_tutor(tutor_id: int, session: SessionDep):
    controller = BaseCrudService(models.Tutor)
    try:
        result = controller.delete(session, tutor_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## Directivo Routes
# CRUD operations for Directivo model
@router.post("/directivos", response_model=models.Directivo)
async def create_directivo(session: SessionDep, directivo: models.DirectivoBase):
    controller = DirectivoService()
    try:
        db_directivo = controller.create(session, directivo)
        return db_directivo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/directivos/{directivo_id}", response_model=models.Directivo)
async def read_directivo(directivo_id: int, session: SessionDep):
    controller = DirectivoService()
    try:
        db_directivo = controller.read(session, directivo_id)
        return db_directivo
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/directivos", response_model=list[models.Directivo])
async def read_all_directivos(session: SessionDep):
    controller = DirectivoService()
    try:
        directivos = controller.all(session)
        return directivos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/directivos/{directivo_id}", response_model=models.Directivo)
async def update_directivo(directivo_id: int, directivo: models.DirectivoBase, session: SessionDep):
    controller = DirectivoService()
    try:
        updated_directivo = controller.update(session, directivo_id, directivo)
        return updated_directivo
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/directivos/{directivo_id}")
async def delete_directivo(directivo_id: int, session: SessionDep):
    controller = DirectivoService()
    try:
        result = controller.delete(session, directivo_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## Establecimiento Routes
# CRUD operations for Establecimiento model
@router.post("/establecimientos", response_model=models.Establecimiento)
async def create_establecimiento(session: SessionDep, establecimiento: models.EstablecimientoBase):
    controller = BaseCrudService(models.Establecimiento)
    try:
        db_establecimiento = controller.create(session, establecimiento)
        return db_establecimiento
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/establecimientos/{establecimiento_id}", response_model=models.Establecimiento)
async def read_establecimiento(establecimiento_id: UUID, session: SessionDep):
    controller = BaseCrudService(models.Establecimiento)
    try:
        db_establecimiento = controller.read(session, establecimiento_id)
        return db_establecimiento
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/establecimientos", response_model=list[models.Establecimiento])
async def read_all_establecimientos(session: SessionDep):
    controller = BaseCrudService(models.Establecimiento)
    try:
        establecimientos = controller.all(session)
        return establecimientos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/establecimientos/{establecimiento_id}", response_model=models.Establecimiento)
async def update_establecimiento(establecimiento_id: UUID, establecimiento: models.EstablecimientoBase, session: SessionDep):
    controller = BaseCrudService(models.Establecimiento)
    try:
        updated_establecimiento = controller.update(session, establecimiento_id, establecimiento)
        return updated_establecimiento
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/establecimientos/{establecimiento_id}")
async def delete_establecimiento(establecimiento_id: UUID, session: SessionDep):
    controller = BaseCrudService(models.Establecimiento)
    try:
        result = controller.delete(session, establecimiento_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## NivelPractica Routes
# CRUD operations for NivelPractica model
@router.post("/nivelpractica", response_model=models.NivelPractica)
async def create_nivelpractica(session: SessionDep, nivelpractica: models.NivelPracticaBase):
    controller = BaseCrudService(models.NivelPractica)
    try:
        db_nivelpractica = controller.create(session, nivelpractica)
        return db_nivelpractica
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/nivelpractica/{nivelpractica_id}", response_model=models.NivelPractica)
async def read_nivelpractica(nivelpractica_id: int, session: SessionDep):
    controller = BaseCrudService(models.NivelPractica)
    try:
        db_nivelpractica = controller.read(session, nivelpractica_id)
        return db_nivelpractica
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/nivelpractica", response_model=list[models.NivelPractica])
async def read_all_nivelpractica(session: SessionDep):
    controller = BaseCrudService(models.NivelPractica)
    try:
        nivelpractica = controller.all(session)
        return nivelpractica
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/nivelpractica/{nivelpractica_id}", response_model=models.NivelPractica)
async def update_nivelpractica(nivelpractica_id: int, nivelpractica: models.NivelPracticaBase, session: SessionDep):
    controller = BaseCrudService(models.NivelPractica)
    try:
        updated_nivelpractica = controller.update(session, nivelpractica_id, nivelpractica)
        return updated_nivelpractica
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/nivelpractica/{nivelpractica_id}")
async def delete_nivelpractica(nivelpractica_id: int, session: SessionDep):
    controller = BaseCrudService(models.NivelPractica)
    try:
        result = controller.delete(session, nivelpractica_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## Estudiante Routes
# CRUD operations for Estudiante model
@router.post("/estudiantes", response_model=models.Estudiante)
async def create_estudiante(session: SessionDep, estudiante: models.EstudianteBase):
    controller = BaseCrudService(models.Estudiante)
    try:
        db_estudiante = controller.create(session, estudiante)
        return db_estudiante
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/estudiantes/{estudiante_id}", response_model=models.Estudiante)
async def read_estudiante(estudiante_id: int, session: SessionDep):
    controller = BaseCrudService(models.Estudiante)
    try:
        db_estudiante = controller.read(session, estudiante_id)
        return db_estudiante
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/estudiantes", response_model=list[models.Estudiante])
async def read_all_estudiantes(session: SessionDep):
    controller = BaseCrudService(models.Estudiante)
    try:
        estudiantes = controller.all(session)
        return estudiantes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/estudiantes/{estudiante_id}", response_model=models.Estudiante)
async def update_estudiante(estudiante_id: int, estudiante: models.EstudianteBase, session: SessionDep):
    controller = BaseCrudService(models.Estudiante)
    try:
        updated_estudiante = controller.update(session, estudiante_id, estudiante)
        return updated_estudiante
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/estudiantes/{estudiante_id}")
async def delete_estudiante(estudiante_id: int, session: SessionDep):
    controller = BaseCrudService(models.Estudiante)
    try:
        result = controller.delete(session, estudiante_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## Cupo Routes
# CRUD operations for Cupo model
@router.post("/cupos", response_model=models.Cupo)
async def create_cupo(session: SessionDep, cupo: models.CupoBase):
    controller = BaseCrudService(models.Cupo)
    try:
        db_cupo = controller.create(session, cupo)
        return db_cupo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/cupos/{cupo_id}", response_model=models.Cupo)
async def read_cupo(cupo_id: int, session: SessionDep):
    controller = BaseCrudService(models.Cupo)
    try:
        db_cupo = controller.read(session, cupo_id)
        return db_cupo
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/cupos", response_model=list[models.Cupo])
async def read_all_cupos(session: SessionDep):
    controller = BaseCrudService(models.Cupo)
    try:
        cupos = controller.all(session)
        return cupos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/cupos/{cupo_id}", response_model=models.Cupo)
async def update_cupo(cupo_id: int, cupo: models.CupoBase, session: SessionDep):
    controller = BaseCrudService(models.Cupo)
    try:
        updated_cupo = controller.update(session, cupo_id, cupo)
        return updated_cupo
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/cupos/{cupo_id}")
async def delete_cupo(cupo_id: int, session: SessionDep):
    controller = BaseCrudService(models.Cupo)
    try:
        result = controller.delete(session, cupo_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
## Ficha Routes
# CRUD operations for Ficha model
@router.post("/fichas", response_model=models.Ficha)
async def create_ficha(session: SessionDep, ficha: models.FichaBase):
    controller = BaseCrudService(models.Ficha)
    try:
        db_ficha = controller.create(session, ficha)
        return db_ficha
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/fichas/{ficha_id}", response_model=models.Ficha)
async def read_ficha(ficha_id: int, session: SessionDep):
    controller = BaseCrudService(models.Ficha)
    try:
        db_ficha = controller.read(session, ficha_id)
        return db_ficha
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/fichas", response_model=list[models.Ficha])
async def read_all_fichas(session: SessionDep):
    controller = BaseCrudService(models.Ficha)
    try:
        fichas = controller.all(session)
        return fichas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/fichas/{ficha_id}", response_model=models.Ficha)
async def update_ficha(ficha_id: int, ficha: models.FichaBase, session: SessionDep):
    controller = BaseCrudService(models.Ficha)
    try:
        updated_ficha = controller.update(session, ficha_id, ficha)
        return updated_ficha
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/fichas/{ficha_id}")
async def delete_ficha(ficha_id: int, session: SessionDep):
    controller = BaseCrudService(models.Ficha)
    try:
        result = controller.delete(session, ficha_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
