# app/indexes.py
from .db import customers_col
from pymongo import ASCENDING
from .db import invoices, counters

async def ensure_indexes():
    # Unico su vat_number per soli documenti B2B
    await customers_col.create_index(
        [("vat_number", ASCENDING)],
        name="uniq_b2b_vat",
        unique=True,
        partialFilterExpression={"kind": "B2B", "vat_number": {"$type": "string"}}
    )
    # Unicità numero fattura
    await invoices.create_index("number", unique=True, name="uniq_invoice_number")

    # Filtri frequenti
    await invoices.create_index([("customer_id", 1), ("issue_date", -1)], name="by_customer_date")
    await invoices.create_index([("issue_date", -1)], name="by_issue_date")

    # Contatore per anno (documenti tipo: { _id: "invoice-2025", seq: 42 })
    # await counters.create_index("_id", unique=True, name="uniq_counter_id")

    # Unico su codice_fiscale per soli documenti B2C
    await customers_col.create_index(
        [("codice_fiscale", ASCENDING)],
        name="uniq_b2c_codice_fiscale",
        unique=True,
        partialFilterExpression={"kind": "B2C", "codice_fiscale": {"$type": "string"}}
    )


