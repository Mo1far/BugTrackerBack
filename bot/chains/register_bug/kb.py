from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Скасувати', callback_data='bug_register_cancel')]
    ],
    resize_keyboard=True)


def get_admin_decision_kb(bug_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Узгодити ✅', callback_data=f'admin_decision_registered_{bug_id}'),
             InlineKeyboardButton('Відхилити ❌', callback_data=f'admin_decision_dropped_{bug_id}')]
        ],
        resize_keyboard=True
    )
