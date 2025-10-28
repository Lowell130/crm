from beanie import Document, Indexed
from typing import Optional, List, Literal
from datetime import datetime

class Customer(Document):
    # Common fields
    name: str
    email: Optional[Indexed(str, unique=False)] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    customer_type: Literal["B2C", "B2B"] = "B2C"
    vat_or_tax_id: Optional[str] = None  # Partita IVA o Codice fiscale
    registered_at: datetime = datetime.utcnow()
    tags: List[str] = []
    notes: Optional[str] = None
    # Store file metadata (filenames/URLs) if needed
    files: List[str] = []
    is_active: bool = True

    class Settings:
        name = "customers"

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mario Rossi",
                "email": "mario.rossi@example.com",
                "phone": "+390612345678",
                "address": "Via Roma 1, 00100 Roma",
                "customer_type": "B2C",
                "vat_or_tax_id": "RSSMRA80A01H501U",
                "tags": ["vip", "newsletter"],
                "notes": "Cliente interessato a upsell",
            }
        }
