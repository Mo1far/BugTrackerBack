import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env.read_envfile(os.path.join(BASE_DIR, '.env'))

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

ADMIN_CHAT_ID = env.str('ADMIN_CHAT_ID')

DEFAULT_RATE_LIMIT = 2
