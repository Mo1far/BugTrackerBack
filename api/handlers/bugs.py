import json
import os

from aiohttp import web
from sqlalchemy import and_

from api.config import UPLOADS_DIR
from db import Bug, db
from db.config import UPLOAD_DIR
from db.models import BugStatus

import time


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

    async def post(self):
        data = await self.request.post()
        if not 3 < len(data["location"]) < 50:
            return web.json_response({"error": {"field": "location",
                                                "desc": "location len must be between 3 and 50 chars"}})
        if not 3 < len(data["description"]) < 3000:
            return web.json_response({"error": {"field": "description",
                                                "desc": "description len must be between 3 and 50 chars"}})
        if data["image"].content_type not in ("image/png", "image/jpg"):
            return web.json_response({"error": {"field": "image",
                                                "desc": "Allowed content types is png and jpg"}})

        file_type = data["image"].content_type.lstrip("image/")
        filename = f"{int(time.time())}.{file_type}"
        filepath = os.path.join(UPLOAD_DIR, f'bugs/{filename}')

        with open(filepath, "wb") as file:
            while True:
                chunk = data["image"].file.read()  # 8192 bytes by default.
                if not chunk:
                    break

                file.write(chunk)

        default_status = await BugStatus.select('id').where(BugStatus.status == 'pending').gino.scalar()
        bug = await Bug.create(photo_path=f'bugs/{filename}',
                               description=data['description'],
                               location=data["location"],
                               status=default_status,
                               user=None)

        response = {'id': bug.id,
                    'photo_path': f'bugs/{filename}',
                    'description': bug.description,
                    'location': bug.location,
                    'status': default_status
                    }
        return web.json_response(response)
