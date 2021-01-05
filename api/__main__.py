from aiohttp.web import run_app

from api.app import create_app
from api.config import API_ADDRESS, API_PORT
from db import db
from db.config import POSTGRES_URI


def main():
    app = create_app([db])
    db.init_app(app, dict(dsn=POSTGRES_URI))
    run_app(app, host=API_ADDRESS, port=API_PORT)


if __name__ == '__main__':
    main()
