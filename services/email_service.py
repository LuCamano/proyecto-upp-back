import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.office365.com'
SMTP_PORT = 587
SMTP_USER = 'upp@ucsc.cl'
SMTP_PASSWORD = 'EquipoUnidad8'

def send_emails(subject, messages):
    print(f'Enviando correos a: {[msg["email"] for msg in messages]}')

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)

        for msg in messages:
            print(f'Enviando a: {msg["email"]}')

            email_msg = MIMEMultipart('alternative')
            email_msg['From'] = SMTP_USER
            email_msg['To'] = msg['email']
            email_msg['Subject'] = subject

            html_part = MIMEText(msg['html'], 'html')
            email_msg.attach(html_part)

            server.sendmail(SMTP_USER, msg['email'], email_msg.as_string())

            print(f'Correo enviado a: {msg["email"]}')
