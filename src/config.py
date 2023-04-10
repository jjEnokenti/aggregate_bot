import os

from dotenv import load_dotenv

load_dotenv()

GROUP_IDS = {
    'hour': {
        'hour': {'$hour': '$dt'},
        'day': {'$dayOfMonth': '$dt'},
        'month': {'$month': '$dt'},
        'year': {'$year': '$dt'}
    },
    'day': {
        'day': {'$dayOfMonth': '$dt'},
        'month': {'$month': '$dt'},
        'year': {'$year': '$dt'}
    },
    'month': {
        'month': {'$month': '$dt'},
        'year': {'$year': '$dt'}
    }
}

DATE_FORMATS = {
    'hour': '%Y-%m-%dT%H:00:00',
    'day': '%Y-%m-%dT00:00:00',
    'month': '%Y-%m-01T00:00:00'
}

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')

TOKEN = os.getenv('TOKEN')
