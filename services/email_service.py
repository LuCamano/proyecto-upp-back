from typing import List, Dict, Optional
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlmodel import select
from pydantic import BaseModel, EmailStr
from app.config import CON_CONFIG
from app.db import SessionDep
from models import Directivo, Establecimiento, Ficha, Estudiante
from uuid import UUID
from app.scheduler import scheduler
from datetime import datetime, timezone, date

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
    semana_inicio: str
    semana_termino: str

class StablishmentBody(BaseModel):
    directivo: Optional[Directivo]
    establecimiento: Optional[Establecimiento]
    semana_inicio_profesional: str
    semana_termino_profesional: str
    numero_semanas_profesional: int
    semana_inicio_pp: str
    semana_termino_pp: str
    numero_semanas_pp: int
    fichas: List[Ficha]

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
        nivel_practica=ficha.cupo.nivel_practica.nombre,
        semana_inicio=ficha.fecha_inicio.strftime("%d-%B") if hasattr(ficha, 'fecha_inicio') and ficha.fecha_inicio else str(ficha.fecha_inicio) if ficha.fecha_inicio else '',
        semana_termino=ficha.fecha_termino.strftime("%d-%B") if hasattr(ficha, 'fecha_termino') and ficha.fecha_termino else str(ficha.fecha_termino) if ficha.fecha_termino else ''
    )
    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=body.model_dump(),
        subtype=MessageType.html
    )
    fm = FastMail(CON_CONFIG)
    # Programar el envío usando APScheduler
    def send_mail_job():
        import asyncio
        try:
            asyncio.run(fm.send_message(message, template_name="plantilla estudiante.html"))
        except Exception as e:
            print(f"[APScheduler] Error al enviar correo a {email.email}: {e}")
    # Convertir fecha_envio a datetime UTC si es necesario
    run_date = ficha.fecha_envio
    if isinstance(run_date, str):
        run_date = datetime.fromisoformat(run_date)
    if run_date.tzinfo is None:
        run_date = run_date.replace(tzinfo=timezone.utc)
    else:
        run_date = run_date.astimezone(timezone.utc)
    scheduler.add_job(send_mail_job, 'date', run_date=run_date)
    # Opcional: retornar información de la programación
    return {"status": "scheduled", "run_date": str(run_date)}

async def send_stablishment_email(session: SessionDep, email: EmailSchema, body: StablishmentBody, establecimiento_id: UUID):
    body.establecimiento = session.exec(select(Establecimiento).where(Establecimiento.id == establecimiento_id)).first()
    if not body.establecimiento:
        raise ValueError("No se encontró el establecimiento con el ID proporcionado.")
    if not body.directivo:
        body.directivo = body.establecimiento.directivos[0] if body.establecimiento.directivos else None
    if not body.directivo:
        raise ValueError("No se encontró un directivo asociado al establecimiento.")
    fichas = body.fichas or session.exec(select(Ficha).where(Ficha.establecimiento_id == establecimiento_id)).all()
    data = body.model_dump()
    data["fichas"] = []
    for f in fichas:
        fichaData = f.model_dump()
        fichaData["estudiante"] = session.exec(select(Estudiante).where(Estudiante.id == f.estudiante_id)).first().model_dump()
        fichaData["fecha_inicio"] = date.fromisoformat(f.fecha_inicio).strftime("%d-%B") if f.fecha_inicio else ''
        fichaData["fecha_termino"] = date.fromisoformat(f.fecha_termino).strftime("%d-%B") if f.fecha_termino else ''
        data["fichas"].append(fichaData)

    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=data,
        subtype=MessageType.html
    )
    
    fm = FastMail(CON_CONFIG)
    await fm.send_message(message, template_name="plantilla colegio.html")