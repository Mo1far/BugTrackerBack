from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterBug(StatesGroup):
    wait_photo = State()
    wait_location = State()
    wait_description = State()
    wait_admin_description = State()
    message = State()
    bug = State()
