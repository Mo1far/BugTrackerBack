import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env.read_envfile(os.path.join(BASE_DIR, '.env'))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads/')

POSTGRES_HOST = env.str('DB_HOST', default='localhost')

POSTGRES_PORT = env.int('DB_PORT', default=5432)
POSTGRES_PASSWORD = env.str('DB_PASSWORD', default='')
POSTGRES_USER = env.str('DB_USERNAME')
POSTGRES_DB = env.str('DB_NAME')
POSTGRES_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
