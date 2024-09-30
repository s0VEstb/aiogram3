from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from config import bot
from database import sql_queries
from consts import profile_text
from database.a_db import AsyncDatabase
from keyboards.my_profile import my_profile_keyboard
router = Router()


@router.callback_query(lambda call: call.data == 'my_profile')
async def view_my_profiles(call: types.CallbackQuery, db=AsyncDatabase()):
    profile = await db.execute_query(
        query=sql_queries.SELECT_ONE_PROFILE_QUERY,
        params=(call.from_user.id,),
        fetch='one'
    )
    if profile:
        photo = FSInputFile(profile['PHOTO'])
        await bot.send_photo(
            chat_id=call.from_user.id,
            photo=photo,
            caption=profile_text.format(
                nickname=profile['NICKNAME'],
                bio=profile['BIO'],
                is_married=profile['IS_MARRIED'],
                male=profile['MALE']
            ),
            reply_markup=await my_profile_keyboard()
        )
    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text='You dont have profile, pls go register )'
        )


class DeleteProfileState(StatesGroup):
    confirm = State()


@router.callback_query(lambda call: call.data == 'delete_profile')
async def ask_delete_confirmation(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('You really want to delete your profile? Reply with "yes" or "no".')
    await state.set_state(DeleteProfileState.confirm)


@router.message(DeleteProfileState.confirm)
async def delete_profile(message: types.Message, db=AsyncDatabase()):
    if message.text.lower() == 'yes':
        await db.execute_query(
            query=sql_queries.DELETE_PROFILE_QUERY,
            params=(message.from_user.id,),
            fetch='none'
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='You have deleted your profile!'
        )
    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Deleting cancelled!!!'
        )
