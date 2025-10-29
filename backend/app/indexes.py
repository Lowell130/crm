# app/indexes.py
from .db import customers_col
from pymongo import ASCENDING

async def ensure_indexes():
    # Unico su vat_number per soli documenti B2B
    await customers_col.create_index(
        [("vat_number", ASCENDING)],
        name="uniq_b2b_vat",
        unique=True,
        partialFilterExpression={"kind": "B2B", "vat_number": {"$type": "string"}}
    )
    # Unico su codice_fiscale per soli documenti B2C
    await customers_col.create_index(
        [("codice_fiscale", ASCENDING)],
        name="uniq_b2c_codice_fiscale",
        unique=True,
        partialFilterExpression={"kind": "B2C", "codice_fiscale": {"$type": "string"}}
    )
