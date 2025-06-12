from sqlmodel import delete
from app.db import SessionDep
from models import (
    Ficha,
    Estudiante,
    Cupo,
    NivelPractica,
    Establecimiento,
    Carrera,
    Tutor,
    Directivo,
    Comuna
)

MODELOS = [
    Ficha,
    Estudiante,
    Cupo,
    NivelPractica,
    Establecimiento,
    Carrera,
    Tutor,
    Directivo,
    Comuna
]

def clear_db(session: SessionDep):
    """
    Clear all data from the database.
    
    Args:
        session (SessionDep): Database session dependency.
    
    Returns:
        dict: A message indicating the result of the operation.
    """
    try:
        for modelo in MODELOS:
            session.exec(delete(modelo))
        session.commit()
        return {"message": "Database cleared successfully."}
    except Exception as e:
        session.rollback()
        raise ValueError(f"An error occurred while clearing the database: {e}")