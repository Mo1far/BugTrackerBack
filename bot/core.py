import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor

from bot.config import TELEGRAM_BOT_TOKEN
from bot.middlewares.registration import RegistrationMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode='HTML')

storage = RedisStorage2(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    db=os.getenv('REDIS_DB'),
    password=os.getenv('REDIS_PASSWORD'),
)


dp = Dispatcher(bot=bot, storage=storage)

dp.middleware.setup(ThrottlingMiddleware())
dp.middleware.setup(RegistrationMiddleware())

executor = Executor(dp, skip_updates=True)
