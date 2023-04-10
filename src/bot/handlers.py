import json

from aiogram import Bot, Dispatcher
from aiogram import types

from src import my_exceptions
from src.bot.utils import validation_user_input
from src.config import TOKEN
from src.core.db import get_payments

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    name = message.chat.full_name
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Hi, [{name}]({message.chat.user_url})!',
        reply_markup=types.ForceReply(),
        parse_mode='Markdown')


@dp.message_handler()
async def mongo_query(message: types.Message):
    try:
        request_data = await validation_user_input(message)
        group_type = request_data.group_type
        dt_from = request_data.dt_from
        dt_upto = request_data.dt_upto
        result = await get_payments(group_type, dt_from, dt_upto)

        result = json.dumps(result[0])
        await bot.send_message(
            chat_id=message.chat.id,
            text=result)

    except my_exceptions.BadRequestError as error:
        await message.answer(error.message)

    except my_exceptions.ValidationError as error:
        await message.answer(error.message)
