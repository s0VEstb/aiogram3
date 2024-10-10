import random

from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from config import bot
from database import sql_queries
from consts import profile_text
from database.a_db import AsyncDatabase
from keyboards.like_dislike import history_keyboard
from keyboards.my_profile import my_profile_keyboard
router = Router()


@router.callback_query(lambda call: call.data == 'history')
async def liked_history(call: types.CallbackQuery, db=AsyncDatabase()):
    profiles = await db.execute_query(
        query=sql_queries.SELECT_LIKED_PROFILES_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='all'
    )
    if profiles != []:
        randomizer = random.choice(profiles)
        random_profile = await db.execute_query(
            query=sql_queries.SELECT_ONE_PROFILE_QUERY,
            params=(
                randomizer['OWNER_ID'],
            ),
            fetch='one'
        )
        photo = FSInputFile(random_profile['PHOTO'])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=profile_text.format(
                nickname=random_profile['NICKNAME'],
                bio=random_profile['BIO'],
                is_married=random_profile['IS_MARRIED'],
                male=random_profile['MALE']
            ),
            reply_markup=await history_keyboard(random_profile['TELEGRAM_ID'])
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You have not liked profiles.'
        )