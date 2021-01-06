from db.core import db
from db.models.base import TimedBaseModel


class BugStatus(TimedBaseModel):
    __tablename__ = 'bug_status'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    status = db.Column(db.String(15), nullable=False, default='pending')

    @classmethod
    async def check_status(cls, status_name):
        status = await BugStatus.select('status').where(BugStatus.status == status_name).gino.scalar()
        return str(status)


class Bug(TimedBaseModel):
    __tablename__ = 'bugs'

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    photo_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(50))
    status = db.Column(db.Integer, db.ForeignKey('bug_status.id'), nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    cause = db.Column(db.Text)

    @classmethod
    async def get_by_id(cls, id):
        bug = await Bug.query.where(Bug.id == id).gino.first()
        return bug
