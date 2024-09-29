from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard():
    reqistration_button = InlineKeyboardButton(
        text='Registration 👾',
        callback_data='registration'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [reqistration_button],
        ]
    )
    return markup
