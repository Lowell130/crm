from fastapi import APIRouter, HTTPException, status
from ..deps import settings
from ...core.security import create_access_token, verify_password, hash_password
from ...schemas.auth import LoginInput, TokenOutput

router = APIRouter()

# Hash the bootstrap admin password at import (simple demo, not persisted)
_ADMIN_HASH = hash_password(settings.admin_password)

@router.post("/auth/login", response_model=TokenOutput)
async def login(payload: LoginInput):
    if payload.email.lower() != settings.admin_email.lower():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(payload.password, _ADMIN_HASH):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(settings.admin_email)
    return TokenOutput(access_token=token)
