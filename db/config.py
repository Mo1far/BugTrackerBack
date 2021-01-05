import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# move to setup.py
env.read_envfile(os.path.join(BASE_DIR, '.env'))
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads/bugs')

POSTGRES_HOST = env.str('POSTGRES_HOST', default='localhost')

POSTGRES_PORT = env.int('POSTGRES_PORT', default=5432)
POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD', default='')
POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_DB = env.str('POSTGRES_DB')
POSTGRES_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
