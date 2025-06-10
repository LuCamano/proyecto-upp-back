import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from services.email_service import send_emails, EmailSchema

router = APIRouter()

@router.post("/send-email")
async def send_emails_route(email: EmailSchema):
    try:
        await send_emails(email)
        return JSONResponse(status_code=200, content="Correos enviados correctamente")
    except Exception as e:
        logging.error(f'Error al enviar correos: {e}')
        raise HTTPException(status_code=500, detail="Error al enviar correos", headers={"X-Error": str(e)})