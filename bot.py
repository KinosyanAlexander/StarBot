#!venv/bin/python
import logging
import shelve
import requests

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook

from config import BOT_TOKEN
from config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL
from config import APP_MODE, TMP_DATA


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    logging.warning('Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    await requests.get(WEBHOOK_URL)
    logging.info('Is it work?')
    logging.warning('Bye! Shutting down webhook connection')


def main(mode='dev'):
    if mode == 'dev':
        executor.start_polling(dp, skip_updates=True)
    elif mode == 'prod':
        start_webhook(dispatcher=dp,
                      webhook_path=WEBHOOK_PATH,
                      on_startup=on_startup,
                      on_shutdown=on_shutdown,
                      skip_updates=True,
                      host=WEBAPP_HOST,
                      port=WEBAPP_PORT)


if __name__ == "__main__":
    from commands import *

    main(mode=APP_MODE)