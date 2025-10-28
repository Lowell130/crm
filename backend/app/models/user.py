from beanie import Document, Indexed
from typing import Literal
from datetime import datetime

class User(Document):
    email: Indexed(str, unique=True)  # indice unico
    password_hash: str
    role: Literal["admin", "operator"] = "admin"
    is_active: bool = True
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "users"
