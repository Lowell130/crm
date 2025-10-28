# backend/app/schemas/auth.py
from pydantic import BaseModel, field_validator

class LoginInput(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        # accetta anche domini special-use (.local, localhost, ecc.), fai solo sanità minima
        v = (v or "").strip()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError("invalid email-like string")
        return v.lower()

class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"
