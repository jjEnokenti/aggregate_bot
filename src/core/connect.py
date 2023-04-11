from motor.motor_asyncio import AsyncIOMotorClient


async def get_client(uri, db_name):
    return AsyncIOMotorClient(uri)[db_name]
