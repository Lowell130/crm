import asyncio
from bson import ObjectId
from app.db import db, customers_col, invoices, counters, users_col

EMAIL = "tua@email.it"  # scegli a chi assegnare i documenti legacy

async def run():
    user = await users_col.find_one({"email": EMAIL})
    if not user:
        print("User non trovato"); return
    oid = user["_id"]

    # customers
    await customers_col.update_many({"owner_id": {"$exists": False}}, {"$set": {"owner_id": oid}})
    # invoices (+year calcolato se manca)
    async for inv in invoices.find({"owner_id": {"$exists": False}}):
        y = int(str(inv.get("issue_date", ""))[:4]) if inv.get("issue_date") else None
        upd = {"owner_id": oid}
        if y is not None: upd["year"] = y
        await invoices.update_one({"_id": inv["_id"]}, {"$set": upd})
    # counters (se usavi il vecchio schema)
    async for c in counters.find({"owner_id": {"$exists": False}}):
        # prova a inferire anno da _id="invoice-YYYY"
        y = None
        if isinstance(c.get("_id"), str) and c["_id"].startswith("invoice-"):
            try: y = int(c["_id"].split("-")[1])
            except: pass
        upd = {"owner_id": oid}
        if y is not None: upd["year"] = y
        await counters.update_one({"_id": c["_id"]}, {"$set": upd})

if __name__ == "__main__":
    asyncio.run(run())
