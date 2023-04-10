from aiogram import executor

from src.bot.handlers import dp

if __name__ == '__main__':
    executor.start_polling(dp)
