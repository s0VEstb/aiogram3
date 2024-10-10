from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def start_menu_keyboard():
    reqistration_button = InlineKeyboardButton(
        text='Registration 👾',
        callback_data='registration'
    )
    view_profiles_button = InlineKeyboardButton(
        text='View Profiles 🎲',
        callback_data='view_profiles'
    )
    my_profile_button = InlineKeyboardButton(
        text='My Profile ☠️',
        callback_data='my_profile'
    )
    reference_menu_button = InlineKeyboardButton(
        text='Reference Menu 🤪️',
        callback_data='reference_menu'
    )
    liked_history_button = InlineKeyboardButton(
        text='Liked Profiles 🩵',
        callback_data='history'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [reqistration_button],
            [view_profiles_button],
            [my_profile_button],
            [reference_menu_button],
            [liked_history_button],
        ]
    )
    return markup
