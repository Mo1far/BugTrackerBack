from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User

from bot.chains.base.kb import start_kb
from bot.core import dp


@dp.message_handler(commands='start', state='*')
async def start_command(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer(f'Привіт,  {User.get_current().first_name}', reply_markup=start_kb)
