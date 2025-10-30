# app/utils/sequences.py
from datetime import date
from pymongo import ReturnDocument
from app.db import counters

async def next_invoice_number(issue_date: date | None = None) -> str:
    y = (issue_date or date.today()).year
    key = f"invoice-{y}"
    doc = await counters.find_one_and_update(
        {"_id": key},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    seq = doc["seq"]
    return f"{y}-{seq:05d}"
