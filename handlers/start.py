import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from config import bot, ADMIN_ID, MEDIA_PATH
from database import sql_queries
from database.a_db import AsyncDatabase
from consts import start_text
from keyboards.start import start_menu_keyboard
router = Router()


@router.message(Command('start'))
async def start(message: types.Message, db=AsyncDatabase()):
    try:
        await db.execute_query(
            query=sql_queries.INSERT_USER_QUERY,
            params=(
                None,
                message.from_user.id,
                message.from_user.username,
                message.from_user.first_name,
                message.from_user.last_name
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
