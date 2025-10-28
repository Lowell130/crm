from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    mongo_uri: str = Field(alias="MONGO_URI")
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_expires_min: int = Field(default=60, alias="JWT_EXPIRES_MIN")
    allowed_origins: List[str] = Field(default_factory=lambda: ["http://localhost:3000"] , alias="ALLOWED_ORIGINS")

    # bootstrap admin (for initial testing)
    admin_email: str = Field(alias="ADMIN_EMAIL", default="admin@mycrm.local")
    admin_password: str = Field(alias="ADMIN_PASSWORD", default="admin12345")

    # Email
    email_host: str = Field(alias="EMAIL_HOST", default="smtp.gmail.com")
    email_port: int = Field(alias="EMAIL_PORT", default=587)
    email_user: str = Field(alias="EMAIL_USER", default="")
    email_pass: str = Field(alias="EMAIL_PASS", default="")

    # Twilio
    twilio_account_sid: str = Field(alias="TWILIO_ACCOUNT_SID", default="")
    twilio_auth_token: str = Field(alias="TWILIO_AUTH_TOKEN", default="")
    twilio_whatsapp_from: str = Field(alias="TWILIO_WHATSAPP_FROM", default="")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False
    }

settings = Settings()
