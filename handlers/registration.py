from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from config import bot
from database import sql_queries
from database.a_db import AsyncDatabase
from consts import profile_text
router = Router()


class RegistrationStates(StatesGroup):
    nickname = State()
    bio = State()
    is_married = State()
    male = State()
    photo = State()


@router.callback_query(lambda call: call.data == 'registration')
async def registration_start(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='1. Send your Nickname !'
    )
    await state.set_state(RegistrationStates.nickname)


@router.callback_query(lambda call: call.data == 'edit_profile')
async def registration_start(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='1. Send your Nickname !'
    )
    await state.set_state(RegistrationStates.nickname)


@router.message(RegistrationStates.nickname)
async def process_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='2. Talk about yourself :)'
    )
    await state.set_state(RegistrationStates.bio)


@router.message(RegistrationStates.bio)
async def process_bio(message: types.Message, state: FSMContext):
    await state.update_data(bio=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='3. Are you married ?'
    )
    await state.set_state(RegistrationStates.is_married)


@router.message(RegistrationStates.is_married)
async def process_is_married(message: types.Message, state: FSMContext):
    if message.text.lower() not in ["yes", "no"]:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Please answer "yes" or "no". Are you married?'
        )
        return
    await state.update_data(is_married=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='4. Write about your male.'
    )
    await state.set_state(RegistrationStates.male)


@router.message(RegistrationStates.male)
async def process_male(message: types.Message, state: FSMContext):
    if message.text.lower() not in ["male", "female"]:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Bro wtf, there is only 2 genders, male or female '
        )
        return
    await state.update_data(male=message.text)
    await bot.send_message(
        chat_id=message.from_user.id,
        text='5. Give me your photo'
    )
    await state.set_state(RegistrationStates.photo)


@router.message(RegistrationStates.photo)
async def process_photo(message: types.Message, state: FSMContext, db=AsyncDatabase()):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(
        file_path,
        'media/' + file_path
    )
    data = await state.get_data()
    photo = FSInputFile('media/' + file_path)
    profile = await db.execute_query(
        query=sql_queries.SELECT_ONE_PROFILE_QUERY,
        params=(message.from_user.id,),
        fetch='one'
    )
    if profile:
        await db.execute_query(
            query=sql_queries.UPDATE_PROFILE_QUERY,
            params=(
                data['nickname'],
                data['bio'],
                data['is_married'],
                data['male'],
                'media/' + file_path,
                message.from_user.id
            ),
            fetch='none'
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='You have successfully re-registered!!!'
        )
    else:
        await db.execute_query(
            query=sql_queries.INSERT_PROFILE_QUERY,
            params=(
                None,
                message.from_user.id,
                data['nickname'],
                data['bio'],
                data['is_married'],
                data['male'],
                'media/' + file_path,
            ),
            fetch='none'
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text='You have successfully registered!!!'
        )

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=photo,
        caption=profile_text.format(
            nickname=data['nickname'],
            bio=data['bio'],
            is_married=data['is_married'],
            male=data['male']
        )
    )
