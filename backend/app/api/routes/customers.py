from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from ...models.customer import Customer
from ...schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from ..deps import get_current_admin

router = APIRouter()

@router.post("/customers", response_model=CustomerOut)
async def create_customer(data: CustomerCreate, admin=Depends(get_current_admin)):
    doc = Customer(**data.model_dump())
    await doc.insert()
    return CustomerOut.model_validate(doc.model_dump(by_alias=True))

@router.get("/customers/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: str, admin=Depends(get_current_admin)):
    doc = await Customer.get(customer_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return CustomerOut.model_validate(doc.model_dump(by_alias=True))

@router.get("/customers", response_model=List[CustomerOut])
async def list_customers(
    admin=Depends(get_current_admin),
    q: Optional[str] = None,
    customer_type: Optional[str] = Query(None, pattern="^(B2C|B2B)$"),
    tag: Optional[str] = None,
    sort: Optional[str] = Query(None, description="field,[asc|desc] e.g. registered_at,desc"),
    skip: int = 0,
    limit: int = 50,
):
    q_filters = {}
    if q:
        # naive text search over name/email/phone
        q_filters["$or"] = [
            {"name": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}},
            {"phone": {"$regex": q, "$options": "i"}},
            {"tags": {"$in": [q]}},
        ]
    if customer_type:
        q_filters["customer_type"] = customer_type
    if tag:
        q_filters.setdefault("tags", {"$in": [tag]})

    cursor = Customer.find(q_filters) if q_filters else Customer.find_many({})

    # sorting
    if sort:
        try:
            field, direction = sort.split(",", 1)
            direction = -1 if direction.lower() == "desc" else 1
            cursor = cursor.sort([(field, direction)])
        except Exception:
            pass

    results = await cursor.skip(skip).limit(limit).to_list()
    return [CustomerOut.model_validate(r.model_dump(by_alias=True)) for r in results]

@router.patch("/customers/{customer_id}", response_model=CustomerOut)
async def update_customer(customer_id: str, data: CustomerUpdate, admin=Depends(get_current_admin)):
    doc = await Customer.get(customer_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    update_data = {k: v for k, v in data.model_dump(exclude_unset=True).items()}
    await doc.set(update_data)
    await doc.save()
    return CustomerOut.model_validate(doc.model_dump(by_alias=True))

@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str, admin=Depends(get_current_admin)):
    doc = await Customer.get(customer_id)
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    await doc.delete()
    return {"ok": True}
