from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .core.config import settings
from .models.customer import Customer

async def init_beanie():
    client = AsyncIOMotorClient(settings.mongo_uri)
    db = client.get_default_database() or client.get_database("crm")
    await init_beanie(database=db, document_models=[Customer])
