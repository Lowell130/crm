from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pathlib import Path
from ...models.customer import Customer
from ..deps import get_current_admin
import uuid

router = APIRouter()
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/customers/{customer_id}/files")
async def upload_file(customer_id: str, file: UploadFile = File(...), admin=Depends(get_current_admin)):
    doc = await Customer.get(customer_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Customer not found")
    ext = Path(file.filename).suffix
    fname = f"{uuid.uuid4().hex}{ext}"
    path = UPLOAD_DIR / fname
    content = await file.read()
    path.write_bytes(content)
    doc.files.append(fname)
    await doc.save()
    return {"filename": fname}

@router.get("/customers/{customer_id}/files")
async def list_files(customer_id: str, admin=Depends(get_current_admin)):
    doc = await Customer.get(customer_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"files": doc.files}
