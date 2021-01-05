from aiohttp import web

from db import Bug
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
