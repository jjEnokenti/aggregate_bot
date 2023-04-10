from enum import Enum

from pydantic import BaseModel
from pydantic.validators import datetime


class MyEnum(str, Enum):
    month = 'month'
    day = 'day'
    hour = 'hour'


class Request(BaseModel):
    dt_from: datetime
    dt_upto: datetime
    group_type: MyEnum
