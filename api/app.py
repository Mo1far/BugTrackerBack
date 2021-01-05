import logging

from aiohttp.web import run_app
from aiohttp.web_app import Application

from api.handlers import HANDLERS
from db.config import POSTGRES_URI
from db.core import db

MEGABYTE = 1024 ** 2
MAX_REQUEST_SIZE = 70 * MEGABYTE

log = logging.getLogger(__name__)


def create_app(middlewares=[]):
    app = Application(middlewares=middlewares)

    for handler in HANDLERS:
        log.info('Registering handler %r as %r', handler, handler.URL_PATH)
        app.router.add_route('*', handler.URL_PATH, handler)

    return app
