import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import User as TgUser

from bot.chains.base.kb import start_kb
from bot.chains.register_bug.kb import cancel_kb, get_admin_decision_kb
from bot.chains.register_bug.state import RegisterBug
from bot.config import ADMIN_CHAT_ID
from bot.core import dp, bot
from db.config import UPLOAD_DIR
from db.models.bug import Bug, BugStatus


@dp.callback_query_handler(lambda x: x.data == 'bug_register_cancel', state='*')
async def cancel(c: types.CallbackQuery, state: FSMContext):
    await c.message.delete_reply_markup()
    await state.finish()
    await bot.send_message(c.from_user.id, 'Скасовано', reply_markup=start_kb)
    await c.answer('Скасовано')


@dp.message_handler(regexp='Додати баг 🐞', state='*')
async def add_bug_start(msg: types.Message, state: FSMContext):
    await RegisterBug.wait_photo.set()
    data_state = await msg.answer('Надішліть фото багу 📸', reply_markup=cancel_kb)
    await state.update_data({'message': data_state})


@dp.message_handler(state=RegisterBug.wait_photo, content_types=['photo', 'video', 'document'])
async def add_bug_photo(msg: types.Message, state: FSMContext):
    data_state = await state.get_data()
    await data_state.get('message').delete_reply_markup()
    if len(msg.photo) == 0:
        await msg.answer('Упсс.. Помилка 😔\n'
                         'Спробуйте надіслати фото, або скасуйте додавання багу', reply_markup=cancel_kb)

    await state.update_data({'photo': msg.photo[-1]})
    await RegisterBug.wait_description.set()
    answer = await msg.answer('Опишіть проблему в 1 повідомленні', reply_markup=cancel_kb)
    await state.update_data({'message': answer})


@dp.message_handler(state=RegisterBug.wait_description)
async def add_bug_description(msg: types.Message, state: FSMContext):
    data_state = await state.get_data()
    await data_state.get('message').delete_reply_markup()
    await state.update_data({'description': msg.text})
    await RegisterBug.wait_location.set()
    answer = await msg.answer('Надішліть місцезнаходження (аудиторію, корпус) якомога конкретніше 🏢',
                              reply_markup=cancel_kb)
    await state.update_data({'message': answer})


@dp.message_handler(state=RegisterBug.wait_location)
async def add_bug_location(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await data.get('message').delete_reply_markup()
    default_status = await BugStatus.select('id').where(BugStatus.status == 'pending').gino.scalar()

    photo = data.get('photo')

    bug = await Bug.create(photo_path=photo.file_id,
                           description=data.get('description'),
                           location=msg.text,
                           status=default_status,
                           user=TgUser.get_current())

    photo_path = os.path.join(UPLOAD_DIR, f'bugs/{bug.id}.jpg')
    await photo.download(photo_path)
    await bug.update(photo_path=f'bugs/{bug.id}.jpg').apply()

    await bot.send_photo(ADMIN_CHAT_ID, photo.file_id, caption=f'Баг №{bug.id}\n'
                                                               f'Місцезнаходження: <i>{msg.text}</i>\n'
                                                               f'Опис: "<i>{data.get("description")}</i>"',
                         reply_markup=get_admin_decision_kb(bug.id))

    await state.finish()
    await msg.answer(f'Баг № {bug.id} було надіслано адмінам. '
                     f'Найближчим часом інформацію перевірять, та сповістять вас\n\n'
                     f'Дякуємо за повідомлення 😊')


@dp.callback_query_handler(lambda x: x.data.startswith('admin_decision_'))
async def admin_decision_(cq: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'RegisterBug:wait_admin_description':
        state_data = await state.get_data()
        bug_id = state_data['bug'].id

        await cq.message.answer(f'Спочатку дайте пояснення багу №{bug_id}')
        return await cq.answer('Заборонено')

    c_data = cq.data.replace('admin_decision_', '')
    decision, bug_id = c_data.split('_')
    bug = await Bug.get(int(bug_id))
    status = await BugStatus.select('id').where(BugStatus.status == decision).gino.scalar()
    if decision == 'registered':
        await bot.edit_message_caption(ADMIN_CHAT_ID,
                                       message_id=cq.message.message_id,
                                       caption=cq.message.caption + '\n\nБаг прийнято в роботу ✅')
        await bot.send_message(bug.user, f'Баг № {bug.id}'
                                         f' прийнято в роботу, будемо старатися пофіксити його найближчим часом 😉')
        await cq.answer('Прийнято в роботу')
    else:
        await bot.edit_message_caption(ADMIN_CHAT_ID,
                                       message_id=cq.message.message_id,
                                       caption=cq.message.caption + '\n\nБаг відхилено ❌')

        await bot.send_message(ADMIN_CHAT_ID, 'Опишіть, чому цей баг відхилено 🤔')
        await RegisterBug.wait_admin_description.set()
        await state.set_data({'bug': bug})
        await cq.answer('Відхилено')

    await bug.update(status=status).apply()


@dp.message_handler(state=RegisterBug.wait_admin_description)
async def cause_text(msg: types.Message, state: FSMContext):
    data_state = await state.get_data()
    await bot.send_message(ADMIN_CHAT_ID, f'Дякуємо! Причина буде передана відправнику!')
    await bot.send_message(data_state.get('bug').user,
                           f'Баг № {data_state.get("bug").id} відхилено 😔\n\nПричина: \"{msg.text}\"')
    await data_state.get('bug').update(cause=msg.text).apply()
    await state.finish()
