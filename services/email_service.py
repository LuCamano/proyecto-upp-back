from typing import List
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from app.config import CON_CONFIG

class EmailBody(BaseModel):
    first_name: str
    last_name: str
class EmailSchema(BaseModel):
    subject: str
    email: List[EmailStr]
    body: EmailBody
    

async def send_emails(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,  # Subject of the email
        recipients=email.email,  # List of email addresses
        template_body=email.body.model_dump(),
        subtype=MessageType.html
    )
    
    fm = FastMail(CON_CONFIG)
    await fm.send_message(message, template_name="plantilla estudiante.html")