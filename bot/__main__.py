import logging

from aiogram import Dispatcher

from bot.core import executor
from db import db
from db.config import POSTGRES_URI

from bot.chains import *


async def on_startup(dp: Dispatcher):
    logging.info("Setup PostgreSQL Connection")
    await db.set_bind(POSTGRES_URI)


async def on_shutdown(dp: Dispatcher):
    bind = db.pop_bind()
    if bind:
        logging.info("Close PostgreSQL Connection")
        await bind.close()


def main():
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)

    executor.start_polling()


if __name__ == '__main__':
    main()
