import json
import os

from aiohttp import web
from sqlalchemy import and_

from api.config import UPLOADS_DIR
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
    def categories(self):
        return set(json.loads(self.request.query.get('categories')))

    @property
    def page(self):
        return max(int(self.request.query.get('page', 1)), 0)

    @property
    def per_page(self):
        return min(int(self.request.query.get('per_page', 20)), 100)

    @property
    def limit(self):
        return self.per_page

    @property
    def offset(self):
        return (self.page - 1) * self.per_page

    async def get(self):
        response = {}

        query = Bug.join(BugStatus, and_(Bug.status == BugStatus.id,
                                         BugStatus.status.in_(
                                             self.categories)))

        bugs = db.select([Bug.id, Bug.photo_path, Bug.description, Bug.location, BugStatus.status]) \
            .limit(self.limit).offset(self.offset).order_by(Bug.created_at.desc()) \
            .select_from(query)

        response['data'] = []
        for bug in await bugs.gino.all():
            response['data'].append({
                'id': bug.id,
                'photo_img': os.path.join(UPLOADS_DIR, bug.photo_path),
                'description': bug.description,
                'location': bug.location,
                'status': bug.status
            })

        response['page'] = self.page

        return web.json_response(response)
