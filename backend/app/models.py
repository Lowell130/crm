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
