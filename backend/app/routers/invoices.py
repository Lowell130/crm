from datetime import date, timedelta
from typing import Optional, List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pymongo.errors import DuplicateKeyError
from pymongo import ReturnDocument

from app.db import invoices, customers_col, counters
from app.models import InvoiceCreate, InvoiceUpdate, InvoiceOut, InvoiceItem
from ..auth import get_current_user
from app.utils.sequences import next_invoice_number

router = APIRouter(prefix="/invoices", tags=["invoices"])

# ----------------------------
# Helpers
# ----------------------------
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

def build_invoice_filter(q: Optional[str], status: Optional[str]):
    query: dict = {}
    if status in ("issued", "draft", "cancelled"):
        query["status"] = status
    if q:
        rx = {"$regex": q, "$options": "i"}
        query["$or"] = [
            {"number": rx},
            {"customer_snapshot.company_name": rx},
            {"customer_snapshot.first_name": rx},
            {"customer_snapshot.last_name": rx},
            {"customer_snapshot.email": rx},
            {"customer_snapshot.vat_number": rx},
            {"customer_snapshot.codice_fiscale": rx},
        ]
    return query

def _parse_date(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    try:
        _ = date.fromisoformat(s)
        return s
    except Exception:
        raise HTTPException(400, "Formato data non valido. Usa YYYY-MM-DD.")

# ----------------------------
# DASHBOARD: rotte PRIMA di /{invoice_id}
# ----------------------------
@router.get("/stats")
async def invoices_stats(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    user=Depends(get_current_user),
):
    q = {}
    df = _parse_date(date_from)
    dt = _parse_date(date_to)
    if df or dt:
        rng = {}
        if df: rng["$gte"] = df
        if dt: rng["$lte"] = dt
        q["issue_date"] = rng

    total = await invoices.count_documents(q)
    draft = await invoices.count_documents({**q, "status": "draft"})
    issued = await invoices.count_documents({**q, "status": "issued"})
    cancelled = await invoices.count_documents({**q, "status": "cancelled"})
    paid_count = await invoices.count_documents({**q, "paid": True})

    pipeline_sum = []
    if q:
        pipeline_sum.append({"$match": q})
    pipeline_sum += [
        {"$group": {
            "_id": None,
            "sum_total": {"$sum": {"$ifNull": ["$total", 0]}},
            "sum_paid":  {"$sum": {
                "$cond": [
                    {"$eq": [{"$ifNull": ["$paid", False]}, True]},
                    {"$ifNull": ["$total", 0]},
                    0
                ]
            }}
        }}
    ]
    sums = await invoices.aggregate(pipeline_sum).to_list(length=1)
    sum_total = float(sums[0]["sum_total"]) if sums else 0.0
    sum_paid = float(sums[0]["sum_paid"]) if sums else 0.0

    return {
        "counts": {
            "total": total,
            "draft": draft,
            "issued": issued,
            "cancelled": cancelled,
            "paid": paid_count
        },
        "amounts": {
            "total": round(sum_total, 2),
            "paid": round(sum_paid, 2),
            "outstanding": round(sum_total - sum_paid, 2)
        }
    }

@router.get("/timeseries")
async def invoices_timeseries(
    days: int = Query(30, ge=1, le=365),
    user=Depends(get_current_user),
):
    today = date.today()
    start = (today - timedelta(days=days - 1)).isoformat()

    pipeline_total = [
        {"$match": {"issue_date": {"$gte": start}, "status": {"$ne": "cancelled"}}},
        {"$group": {"_id": "$issue_date", "total_day": {"$sum": {"$ifNull": ["$total", 0]}}}},
        {"$sort": {"_id": 1}}
    ]
    pipeline_paid = [
        {"$match": {"paid": True, "paid_at": {"$gte": start}}},
        {"$group": {"_id": "$paid_at", "paid_day": {"$sum": {"$ifNull": ["$total", 0]}}}},
        {"$sort": {"_id": 1}}
    ]

    totals = {r["_id"]: float(r["total_day"]) for r in await invoices.aggregate(pipeline_total).to_list(length=10000)}
    paids  = {r["_id"]: float(r["paid_day"])  for r in await invoices.aggregate(pipeline_paid).to_list(length=10000)}

    out = []
    for i in range(days):
        d = (today - timedelta(days=(days - 1 - i))).isoformat()
        out.append({
            "date": d,
            "total": round(totals.get(d, 0.0), 2),
            "paid":  round(paids.get(d, 0.0), 2)
        })
    return out

@router.get("/top-customers")
async def invoices_top_customers(
    limit: int = Query(5, ge=1, le=50),
    days: int = Query(90, ge=1, le=365),
    user=Depends(get_current_user),
):
    start = (date.today() - timedelta(days=days)).isoformat()

    name_expr = {
        "$ifNull": [
            "$customer_snapshot.company_name",
            {
                "$trim": {
                    "input": {
                        "$concat": [
                            {"$ifNull": ["$customer_snapshot.first_name", ""]},
                            " ",
                            {"$ifNull": ["$customer_snapshot.last_name", ""]},
                        ]
                    }
                }
            }
        ]
    }

    pipeline = [
        {"$match": {"issue_date": {"$gte": start}, "status": {"$ne": "cancelled"}}},
        {"$group": {
            "_id": {"customer_id": "$customer_id", "name": name_expr},
            "sum_total": {"$sum": {"$ifNull": ["$total", 0]}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"sum_total": -1}},
        {"$limit": limit}
    ]

    rows = await invoices.aggregate(pipeline).to_list(length=limit + 10)
    return [
        {
            "customer_id": r["_id"]["customer_id"],
            "name": (r["_id"]["name"] or "").strip(),
            "invoices": int(r.get("count", 0)),
            "amount": round(float(r.get("sum_total", 0.0)), 2)
        } for r in rows
    ]

# ----------------------------
# CRUD
# ----------------------------
@router.get("", response_model=List[InvoiceOut])
async def list_invoices(
    response: Response,
    q: Optional[str] = Query(None, description="Ricerca per numero o anagrafica cliente"),
    customer_id: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    status: Optional[str] = Query(None, regex="^(draft|issued|cancelled)$"),
    paid: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 20,
    user=Depends(get_current_user),
):
    query = build_invoice_filter(q, status)

    if customer_id:
        query["customer_id"] = customer_id

    if date_from or date_to:
        rng = {}
        if date_from:
            rng["$gte"] = date_from.isoformat()
        if date_to:
            rng["$lte"] = date_to.isoformat()
        query["issue_date"] = rng

    if paid is not None:
        query["paid"] = bool(paid)

    total = await invoices.count_documents(query)
    cursor = (
        invoices.find(query)
        .sort([("issue_date", -1), ("_id", -1)])
        .skip(skip)
        .limit(limit)
    )
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
    cust = await customers_col.find_one({"_id": ObjectId(payload.customer_id)})
    if not cust:
        raise HTTPException(400, "Cliente inesistente")

    number = payload.number or await next_invoice_number(payload.issue_date)
    subtotal, vat_total, total = compute_totals(payload.items)

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
        "paid": bool(getattr(payload, "paid", False)),
        "paid_at": payload.paid_at.isoformat() if getattr(payload, "paid_at", None) else None,
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
        subtotal, vat_total, total = compute_totals(payload.items)
        update["subtotal"] = subtotal
        update["vat_total"] = vat_total
        update["total"] = total

    if getattr(payload, "paid", None) is not None:
        update["paid"] = bool(payload.paid)
        if payload.paid is False and getattr(payload, "paid_at", None) is None:
            update["paid_at"] = None
    if getattr(payload, "paid_at", None) is not None:
        update["paid_at"] = payload.paid_at.isoformat()

    if not update:
        doc = await invoices.find_one({"_id": oid})
        if not doc:
            raise HTTPException(404, "Fattura non trovata")
        return serialize(doc)

    try:
        updated = await invoices.find_one_and_update(
            {"_id": oid},
            {"$set": update},
            return_document=ReturnDocument.AFTER,
        )
    except DuplicateKeyError:
        raise HTTPException(409, "Numero fattura già esistente")

    if not updated:
        raise HTTPException(404, "Fattura non trovata")
    return serialize(updated)

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice(invoice_id: str, user=Depends(get_current_user)):
    res = await invoices.delete_one({"_id": parse_object_id(invoice_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Fattura non trovata")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/number/preview/next", response_model=str)
async def preview_next_number(issue_date: Optional[date] = None, user=Depends(get_current_user)):
    y = (issue_date or date.today()).year
    key = f"invoice-{y}"
    doc = await counters.find_one({"_id": key}) or {"seq": 0}
    seq = doc["seq"] + 1
    return f"{y}-{seq:05d}"
