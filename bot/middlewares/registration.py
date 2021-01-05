from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import User as TgUser

from db import User


class RegistrationMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self):
        super(RegistrationMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message

        :param data:
        :param message:
        """
        tg_user = TgUser().get_current()
        if not await User.exist(tg_user):
            await User.create(id=tg_user,
                              locale=tg_user.locale.language)
