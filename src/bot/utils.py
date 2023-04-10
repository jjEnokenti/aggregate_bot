import json

import pydantic
from aiogram import types

from src import my_exceptions
from src.core.request_schema import Request


def get_group_config(config_data: dict, group_type: str):
    return config_data[group_type]


async def validation_user_input(message: types.Message) -> Request | bool:
    try:
        text = json.loads(message.text)
        if isinstance(text, (int, float, bool)):
            raise my_exceptions.BadRequestError
        if isinstance(text, str):
            raise my_exceptions.ValidationError
    except json.decoder.JSONDecodeError:
        raise my_exceptions.ValidationError

    try:
        request_data = Request(**text)
        return request_data
    except pydantic.error_wrappers.ValidationError:
        raise my_exceptions.BadRequestError
