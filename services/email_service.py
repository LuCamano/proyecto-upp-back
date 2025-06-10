from typing import List, Dict
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from app.config import CON_CONFIG
from app.db import SessionDep
from models import Ficha

class EmailSchema(BaseModel):
    subject: str
    email: List[EmailStr]

class StudentBody(BaseModel):
    estudiante: Dict[str, str] = {
        "nombre": str,
        "ap_paterno": str,
        "ap_materno": str
    }
    directivo: Dict[str, str] = {
        "nombre": str,
        "cargo": str,
        "email": str
    }
    nombre_establecimiento: str
    nivel_practica: str

class StablishmentBody(BaseModel):
    pass

# async def send_emails(email: EmailSchema):
#     message = MessageSchema(
#         subject=email.subject,  # Subject of the email
#         recipients=email.email,  # List of email addresses
#         template_body=email.body.model_dump(),
#         subtype=MessageType.html
#     )
    
#     fm = FastMail(CON_CONFIG)
#     await fm.send_message(message, template_name="plantilla estudiante.html")
    
async def send_student_email(session: SessionDep, email: EmailSchema, ficha_id: int):
    ficha = session.get(Ficha, ficha_id)
    if not ficha:
        raise ValueError("No se encontró la ficha con el ID proporcionado.")
    body = StudentBody(
        estudiante={
            "nombre": ficha.estudiante.nombre,
            "ap_paterno": ficha.estudiante.ap_paterno,
            "ap_materno": ficha.estudiante.ap_materno
        },
        directivo={
            "nombre": ficha.establecimiento.directivos[0].nombre,
            "cargo": ficha.establecimiento.directivos[0].cargo,
            "email": ficha.establecimiento.directivos[0].email
        },
        nombre_establecimiento=ficha.establecimiento.nombre,
        nivel_practica=ficha.cupo.nivel_practica.nombre
    )
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=body.model_dump(),
        subtype=MessageType.html
    )
    
    fm = FastMail(CON_CONFIG)
    await fm.send_message(message, template_name="plantilla estudiante.html")

async def send_stablishment_email(email: EmailSchema, body: StablishmentBody):
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=body.model_dump(),
        subtype=MessageType.html
    )
    
    fm = FastMail(CON_CONFIG)
    await fm.send_message(message, template_name="plantilla colegio.html")