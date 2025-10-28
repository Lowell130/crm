from fastapi import APIRouter, Depends
from datetime import datetime
from ...models.customer import Customer
from ..deps import get_current_admin

router = APIRouter()

# @router.get("/stats/summary")
# async def stats_summary(admin=Depends(get_current_admin)):
#     total = await Customer.find({}).count()
#     b2c = await Customer.find({"customer_type": "B2C"}).count()
#     b2b = await Customer.find({"customer_type": "B2B"}).count()
#     return {"total": total, "b2c": b2c, "b2b": b2b}

# @router.get("/stats/active-by-month")
# async def active_by_month(admin=Depends(get_current_admin)):
#     pipeline = [
#         {"$match": {"is_active": True}},
#         {"$project": {"ym": {"$dateToString": {"format": "%Y-%m", "date": "$registered_at"}}}},
#         {"$group": {"_id": "$ym", "count": {"$sum": 1}}},
#         {"$sort": {"_id": 1}},
#     ]
#     data = await Customer.get_motor_collection().aggregate(pipeline).to_list(length=None)
#     return {"data": data}
