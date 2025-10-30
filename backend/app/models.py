# app/models.py
from typing import Optional, Literal
from pydantic import BaseModel, Field, EmailStr, model_validator

# ---------- USERS ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: str = Field(..., alias="_id")
    email: EmailStr

# ---------- AUTH ----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# ---------- CUSTOMERS ----------
class CustomerBase(BaseModel):
    kind: Literal["B2B", "B2C"] = "B2C"
    # comuni
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    # B2C
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    codice_fiscale: Optional[str] = None
    # B2B
    company_name: Optional[str] = None
    vat_number: Optional[str] = None  # P.IVA

    @model_validator(mode="after")
    def validate_by_kind(self):
        if self.kind == "B2B":
            if not self.company_name:
                raise ValueError("Per B2B è richiesto 'company_name'.")
            if not self.vat_number:
                raise ValueError("Per B2B è richiesto 'vat_number'.")
        if self.kind == "B2C":
            if not self.first_name or not self.last_name:
                raise ValueError("Per B2C sono richiesti 'first_name' e 'last_name'.")
            if not self.codice_fiscale:
                raise ValueError("Per B2C è richiesto 'codice_fiscale'.")
        return self

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    @model_validator(mode="after")
    def validate_update(self):
        return super().validate_by_kind() if self.kind else self

class CustomerPublic(CustomerBase):
    id: str = Field(..., alias="_id")


# --- FATTURE ---

from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import date
from bson import ObjectId

class InvoiceItem(BaseModel):
    description: str = Field(..., min_length=1, max_length=300)
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    vat_rate: float = Field(0, ge=0)  # es. 22 per 22%

    @property
    def net_amount(self) -> float:
        return round(self.quantity * self.unit_price, 2)

    @property
    def vat_amount(self) -> float:
        return round(self.net_amount * (self.vat_rate / 100.0), 2)

    @property
    def gross_amount(self) -> float:
        return round(self.net_amount + self.vat_amount, 2)

class InvoiceBase(BaseModel):
    customer_id: str  # ObjectId as str
    issue_date: date
    due_date: Optional[date] = None
    notes: Optional[str] = None
    items: List[InvoiceItem] = Field(..., min_items=1)
    # numero fattura: se non impostato, viene autogenerato
    number: Optional[str] = None
    status: str = Field("draft", pattern="^(draft|issued|cancelled)$")

    @validator("customer_id")
    def validate_object_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("customer_id non è un ObjectId valido")
        return v

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None
    items: Optional[List[InvoiceItem]] = None
    number: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(draft|issued|cancelled)$")

class InvoiceDB(InvoiceBase):
    id: str
    # totali calcolati lato server
    subtotal: float
    vat_total: float
    total: float

class InvoiceOut(InvoiceDB):
    customer_snapshot: dict | None = None  # opzionale: anagrafica memorizzata al momento della fattura
