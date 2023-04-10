from motor.motor_asyncio import AsyncIOMotorClient


async def get_client(uri):
    client = AsyncIOMotorClient(uri)

    return client
