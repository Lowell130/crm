from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal

class UserOut(BaseModel):
    id: str = Field(alias="_id")
    email: EmailStr
    role: Literal["admin", "operator"]
    is_active: bool
    created_at: datetime
