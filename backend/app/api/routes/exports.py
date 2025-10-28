from fastapi import APIRouter, Depends, Response
from io import BytesIO
import pandas as pd
from ...models.customer import Customer
from ..deps import get_current_admin

router = APIRouter()

def _customers_to_records(objs):
    recs = []
    for c in objs:
        d = c.model_dump(by_alias=True)
        d["_id"] = str(d.get("_id", ""))
        recs.append({
            "_id": d["_id"],
            "name": d.get("name"),
            "email": d.get("email"),
            "phone": d.get("phone"),
            "address": d.get("address"),
            "customer_type": d.get("customer_type"),
            "vat_or_tax_id": d.get("vat_or_tax_id"),
            "registered_at": d.get("registered_at"),
            "tags": ",".join(d.get("tags", [])) if d.get("tags") else "",
            "is_active": d.get("is_active", True),
        })
    return recs

@router.get("/exports/customers.csv")
async def export_customers_csv(admin=Depends(get_current_admin)):
    docs = await Customer.find({}).to_list()
    df = pd.DataFrame(_customers_to_records(docs))
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    return Response(
        content=csv_bytes,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="customers.csv"'}
    )

@router.get("/exports/customers.xlsx")
async def export_customers_xlsx(admin=Depends(get_current_admin)):
    docs = await Customer.find({}).to_list()
    df = pd.DataFrame(_customers_to_records(docs))
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="customers")
    buf.seek(0)
    return Response(
        content=buf.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="customers.xlsx"'}
    )
