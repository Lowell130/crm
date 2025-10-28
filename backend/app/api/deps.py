from fastapi import Header, HTTPException, status, Depends
from typing import Optional
from ..core.security import decode_token
from ..core.config import settings

async def get_current_admin(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_token(token)
        if payload.get("sub") != settings.admin_email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid subject")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"email": settings.admin_email}
