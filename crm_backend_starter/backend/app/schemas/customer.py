from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Literal
from datetime import datetime

class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    customer_type: Literal["B2C", "B2B"] = "B2C"
    vat_or_tax_id: Optional[str] = None
    tags: List[str] = []
    notes: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    customer_type: Optional[Literal["B2C", "B2B"]] = None
    vat_or_tax_id: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class CustomerOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    customer_type: Literal["B2C", "B2B"]
    vat_or_tax_id: Optional[str] = None
    registered_at: datetime
    tags: List[str] = []
    notes: Optional[str] = None
    files: List[str] = []
    is_active: bool
