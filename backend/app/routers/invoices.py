# app/routers/invoices.py
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from typing import Optional, List
from datetime import date
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.db import invoices, customers_col, counters
from app.models import InvoiceCreate, InvoiceUpdate, InvoiceOut, InvoiceItem
from ..auth import get_current_user
from app.utils.sequences import next_invoice_number

router = APIRouter(prefix="/invoices", tags=["invoices"])

def compute_totals(items: List[InvoiceItem]) -> tuple[float, float, float]:
    subtotal = round(sum(i.net_amount for i in items), 2)
    vat_total = round(sum(i.vat_amount for i in items), 2)
    total = round(subtotal + vat_total, 2)
    return subtotal, vat_total, total

def parse_object_id(s: str) -> ObjectId:
    if not ObjectId.is_valid(s):
        raise HTTPException(status_code=400, detail="ID non valido")
    return ObjectId(s)

def serialize(inv: dict) -> InvoiceOut:
    inv["id"] = str(inv.pop("_id"))
    return InvoiceOut(**inv)

@router.get("", response_model=List[InvoiceOut])
async def list_invoices(
    response: Response,
    q: Optional[str] = Query(None, description="search su number"),
    customer_id: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    status: Optional[str] = Query(None, regex="^(draft|issued|cancelled)$"),
    skip: int = 0,
    limit: int = 20,
    user=Depends(get_current_user),
):
    query: dict = {}
    if q:
        query["number"] = {"$regex": q, "$options": "i"}
    if customer_id:
        query["customer_id"] = customer_id
    if status:
        query["status"] = status
    if date_from or date_to:
        rng = {}
        if date_from:
            rng["$gte"] = date_from.isoformat()
        if date_to:
            rng["$lte"] = date_to.isoformat()
        query["issue_date"] = rng

    total = await invoices.count_documents(query)
    cursor = invoices.find(query).sort("issue_date", -1).skip(skip).limit(limit)
    docs = [serialize(d) async for d in cursor]
    response.headers["X-Total-Count"] = str(total)
    return docs

@router.get("/{invoice_id}", response_model=InvoiceOut)
async def get_invoice(invoice_id: str, user=Depends(get_current_user)):
    doc = await invoices.find_one({"_id": parse_object_id(invoice_id)})
    if not doc:
        raise HTTPException(404, "Fattura non trovata")
    return serialize(doc)

@router.post("", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
async def create_invoice(payload: InvoiceCreate, user=Depends(get_current_user)):
    # Verifica cliente
    cust = await customers_col.find_one({"_id": ObjectId(payload.customer_id)})
    if not cust:
        raise HTTPException(400, "Cliente inesistente")

    # Numero: genera se mancante
    number = payload.number or await next_invoice_number(payload.issue_date)

    # Totali
    subtotal, vat_total, total = compute_totals(payload.items)

    # snapshot anagrafica base (utile anche se poi il cliente cambia dati)
    snapshot = {
        "kind": cust.get("kind"),
        "company_name": cust.get("company_name"),
        "first_name": cust.get("first_name"),
        "last_name": cust.get("last_name"),
        "vat_number": cust.get("vat_number"),
        "codice_fiscale": cust.get("codice_fiscale"),
        "email": cust.get("email"),
        "address": cust.get("address"),
        "city": cust.get("city"),
        "zip": cust.get("zip"),
        "country": cust.get("country"),
    }

    doc = {
        "customer_id": payload.customer_id,
        "issue_date": payload.issue_date.isoformat(),
        "due_date": payload.due_date.isoformat() if payload.due_date else None,
        "notes": payload.notes,
        "items": [i.dict() for i in payload.items],
        "number": number,
        "status": payload.status,
        "subtotal": subtotal,
        "vat_total": vat_total,
        "total": total,
        "customer_snapshot": snapshot,
        "created_at": date.today().isoformat(),
    }

    try:
        res = await invoices.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(409, "Numero fattura già esistente")

    inserted = await invoices.find_one({"_id": res.inserted_id})
    return serialize(inserted)

@router.patch("/{invoice_id}", response_model=InvoiceOut)
async def update_invoice(invoice_id: str, payload: InvoiceUpdate, user=Depends(get_current_user)):
    oid = parse_object_id(invoice_id)
    update: dict = {}
    if payload.issue_date is not None:
        update["issue_date"] = payload.issue_date.isoformat()
    if payload.due_date is not None:
        update["due_date"] = payload.due_date.isoformat()
    if payload.notes is not None:
        update["notes"] = payload.notes
    if payload.number is not None:
        update["number"] = payload.number
    if payload.status is not None:
        update["status"] = payload.status
    if payload.items is not None:
        update["items"] = [i.dict() for i in payload.items]
        # ricalcola totali
        subtotal, vat_total, total = compute_totals(payload.items)
        update["subtotal"] = subtotal
        update["vat_total"] = vat_total
        update["total"] = total

    if not update:
        doc = await invoices.find_one({"_id": oid})
        if not doc:
            raise HTTPException(404, "Fattura non trovata")
        return serialize(doc)

    try:
        res = await invoices.find_one_and_update(
            {"_id": oid},
            {"$set": update},
            return_document=True
        )
    except DuplicateKeyError:
        raise HTTPException(409, "Numero fattura già esistente")

    if not res:
        raise HTTPException(404, "Fattura non trovata")
    return serialize(res)

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(invoice_id: str, user=Depends(get_current_user)):
    res = await invoices.delete_one({"_id": parse_object_id(invoice_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Fattura non trovata")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/number/preview/next", response_model=str)
async def preview_next_number(issue_date: Optional[date] = None, user=Depends(get_current_user)):
    # NON incrementa: calcola guardando il contatore corrente
    y = (issue_date or date.today()).year
    key = f"invoice-{y}"
    doc = await counters.find_one({"_id": key}) or {"seq": 0}
    seq = doc["seq"] + 1
    return f"{y}-{seq:05d}"
