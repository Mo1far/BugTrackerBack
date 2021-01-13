import os

from envparse import env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env.read_envfile(os.path.join(BASE_DIR, '.env'))

API_ADDRESS = env.str('API_ADDRESS')
API_PORT = env.int('API_PORT', default=5000)

UPLOADS_DIR = env.str('UPLOADS_DIR', default='uploads/')
UPLOADS_PATH = os.path.join(BASE_DIR, UPLOADS_DIR)
