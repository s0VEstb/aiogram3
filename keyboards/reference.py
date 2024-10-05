from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


async def reference_menu_keyboard():
    link_button = InlineKeyboardButton(
        text='Link 👑',
        callback_data='link'
    )
    my_balance_button = InlineKeyboardButton(
        text='My Balance 💰',
        callback_data='my_balance'
    )
    my_references_button = InlineKeyboardButton(
        text='My References 😗',
        callback_data='my_references'
    )
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [link_button],
            [my_balance_button],
            [my_references_button],
        ]
    )
    return markup