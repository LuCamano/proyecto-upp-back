import logging
from uuid import UUID
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from app.db import SessionDep
from services.email_service import EmailSchema, StablishmentBody, send_student_email, send_stablishment_email
from controllers.PlantillasCorreos import get_stablishment_email_template, get_student_email_template, set_student_email_template, set_stablishment_email_template

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
    try:
        await send_stablishment_email(session, email, body, establecimiento_id)
        return JSONResponse(status_code=200, content={"message": "Email sent successfully"})
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
    
@router.get("/email-template/student", response_class=HTMLResponse)
async def get_student_email_template_route():
    try:
        template = get_student_email_template()
        return template
    except Exception as e:
        logging.error(f"Error retrieving student email template: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve email template")
    
@router.get("/email-template/stablishment", response_class=HTMLResponse)
async def get_stablishment_email_template_route():
    try:
        template = get_stablishment_email_template()
        return template
    except Exception as e:
        logging.error(f"Error retrieving stablishment email template: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve email template")
    
@router.post("/email-template/student")
async def set_student_email_template_route(html: str):
    try:
        await set_student_email_template(html)
        return JSONResponse(status_code=200, content={"message": "Student email template updated successfully"})
    except Exception as e:
        logging.error(f"Error updating student email template: {e}")
        raise HTTPException(status_code=500, detail="Failed to update email template")
    
@router.post("/email-template/stablishment")
async def set_stablishment_email_template_route(html: str):
    try:
        await set_stablishment_email_template(html)
        return JSONResponse(status_code=200, content={"message": "Stablishment email template updated successfully"})
    except Exception as e:
        logging.error(f"Error updating stablishment email template: {e}")
        raise HTTPException(status_code=500, detail="Failed to update email template")