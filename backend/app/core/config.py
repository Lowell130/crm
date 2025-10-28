from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Any

class Settings(BaseSettings):
    # Mongo
    mongo_uri: str = Field(alias="MONGO_URI")
    mongo_db: str = Field(default="crm", alias="MONGO_DB")  # fallback se la URI non contiene il DB

    # Auth
    jwt_secret: str = Field(alias="JWT_SECRET")
    jwt_expires_min: int = Field(default=60, alias="JWT_EXPIRES_MIN")

    # CORS
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        alias="ALLOWED_ORIGINS",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, v: Any):
        """
        Accetta sia JSON (p.es. '["http://a","http://b"]') sia CSV (p.es. http://a,http://b).
        """
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):  # JSON
                import json
                try:
                    return json.loads(s)
                except Exception:
                    pass
            # CSV
            return [p.strip().strip('"').strip("'") for p in s.split(",") if p.strip()]
        return v

    # Bootstrap admin (solo per test iniziali)
    admin_email: str = Field(alias="ADMIN_EMAIL", default="admin@mycrm.local")
    admin_password: str = Field(alias="ADMIN_PASSWORD", default="admin12345")

    # Email (opzionale)
    email_host: str = Field(alias="EMAIL_HOST", default="smtp.gmail.com")
    email_port: int = Field(alias="EMAIL_PORT", default=587)
    email_user: str = Field(alias="EMAIL_USER", default="")
    email_pass: str = Field(alias="EMAIL_PASS", default="")

    # Twilio (opzionale)
    twilio_account_sid: str = Field(alias="TWILIO_ACCOUNT_SID", default="")
    twilio_auth_token: str = Field(alias="TWILIO_AUTH_TOKEN", default="")
    twilio_whatsapp_from: str = Field(alias="TWILIO_WHATSAPP_FROM", default="")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

settings = Settings()
