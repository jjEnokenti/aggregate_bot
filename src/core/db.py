from dateutil.relativedelta import relativedelta

from src.config import GROUP_IDS, DATE_FORMATS, MONGODB_URI, DB_NAME
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


async def create_docs(db_conn, group_type, dt_from, dt_upto):

    salaries = db_conn.salaries

    start = dt_from
    end_date = dt_upto

    current_date = start
    while current_date <= end_date:

        doc = await salaries.find_one({'dt': {'$eq': current_date}})

        if not doc:
            new_doc = {'dt': current_date, 'value': 0}
            await salaries.insert_one(new_doc)

        if group_type == 'hour':
            current_date += relativedelta(hours=1)
        elif group_type == 'day':
            current_date += relativedelta(days=1)
        else:
            current_date += relativedelta(months=1)


async def get_payments(group_type, dt_from, dt_upto):
    db = await get_client(MONGODB_URI, DB_NAME)
    await create_docs(db, group_type, dt_from, dt_upto)

    salaries = db.salaries
    pipeline = get_pipeline(group_type, dt_from, dt_upto)
    return await salaries.aggregate(pipeline).to_list(length=None)
