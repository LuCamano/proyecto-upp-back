from typing import List, Dict, Optional
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlmodel import select
from pydantic import BaseModel, EmailStr
from fastapi import HTTPException
from app.config import CON_CONFIG
from app.db import SessionDep
from models import Directivo, Establecimiento, Ficha, Estudiante, Carrera, Cupo, NivelPractica
from uuid import UUID
from app.scheduler import scheduler
from datetime import datetime, timezone


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


def _format_fecha(fecha) -> str:
    if not fecha:
        return ""
    try:
        return fecha.strftime("%d de %B, %Y")
    except Exception:
        return str(fecha)


def _resolve_carrera_nombre(session: SessionDep, estudiante: Estudiante) -> str:
    try:
        if hasattr(estudiante, "carrera") and estudiante.carrera:
            if hasattr(estudiante.carrera, "nombre"):
                return estudiante.carrera.nombre or ""
    except Exception:
        pass

    try:
        if getattr(estudiante, "carrera_id", None):
            carrera = session.get(Carrera, estudiante.carrera_id)
            if carrera and hasattr(carrera, "nombre"):
                return carrera.nombre or ""
    except Exception:
        pass

    return ""


def _resolve_nivel_practica_nombre(session: SessionDep, ficha: Ficha) -> str:
    try:
        if hasattr(ficha, "cupo") and ficha.cupo:
            if hasattr(ficha.cupo, "nivel_practica") and ficha.cupo.nivel_practica:
                if hasattr(ficha.cupo.nivel_practica, "nombre"):
                    return ficha.cupo.nivel_practica.nombre or ""
    except Exception:
        pass

    try:
        if getattr(ficha, "cupo_id", None):
            cupo = session.get(Cupo, ficha.cupo_id)
            if cupo and getattr(cupo, "nivel_practica_id", None):
                nivel = session.get(NivelPractica, cupo.nivel_practica_id)
                if nivel and hasattr(nivel, "nombre"):
                    return nivel.nombre or ""
    except Exception:
        pass

    return ""


def _build_estudiante_data_for_template(session: SessionDep, ficha: Ficha) -> Optional[Dict]:
    try:
        estudiante = ficha.estudiante if hasattr(ficha, "estudiante") else None
    except Exception:
        estudiante = None

    if not estudiante and getattr(ficha, "estudiante_id", None):
        estudiante = session.get(Estudiante, ficha.estudiante_id)

    if not estudiante:
        return None

    estudiante_data = estudiante.model_dump()
    estudiante_data["carrera"] = _resolve_carrera_nombre(session, estudiante)

    ficha_data = ficha.model_dump()
    ficha_data["estudiante"] = estudiante_data
    ficha_data["nivel_practica"] = _resolve_nivel_practica_nombre(session, ficha)
    ficha_data["fecha_inicio"] = _format_fecha(ficha.fecha_inicio)
    ficha_data["fecha_termino"] = _format_fecha(ficha.fecha_termino)

    return ficha_data


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
        semana_inicio=ficha.fecha_inicio.strftime("%d-%B") if hasattr(ficha, "fecha_inicio") and ficha.fecha_inicio else str(ficha.fecha_inicio) if ficha.fecha_inicio else "",
        semana_termino=ficha.fecha_termino.strftime("%d-%B") if hasattr(ficha, "fecha_termino") and ficha.fecha_termino else str(ficha.fecha_termino) if ficha.fecha_termino else ""
    )

    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=body.model_dump(),
        subtype=MessageType.html
    )

    fm = FastMail(CON_CONFIG)

    def send_mail_job():
        import asyncio
        import traceback
        try:
            asyncio.run(fm.send_message(message, template_name="plantilla estudiante.html"))
            print(f"[APScheduler] Correo enviado correctamente a {email.email}")
        except Exception as e:
            print(f"[APScheduler] Error al enviar correo a {email.email}: {repr(e)}")
            traceback.print_exc()

    run_date = ficha.fecha_envio
    if isinstance(run_date, str):
        run_date = datetime.fromisoformat(run_date)

    if run_date.tzinfo is None:
        run_date = run_date.replace(tzinfo=timezone.utc)
    else:
        run_date = run_date.astimezone(timezone.utc)

    scheduler.add_job(send_mail_job, "date", run_date=run_date)
    print(f"[APScheduler] Correo programado para {email.email} en {run_date}")

    return {"status": "scheduled", "run_date": str(run_date)}


async def send_stablishment_email(session: SessionDep, email: EmailSchema, body: StablishmentBody, establecimiento_id: UUID):
    body.establecimiento = session.exec(
        select(Establecimiento).where(Establecimiento.id == establecimiento_id)
    ).first()

    if not body.establecimiento:
        raise ValueError("No se encontró el establecimiento con el ID proporcionado.")

    if not body.directivo:
        body.directivo = body.establecimiento.directivos[0] if body.establecimiento.directivos else None

    if not body.directivo:
        raise ValueError("No se encontró un directivo asociado al establecimiento.")

    fichas = body.fichas or session.exec(
        select(Ficha).where(Ficha.establecimiento_id == establecimiento_id)
    ).all()

    data = body.model_dump()
    data["fichas"] = []

    for f in fichas:
        ficha_db = session.get(Ficha, f.id) if getattr(f, "id", None) else f
        if not ficha_db:
            continue

        ficha_data = _build_estudiante_data_for_template(session, ficha_db)
        if ficha_data:
            data["fichas"].append(ficha_data)

    print("DEBUG FICHAS EMAIL COLEGIO:", data["fichas"])

    message = MessageSchema(
        subject=email.subject,
        recipients=email.email,
        template_body=data,
        subtype=MessageType.html
    )

    fm = FastMail(CON_CONFIG)

    try:
        await fm.send_message(message, template_name="plantilla colegio.html")
        print(f"[EMAIL COLEGIO] Correo enviado correctamente a {email.email}")
        return {"status": "sent"}
    except Exception as e:
        import traceback
        print(f"[EMAIL COLEGIO] Error enviando a {email.email}: {repr(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error al enviar correo al establecimiento: {str(e)}"
        )