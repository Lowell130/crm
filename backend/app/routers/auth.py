from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr
from ..db import users_col
from ..models import UserCreate, TokenResponse, LoginRequest
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
async def register(payload: UserCreate):
    existing = await users_col.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    doc = {"email": str(payload.email), "password": hash_password(payload.password)}
    await users_col.insert_one(doc)
    return {"message": "User registered"}

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await users_col.find_one({"email": str(payload.email)})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user["email"])
    return {"access_token": token, "token_type": "bearer"}
