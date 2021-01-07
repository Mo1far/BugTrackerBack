import json

from aiohttp import web
from sqlalchemy import and_

from db import Bug, db
from db.models import BugStatus


class BugView(web.View):
    URL_PATH = r'/bugs/{id:\d}'

    @property
    def user_id(self):
        return int(self.request.match_info.get('id'))

    async def get(self):
        bug = await Bug.get(self.user_id)
        status = await BugStatus.get(bug.status)

        response = {'id': bug.id,
                    'photo_path': bug.photo_path,
                    'description': bug.description,
                    'location': bug.location,
                    'status': status.status
                    }

        return web.json_response(response)


class BugsView(web.View):
    URL_PATH = r'/bugs'

    @property
    async def category_ids(self):
        categories = await BugStatus.query.where(BugStatus.status.in_(self.categories)).gino.all()
        return [category.id for category in categories]

    @property
    def categories(self):
        return set(json.loads(self.request.query.get('categories')))

    async def get(self):
        response = []

        query = Bug.join(BugStatus, and_(Bug.status == BugStatus.id,
                                         BugStatus.status.in_(self.categories)))

        bugs = db.select([Bug.id, Bug.photo_path, Bug.description, Bug.location, BugStatus.status]).select_from(query)

        for bug in await bugs.gino.all():
            response.append({
                'id': bug.id,
                'photo_img': bug.photo_path,
                'description': bug.description,
                'location': bug.location,
                'status': bug.status
            })

        return web.json_response(response)
