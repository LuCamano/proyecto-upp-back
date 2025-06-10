import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.db import SessionDep
from services.email_service import EmailSchema, send_student_email

router = APIRouter()

@router.post("/send-email/student")
async def send_email_student(session: SessionDep, email: EmailSchema, ficha_id: int):
    await send_student_email(session, email, ficha_id)
    return JSONResponse(status_code=200, content={"message": "Email sent successfully"})
    # try:
    # except Exception as e:
    #     logging.error(f"Error sending email: {e}")
    #     raise HTTPException(status_code=500, detail="Failed to send email") from e