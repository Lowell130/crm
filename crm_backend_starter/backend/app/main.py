from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .db import init_beanie
from .api.routes import health, auth, customers, files, stats

app = FastAPI(title="CRM API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_beanie()

# Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(customers.router, prefix="/api/v1", tags=["customers"])
app.include_router(files.router, prefix="/api/v1", tags=["files"])
app.include_router(stats.router, prefix="/api/v1", tags=["stats"])
