from twilio.rest import Client
from ..core.config import settings

def send_whatsapp(to_e164: str, body: str):
    if not (settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_whatsapp_from):
        raise RuntimeError("Twilio not configured")
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    message = client.messages.create(
        from_=settings.twilio_whatsapp_from,
        to=f"whatsapp:{to_e164}" if not to_e164.startswith("whatsapp:") else to_e164,
        body=body,
    )
    return {"sid": message.sid}
