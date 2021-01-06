import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath('..')
ENV_FILE = os.path.join(BASE_DIR, '.env')

load_dotenv(ENV_FILE)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

DEFAULT_RATE_LIMIT = 2
