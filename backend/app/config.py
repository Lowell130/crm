import os, json
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
MONGO_DB = os.getenv("MONGO_DB", "crm")

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-please")
JWT_EXPIRES_MIN = int(os.getenv("JWT_EXPIRES_MIN", "60"))
JWT_ALGORITHM = "HS256"
JWT_EXPIRES_DELTA = timedelta(minutes=JWT_EXPIRES_MIN)

# ALLOWED_ORIGINS come stringa JSON nell'.env
try:
    ALLOWED_ORIGINS = json.loads(os.getenv("ALLOWED_ORIGINS", "[]"))
    if not isinstance(ALLOWED_ORIGINS, list):
        ALLOWED_ORIGINS = []
except Exception:
    ALLOWED_ORIGINS = []
