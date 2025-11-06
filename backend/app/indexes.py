# app/indexes.py
from pymongo import ASCENDING, DESCENDING
from .db import customers_col, invoices, counters, users_col

async def ensure_indexes():
    # (Pulizia indici legacy: ignora errori se non esistono)
    for name in [
        "uniq_b2b_vat", "uniq_b2c_codice_fiscale", "uniq_invoice_number",
        "uniq_owner_vat_b2b", "uniq_owner_cf_b2c", "uniq_owner_year_number",
        "uniq_users_email"
    ]:
        try:
            await customers_col.drop_index(name)
        except Exception: pass
        try:
            await invoices.drop_index(name)
        except Exception: pass
        try:
            await users_col.drop_index(name)
        except Exception: pass

    # ✅ utenti
    await users_col.create_index([("email", ASCENDING)], name="uniq_users_email", unique=True)

    # ✅ customers: unicità per utente
    await customers_col.create_index(
        [("owner_id", ASCENDING), ("vat_number", ASCENDING)],
        name="uniq_owner_vat_b2b",
        unique=True,
        partialFilterExpression={"kind": "B2B", "owner_id": {"$exists": True}, "vat_number": {"$type": "string"}}
    )
    await customers_col.create_index(
        [("owner_id", ASCENDING), ("codice_fiscale", ASCENDING)],
        name="uniq_owner_cf_b2c",
        unique=True,
        partialFilterExpression={"kind": "B2C", "owner_id": {"$exists": True}, "codice_fiscale": {"$type": "string"}}
    )
    await customers_col.create_index([("owner_id", ASCENDING), ("_id", DESCENDING)], name="owner_recent")

    # ✅ invoices: unicità numero *per utente* e *per anno*
    await invoices.create_index(
        [("owner_id", ASCENDING), ("year", ASCENDING), ("number", ASCENDING)],
        name="uniq_owner_year_number",
        unique=True
    )
    await invoices.create_index([("owner_id", ASCENDING), ("issue_date", DESCENDING)], name="owner_issue_date_desc")

    # (opzionale) counters per velocità
    await counters.create_index([("owner_id", ASCENDING), ("year", ASCENDING)], name="owner_year_counter")
