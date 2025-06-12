from fastapi import UploadFile
import pandas as pd
from app.db import SessionDep
from services import BaseCrudService, DirectivoService, EstudianteService, NivelPracticaService, EstablecimientoService
from services.clearDBService import clear_db
from models import (Comuna, Tutor, Carrera)

SHEETS: list[tuple[str, BaseCrudService]] = [("Comunas", BaseCrudService(Comuna)), ("Establecimientos", EstablecimientoService()), ("Tutores", BaseCrudService(Tutor)), ("Carreras", BaseCrudService(Carrera)), ("Niveles de practica", NivelPracticaService()), ("Estudiantes", EstudianteService()), ("Directivos", DirectivoService())]

def process_excel(file: UploadFile, session: SessionDep):
    """
    Process an Excel file and return a DataFrame.
    
    Args:
        file (UploadFile): The uploaded Excel file.
        session (SessionDep): Database session dependency.
    """
    xls = pd.ExcelFile(file.file)

    try:
        for sheetName, service in SHEETS:
            if sheetName not in xls.sheet_names:
                raise ValueError(f"Sheet '{sheetName}' not found in the uploaded file.")
            df = pd.read_excel(xls, sheet_name=sheetName)
            df.columns = [col.lower() for col in df.columns]  # Normalize column names to lowercase
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)  # Le aplica trim a todos los campos string
            df = df.fillna("")  # Fill NaN values with empty strings
            if "rbd" in df.columns:
                df["rbd"] = df["rbd"].astype(str)
            service.bulk_create(session, df.to_dict(orient="records"))
        return {"message": "Data processed successfully."}
    except Exception as e:
        session.rollback()
        raise ValueError(f"An error occurred while processing the file: {e}")
    
def vaciado_db(session: SessionDep):
    try:
        # Call the delete_all method for each service
        clear_db(session)
        return {"message": "Database cleared successfully."}
    except Exception as e:
        session.rollback()
        raise ValueError(f"An error occurred while clearing the database: {e}")