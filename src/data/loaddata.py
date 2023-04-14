import asyncio

import bson
import pymongo

from src.config import MONGODB_URI, DB_NAME
from src.core.connect import get_client


async def upload_data(file_name):
    client = await get_client(MONGODB_URI, DB_NAME)

    db = client
    coll = db.salaries

    data = get_data_from_bson(file_name)

    await coll.insert_many(data)


def get_data_from_bson(file_name):
    with open(file_name, 'rb') as bsonf:
        return bson.decode_all(bsonf.read())


if __name__ == '__main__':
    bson_file_name = 'sample_collection.bson'
    try:
    	asyncio.run(upload_data(bson_file_name))
    except pymongo.errors.BulkWriteError:
    	pass

