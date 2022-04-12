#!venv/bin/python
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

from commands import *

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)