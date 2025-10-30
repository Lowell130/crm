from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOWED_ORIGINS
from .routers import auth as auth_router
from .routers import customers as customers_router
from .indexes import ensure_indexes
from .db import db
from app.routers import invoices as invoices_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_indexes()
    yield

app = FastAPI(title="CRM Backend", version="0.1.1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
     expose_headers=["X-Total-Count"],  # <— IMPORTANTE
)

app.include_router(auth_router.router)
app.include_router(customers_router.router)
app.include_router(invoices_router.router)

# ✅ Root "alive"
@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": "crm-backend"}

# ✅ Health più completo (ping a Mongo)
@app.get("/health", tags=["health"])
async def health():
    try:
        await db.command("ping")
        return {"status": "ok", "db": "ok"}
    except Exception as e:
        return {"status": "degraded", "db": f"error: {type(e).__name__}"}
