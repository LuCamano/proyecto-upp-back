from fastapi import APIRouter, UploadFile, HTTPException
from controllers.CargaMasiva import process_excel, vaciado_db
from app.db import SessionDep

router = APIRouter()

@router.post("/")
async def carga_masiva(file: UploadFile, session: SessionDep):
    """
    Endpoint to handle bulk data upload from an Excel file.
    
    Args:
        file (UploadFile): The uploaded Excel file.
        session (SessionDep): Database session dependency.
    
    Returns:
        dict: A message indicating the result of the operation.
    """
    try:
        result = process_excel(file, session)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
@router.delete("/vaciadoDB")
async def vaciar_db(session: SessionDep):
    """
    Endpoint to handle database clearing.
    """
    try:
        vaciado_db(session)
        return {"message": "Database cleared successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
