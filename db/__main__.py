from db import db
from db.config import POSTGRES_URI


async def init_db():
    await db.set_bind(POSTGRES_URI)
    return db
