from fastapi import APIRouter, HTTPException
from app.services.email_service import send_emails

router = APIRouter()

@router.post("/send-email")
async def send_email_route(payload: dict):
    subject = payload.get('subject')
    messages = payload.get('messages')

    try:
        send_emails(subject, messages)
        return {"message": "Correos enviados correctamente"}
    except Exception as e:
        print(f'Error al enviar correos: {e}')
        raise HTTPException(status_code=500, detail="Error al enviar correos")
