from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from ..core.config import settings
from typing import List

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_user,
    MAIL_PASSWORD=settings.email_pass,
    MAIL_FROM=settings.email_user,
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_host,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

async def send_email(subject: str, recipients: List[str], body: str):
    message = MessageSchema(subject=subject, recipients=recipients, body=body, subtype="html")
    fm = FastMail(conf)
    await fm.send_message(message)
