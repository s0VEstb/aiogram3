import random
from aiogram import Router, types
from aiogram.types import FSInputFile
from config import bot
from database import sql_queries
from consts import profile_text
from database.a_db import AsyncDatabase
from keyboards.like_dislike import like_dislike_keyboard
router = Router()


@router.callback_query(lambda call: call.data == 'view_profiles')
async def view_random_profiles(call: types.CallbackQuery, db=AsyncDatabase()):
    if call.message.caption.startswith('Nickname'):
        await call.message.delete()
    profiles = await db.execute_query(
        query=sql_queries.SELECT_ALL_PROFILES_QUERY,
        params=(
            call.from_user.id,
            call.from_user.id
        ),
        fetch='all'
    )
    if profiles:
        random_profile = random.choice(profiles)
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
            reply_markup=await like_dislike_keyboard(tg_id=random_profile['TELEGRAM_ID'])
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You have liked all profiles, come later'
        )


@router.callback_query(lambda call: "like_" in call.data)
async def like_detect_call(call: types.CallbackQuery, db=AsyncDatabase()):
    owner_tg_id = call.data.replace('like_', '')
    await db.execute_query(
        query=sql_queries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            1
        ),
        fetch='none'
    )
    await view_random_profiles(call=call)


@router.callback_query(lambda call: "disl_" in call.data)
async def dislike_detect_call(call: types.CallbackQuery, db=AsyncDatabase()):
    owner_tg_id = call.data.replace('disl_', '')
    await db.execute_query(
        query=sql_queries.INSERT_LIKE_QUERY,
        params=(
            None,
            owner_tg_id,
            call.from_user.id,
            0
        ),
        fetch='none'
    )
    await view_random_profiles(call=call)
