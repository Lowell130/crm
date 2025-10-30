from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, MONGO_DB


client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

# Collezioni
users_col = db["users"]
customers_col = db["customers"]
invoices = db["invoices"]
counters = db["counters"]  # per la sequenza numeri fattura per anno

