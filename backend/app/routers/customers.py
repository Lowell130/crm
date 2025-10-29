from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from ..db import customers_col
from ..models import CustomerCreate, CustomerUpdate, CustomerPublic
from ..auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

def _to_public(doc) -> CustomerPublic:
    doc["_id"] = str(doc["_id"])
    return CustomerPublic(**doc)

@router.post("", response_model=CustomerPublic, status_code=201)
async def create_customer(payload: CustomerCreate, user=Depends(get_current_user)):
    doc = payload.model_dump(exclude_none=True)
    try:
        res = await customers_col.insert_one(doc)
    except DuplicateKeyError as e:
        msg = "Valore duplicato su campo unico"
        if "uniq_b2b_vat" in str(e):
            msg = "P.IVA già presente (B2B)."
        if "uniq_b2c_codice_fiscale" in str(e):
            msg = "Codice Fiscale già presente (B2C)."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    created = await customers_col.find_one({"_id": res.inserted_id})
    return _to_public(created)

@router.get("", response_model=list[CustomerPublic])
async def list_customers(
    response: Response,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    kind: str | None = Query(None, pattern="^(B2B|B2C)$"),
    q: str | None = Query(None),
    user=Depends(get_current_user),
):
    # filtro coerente con UI
    filt: dict = {}
    if kind:
        filt["kind"] = kind
    if q:
        filt["$or"] = [
            {"company_name":   {"$regex": q, "$options": "i"}},
            {"first_name":     {"$regex": q, "$options": "i"}},
            {"last_name":      {"$regex": q, "$options": "i"}},
            {"email":          {"$regex": q, "$options": "i"}},
            {"vat_number":     {"$regex": q, "$options": "i"}},
            {"codice_fiscale": {"$regex": q, "$options": "i"}},
        ]

    total = await customers_col.count_documents(filt)
    cursor = customers_col.find(filt).skip(skip).limit(limit).sort("_id", -1)

    results: list[CustomerPublic] = []
    async for doc in cursor:
        results.append(_to_public(doc))

    # header con il totale (assicurati di esporlo in CORS: expose_headers=["X-Total-Count"])
    response.headers["X-Total-Count"] = str(total)
    return results

@router.get("/{customer_id}", response_model=CustomerPublic)
async def get_customer(customer_id: str, user=Depends(get_current_user)):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    doc = await customers_col.find_one({"_id": ObjectId(customer_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return _to_public(doc)

@router.put("/{customer_id}", response_model=CustomerPublic)
async def update_customer(customer_id: str, payload: CustomerUpdate, user=Depends(get_current_user)):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    update_doc = {"$set": payload.model_dump(exclude_none=True)}
    try:
        res = await customers_col.update_one({"_id": ObjectId(customer_id)}, update_doc)
    except DuplicateKeyError as e:
        msg = "Valore duplicato su campo unico"
        if "uniq_b2b_vat" in str(e):
            msg = "P.IVA già presente (B2B)."
        if "uniq_b2c_codice_fiscale" in str(e):
            msg = "Codice Fiscale già presente (B2C)."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    doc = await customers_col.find_one({"_id": ObjectId(customer_id)})
    return _to_public(doc)

@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, user=Depends(get_current_user)):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await customers_col.delete_one({"_id": ObjectId(customer_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return
