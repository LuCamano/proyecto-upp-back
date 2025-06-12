from app.config import template_dir
import os

def get_student_email_template():
    """
    Get the email template for students.
    """
    with open(os.path.join(template_dir, "plantilla estudiante.html"), "r", encoding="utf-8") as f:
        return f.read()

def get_stablishment_email_template():
    """
    Get the email template for establishments.
    """
    with open(os.path.join(template_dir, "plantilla colegio.html"), "r", encoding="utf-8") as f:
        return f.read()

async def set_student_email_template(html: str):
    """
    Set the email template for students.
    """
    with open(os.path.join(template_dir, "plantilla estudiante.html"), "wt", encoding="utf-8") as f:
        f.write(html)

async def set_stablishment_email_template(html: str):
    """
    Set the email template for establishments.
    """
    with open(os.path.join(template_dir, "plantilla colegio.html"), "wt", encoding="utf-8") as f:
        f.write(html)