from src.config import GROUP_IDS, DATE_FORMATS, MONGODB_URI
from src.core.connect import get_client
from src.bot.utils import get_group_config


def get_pipeline(group_type: str, dt_from: str, dt_upto: str) -> list[dict]:
    group_id = get_group_config(GROUP_IDS, group_type)
    date_format = get_group_config(DATE_FORMATS, group_type)
    pipeline = [
        {
            '$match': {
                'dt': {'$gte': dt_from, '$lte': dt_upto}
            }
        },
        {
            '$group': {
                '_id': group_id,
                'total_value': {'$sum': '$value'},
                'date': {
                    '$first': {
                        '$dateToString': {
                            'format': date_format,
                            'date': '$dt'
                        }
                    }
                }
            }
        },
        {
            '$sort': {'date': 1}
        },
        {
            '$group': {
                '_id': None,
                'dataset': {'$push': '$total_value'},
                'labels': {'$push': '$date'}
            }
        },
        {
            '$project':
                {
                    '_id': 0
                }
        }
    ]

    return pipeline


async def get_payments(group_type, dt_from, dt_upto):
    client = await get_client(MONGODB_URI)
    db = client.test_db
    coll = db.salaries
    pipeline = get_pipeline(group_type, dt_from, dt_upto)
    return await coll.aggregate(pipeline).to_list(length=None)
