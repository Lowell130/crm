from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expires_min)
    payload = {"sub": subject, "exp": expire}
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    return token

def decode_token(token: str):
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
