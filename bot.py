#!venv/bin/python
import logging

from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_URL
from config import APP_MODE
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


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