from typing import List, Dict
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlmodel import select
from pydantic import BaseModel, EmailStr
from app.config import CON_CONFIG
from app.db import SessionDep
from models import Directivo, Ficha
from uuid import UUID

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
    directivo: Directivo = None
    semana_inicio_profesional: str
    semana_termino_profesional: str
    numero_semanas_profesional: int
    semana_inicio_pp: str
    semana_termino_pp: str
    numero_semanas_pp: int
    fichas: List[Ficha] = None

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

async def send_stablishment_email(session: SessionDep, email: EmailSchema, body: StablishmentBody, establecimiento_id: UUID):
    fichas = session.exec(select(Ficha).where(Ficha.establecimiento_id == establecimiento_id)).all()
    body.directivo = session.exec(select(Directivo).where(Directivo.establecimiento_id == establecimiento_id)).first()
    data = body.model_dump()
    data["fichas"] = []
    for f in fichas:
        fichaData = f.model_dump()
        fichaData["estudiante"] = f.estudiante.model_dump()
        data["fichas"].append(fichaData)
    
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=data,
        subtype=MessageType.html
    )
    
    fm = FastMail(CON_CONFIG)
    await fm.send_message(message, template_name="plantilla colegio.html")