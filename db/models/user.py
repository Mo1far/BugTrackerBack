from db.core import db
from db.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    locale = db.Column(db.String(5), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)

    @classmethod
    async def exist(cls, tguser):
        user = await User.query.where(User.id == tguser).gino.first()
        return bool(user)
