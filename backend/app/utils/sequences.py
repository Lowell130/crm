from datetime import date
from pymongo import ReturnDocument
from app.db import counters

async def next_invoice_number(owner_id, issue_date: date | None = None) -> str:
    y = (issue_date or date.today()).year
    doc = await counters.find_one_and_update(
        {"owner_id": owner_id, "year": y},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    seq = doc["seq"]
    return f"{y}-{seq:05d}"
