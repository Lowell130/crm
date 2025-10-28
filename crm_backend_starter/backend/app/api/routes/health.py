from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["meta"])
async def health():
    return {"status": "ok"}
