import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.deep_linking import create_start_link

from config import bot, ADMIN_ID, MEDIA_PATH
from database import sql_queries
from database.a_db import AsyncDatabase
from consts import start_text
from keyboards.start import start_menu_keyboard
router = Router()


@router.message(Command('start'))
async def start(message: types.Message, db=AsyncDatabase()):

    token = message.text.split()
    if len(token) > 1:
        await reference_start_link(token[1], message)

    try:
        await db.execute_query(
            query=sql_queries.INSERT_USER_QUERY,
            params=(
                None,
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name,
                None,
                0
            ),
            fetch='none'
        )
    except sqlite3.IntegrityError:
        pass
    animation_file = types.FSInputFile(MEDIA_PATH + "bot-ani.gif")
    await bot.send_animation(
        chat_id=message.from_user.id,
        animation=animation_file,
        caption=start_text.format(message.from_user.first_name),
        reply_markup=await start_menu_keyboard()
    )


@router.message(lambda message: message.text == 'SIUUU')
async def admin_panel(message: types.Message, db=AsyncDatabase()):
    if int(ADMIN_ID) == message.from_user.id:
        users = await db.execute_query(
            query=sql_queries.SELECT_ALL_USERS_QUERY,
            params=None,
            fetch='all'
        )
        user_first_name = "\n".join([user["FIRST_NAME"] for user in users])
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"Here is your Admin Page:\n{user_first_name}",
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You are not a Admin ("
        )


async def reference_start_link(token, message, db=AsyncDatabase()):
    link = await create_start_link(bot=bot, payload=token)
    owner = await db.execute_query(
        query=sql_queries.SELECT_REFERENCE_LINK_QUERY,
        params=(link,),
        fetch='one'
    )
    if owner['TELEGRAM_ID'] == message.from_user.id:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You can not use your own link!"
        )
        return
    try:
        await db.execute_query(
            query=sql_queries.INSERT_REFERENCE_TABLE_QUERY,
            params=(
                None,
                owner['TELEGRAM_ID'],
                message.from_user.id
            ),
            fetch='none'
        )
        await db.execute_query(
            query=sql_queries.UPDATE_USER_BALANCE_QUERY,
            params=(owner['TELEGRAM_ID'],),
            fetch='none'
        )
        await bot.send_message(
            chat_id=owner["TELEGRAM_ID"],
            text="You have new reference! 😍\n"
            'Congratulate!!!'
        )
    except sqlite3.IntegrityError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="You have used this link!"
        )
