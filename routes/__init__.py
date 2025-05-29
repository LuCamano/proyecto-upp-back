from fastapi import APIRouter, HTTPException

router = APIRouter()

## Rutas de prueba para poder ejecutar la creacion de las tablas y la base de datos
from app.db import SessionDep
import models
@router.post("/comunas", response_model=models.Comuna)
async def create_comuna(session: SessionDep, comuna: models.ComunaBase):
    db_comuna = models.Comuna.model_validate(comuna)
    session.add(db_comuna)
    session.commit()
    session.refresh(db_comuna)
    return db_comuna

@router.get("/comunas/{comuna_id}", response_model=models.Comuna)
async def read_comuna(comuna_id: int, session: SessionDep):
    comuna = session.get(models.Comuna, comuna_id)
    if not comuna:
        raise HTTPException(status_code=404, detail="Comuna not found")
    return comuna