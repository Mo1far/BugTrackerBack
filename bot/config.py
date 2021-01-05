import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath('..')
ENV_FILE = os.path.join(BASE_DIR, '.env')

load_dotenv(ENV_FILE)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

DB_USERNAME = os.environ.get('DB_USERNAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

DEFAULT_RATE_LIMIT = 2
