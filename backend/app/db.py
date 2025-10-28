from beanie import init_beanie as beanie_init
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConfigurationError
from .core.config import settings
from .models.customer import Customer

async def init_beanie():
    client = AsyncIOMotorClient(settings.mongo_uri)

    # Prova a usare il DB di default dalla URI; se non presente, fallback a MONGO_DB
    try:
        db = client.get_default_database()
        if db is None:
            raise ConfigurationError("No default database name defined or provided.")
    except ConfigurationError:
        db = client.get_database(settings.mongo_db)

    await beanie_init(database=db, document_models=[Customer])
