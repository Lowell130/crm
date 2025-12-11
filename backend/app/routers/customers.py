# app/routers/customers.py
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from ..db import customers_col
from ..models import CustomerCreate, CustomerUpdate, CustomerPublic
from ..auth import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])


def _to_public(doc) -> CustomerPublic:
    # non esporre owner_id
    d = dict(doc)
    d.pop("owner_id", None)
    d["_id"] = str(d["_id"])
    return CustomerPublic(**d)


@router.get("/stats/distribution")
async def customers_distribution(user=Depends(get_current_user)):
    """
    Restituisce la distribuzione B2B/B2C per l'utente corrente:
    { "b2b": <int>, "b2c": <int>, "total": <int> }
    """
    base = {"owner_id": user["_id"]}
    b2b = await customers_col.count_documents({**base, "kind": "B2B"})
    b2c = await customers_col.count_documents({**base, "kind": "B2C"})
    return {"b2b": int(b2b), "b2c": int(b2c), "total": int(b2b + b2c)}


@router.post("", response_model=CustomerPublic, status_code=201)
async def create_customer(payload: CustomerCreate, user=Depends(get_current_user)):
    doc = payload.model_dump(exclude_none=True)
    doc["owner_id"] = user["_id"]  # 👈 associa al proprietario

    try:
        res = await customers_col.insert_one(doc)
    except DuplicateKeyError as e:
        # gestisce sia vecchi che nuovi nomi indice
        msg = "Valore duplicato su campo unico"
        se = str(e)
        if "uniq_owner_vat_b2b" in se or "uniq_b2b_vat" in se:
            msg = "P.IVA già presente (B2B) per il tuo account."
        if "uniq_owner_cf_b2c" in se or "uniq_b2c_codice_fiscale" in se:
            msg = "Codice Fiscale già presente (B2C) per il tuo account."
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
    # filtro base per utente
    filt: dict = {"owner_id": user["_id"]}
    if kind:
        filt["kind"] = kind
    if q:
        rx = {"$regex": q, "$options": "i"}
        filt["$or"] = [
            {"company_name": rx},
            {"first_name": rx},
            {"last_name": rx},
            {"email": rx},
            {"vat_number": rx},
            {"codice_fiscale": rx},
        ]

    total = await customers_col.count_documents(filt)
    cursor = (
        customers_col.find(filt)
        .skip(skip)
        .limit(limit)
        .sort("_id", -1)
    )

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
    doc = await customers_col.find_one({"_id": ObjectId(customer_id), "owner_id": user["_id"]})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return _to_public(doc)


@router.put("/{customer_id}", response_model=CustomerPublic)
async def update_customer(customer_id: str, payload: CustomerUpdate, user=Depends(get_current_user)):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    update_doc = {"$set": payload.model_dump(exclude_none=True)}
    try:
        res = await customers_col.update_one(
            {"_id": ObjectId(customer_id), "owner_id": user["_id"]},
            update_doc
        )
    except DuplicateKeyError as e:
        msg = "Valore duplicato su campo unico"
        se = str(e)
        if "uniq_owner_vat_b2b" in se or "uniq_b2b_vat" in se:
            msg = "P.IVA già presente (B2B) per il tuo account."
        if "uniq_owner_cf_b2c" in se or "uniq_b2c_codice_fiscale" in se:
            msg = "Codice Fiscale già presente (B2C) per il tuo account."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=msg)

    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")

    doc = await customers_col.find_one({"_id": ObjectId(customer_id), "owner_id": user["_id"]})
    return _to_public(doc)


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, user=Depends(get_current_user)):
    if not ObjectId.is_valid(customer_id):
        raise HTTPException(status_code=400, detail="Invalid id")
    res = await customers_col.delete_one({"_id": ObjectId(customer_id), "owner_id": user["_id"]})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return
