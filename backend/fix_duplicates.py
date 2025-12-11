
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "crm")

async def remove_duplicates():
    print(f"Connecting to MongoDB: {MONGO_URI} (DB: {MONGO_DB})")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]
    customers_col = db["customers"]

    # Pipeline to find duplicates for B2C customers based on codice_fiscale
    pipeline = [
        {"$match": {"kind": "B2C", "codice_fiscale": {"$exists": True, "$ne": None}}},
        {"$group": {
            "_id": "$codice_fiscale",
            "count": {"$sum": 1},
            "ids": {"$push": "$_id"}
        }},
        {"$match": {"count": {"$gt": 1}}}
    ]

    print("Searching for duplicates...")
    cursor = customers_col.aggregate(pipeline)
    
    duplicates_found = 0
    deleted_count = 0

    async for doc in cursor:
        duplicates_found += 1
        codice_fiscale = doc["_id"]
        ids = doc["ids"]
        
        # Keep the last inserted document (assuming implicit insertion order or just pick one)
        # In a real scenario, we might want to check created_at, but simplistic approach:
        # keep the last one in the list (usually the latest one returned by $push)
        ids_to_remove = ids[:-1]
        
        print(f"Found duplicate for codice_fiscale: {codice_fiscale}. Removing {len(ids_to_remove)} documents.")
        
        result = await customers_col.delete_many({"_id": {"$in": ids_to_remove}})
        deleted_count += result.deleted_count

    print("------------------------------------------------")
    print(f"Total duplicate groups found: {duplicates_found}")
    print(f"Total documents deleted: {deleted_count}")
    print("------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(remove_duplicates())
