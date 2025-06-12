import logging
from uuid import UUID
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.db import SessionDep
from services.email_service import EmailSchema, StablishmentBody, send_student_email, send_stablishment_email

router = APIRouter()

@router.post("/send-email/student")
async def send_email_student(session: SessionDep, email: EmailSchema, ficha_id: int):
    try:
        await send_student_email(session, email, ficha_id)
        return JSONResponse(status_code=200, content={"message": "Email sent successfully"})
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")
    
@router.post("/send-email/stablishment")
async def send_email_stablishment(session: SessionDep, email: EmailSchema, body: StablishmentBody, establecimiento_id: UUID):
    await send_stablishment_email(session, email, body, establecimiento_id)
    return JSONResponse(status_code=200, content={"message": "Email sent successfully"})
    # try:
    #     await send_stablishment_email(session, email, body, establecimiento_id)
    #     return JSONResponse(status_code=200, content={"message": "Email sent successfully"})
    # except Exception as e:
    #     logging.error(f"Error sending email: {e}")
    #     raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")