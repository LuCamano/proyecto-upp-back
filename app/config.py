from fastapi_mail import ConnectionConfig
import os

# Obtener la ruta del directorio de templates relativa al archivo actual: ../templates
template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')

CON_CONFIG = ConnectionConfig(
    MAIL_USERNAME=os.getenv('SMTP_USER'),
    MAIL_PASSWORD=os.getenv('SMTP_PASSWORD'),
    MAIL_FROM_NAME="Unidad de Prácticas Pedagógicas",
    MAIL_FROM=os.getenv('SMTP_USER'),
    MAIL_PORT=587,
    MAIL_SERVER='smtp.office365.com',
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=template_dir,
)