# backend/app/services/email_service.py
from typing import List
from email.message import EmailMessage
import aiosmtplib

from ..core.config import settings

def _ensure_email_config():
    if not settings.email_host or not settings.email_port:
        raise RuntimeError("Email not configured: EMAIL_HOST/EMAIL_PORT are missing")
    if not settings.email_user or not settings.email_pass:
        raise RuntimeError("Email not configured: EMAIL_USER/EMAIL_PASS are missing")

def _build_message(subject: str, recipients: List[str], body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.email_user
    msg["To"] = ", ".join(recipients)
    # Proviamo HTML, se vuoi fai una versione text/plain alternativa
    msg.set_content(body, subtype="html")
    return msg

async def send_email(subject: str, recipients: List[str], body: str):
    """
    Invio email via SMTP con STARTTLS usando aiosmtplib (compatibile con Gmail).
    """
    _ensure_email_config()
    if not recipients:
        raise RuntimeError("No recipients")

    msg = _build_message(subject, recipients, body)

    # Connessione SMTP (STARTTLS)
    # Gmail: host=smtp.gmail.com, port=587
    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.email_host,
            port=settings.email_port,
            start_tls=True,
            username=settings.email_user,
            password=settings.email_pass,
            timeout=30,
        )
    except Exception as e:
        raise RuntimeError(f"SMTP send failed: {e}")
