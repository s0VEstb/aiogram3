import binascii
import os
from aiogram import Router, types
from aiogram.utils.deep_linking import create_start_link
from config import bot
from database import sql_queries
from database.a_db import AsyncDatabase
from keyboards.reference import reference_menu_keyboard
router = Router()


@router.callback_query(lambda call: call.data == 'reference_menu')
async def reference_menu(call: types.CallbackQuery, db=AsyncDatabase()):
    await bot.send_message(
        chat_id=call.from_user.id,
        text='Here is your Reference Menu',
        reply_markup=await reference_menu_keyboard()
    )


@router.callback_query(lambda call: call.data == 'link')
async def reference_link(call: types.CallbackQuery, db=AsyncDatabase()):
    token = binascii.hexlify(os.urandom(8)).decode()
    link = await create_start_link(bot=bot, payload=token)
    user = await db.execute_query(
        query=sql_queries.SELECT_ALL_ALL_USERS_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    if user['REFERENCE_LINK']:
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Here is your old link: {user['REFERENCE_LINK']}"
        )
    else:
        await db.execute_query(
            query=sql_queries.UPDATE_USER_LINK_QUERY,
            params=(
                link,
                call.from_user.id,
            ),
            fetch='none'
        )
        await bot.send_message(
            chat_id=call.from_user.id,
            text=f"Here is your new link: {link}"
        )


@router.callback_query(lambda call: call.data == 'my_balance')
async def my_balance(call: types.CallbackQuery, db=AsyncDatabase()):
    user = await db.execute_query(
        query=sql_queries.SELECT_ALL_ALL_USERS_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    balance = user.get("BALANCE", 0)
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Here is your Balance: {balance}"
    )


@router.callback_query(lambda call: call.data == 'my_references')
async def my_references(call: types.CallbackQuery, db=AsyncDatabase()):
    references = await db.execute_query(
        query=sql_queries.SELECT_ALL_REFERENCES_QUERY,
        params=(call.from_user.id,),
        fetch='all'
    )

    if references:
        references_list = []

        for reference in references:
            reference_name = await db.execute_query(
                query=sql_queries.SELECT_REFERENCE_FIRSTNAME_QUERY,
                params=(reference['REFERENCE_TELEGRAM_ID'],),
                fetch='one'
            )
            references_list.append(reference_name['FIRST_NAME'])
            reference_names_str = "\n".join(references_list)
            await bot.send_message(
                chat_id=call.from_user.id,
                text=f"Here are your references:\n{reference_names_str} - {reference['REFERENCE_TELEGRAM_ID']}"
            )

    else:
        await bot.send_message(
            chat_id=call.from_user.id,
            text="You have no references."
        )
