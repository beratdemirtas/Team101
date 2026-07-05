from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DATABASE_NAME

client: AsyncIOMotorClient = None

async def connect_db():
    global client
    client = AsyncIOMotorClient(MONGO_URI)

async def close_db():
    global client
    if client:
        client.close()

def get_database():
    return client[DATABASE_NAME]
