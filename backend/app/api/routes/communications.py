from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from ..deps import get_current_admin
from ...services.email_service import send_email
from ...services.whatsapp_service import send_whatsapp
from ...models.customer import Customer

router = APIRouter()

class EmailPayload(BaseModel):
    subject: str
    body: str  # html/text
    recipients: Optional[List[EmailStr]] = None     # destinatari diretti
    customer_ids: Optional[List[str]] = None        # oppure prendi email dai clienti

@router.post("/communications/email")
async def send_email_to_customers(payload: EmailPayload, admin=Depends(get_current_admin)):
    recipients: List[str] = payload.recipients or []
    if payload.customer_ids:
        docs = await Customer.find({"_id": {"$in": payload.customer_ids}}).to_list()
        recipients.extend([c.email for c in docs if c.email])

    # deduplica e valida
    recipients = sorted({r for r in recipients if r})
    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients")

    await send_email(subject=payload.subject, recipients=recipients, body=payload.body)
    return {"sent": len(recipients)}

class WhatsappPayload(BaseModel):
    to_e164: str   # es. +393331234567
    body: str

@router.post("/communications/whatsapp")
def send_whatsapp_message(payload: WhatsappPayload, admin=Depends(get_current_admin)):
    try:
        res = send_whatsapp(to_e164=payload.to_e164, body=payload.body)
        return {"sid": res["sid"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
