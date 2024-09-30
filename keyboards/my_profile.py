from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def my_profile_keyboard():
    edit_profile_button = InlineKeyboardButton(
        text='Edit 🫵',
        callback_data=f'edit_profile'
    )
    delete_profile_button = InlineKeyboardButton(
        text='Delete 🎃',
        callback_data=f'delete_profile'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [edit_profile_button],
            [delete_profile_button],
        ]
    )
    return markup
