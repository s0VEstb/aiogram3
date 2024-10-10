from aiogram import Router, types
from config import bot
from database import sql_queries
from database.a_db import AsyncDatabase
from aiogram.fsm.state import StatesGroup, State

from aiogram.fsm.context import FSMContext
router = Router()


class DonateProcess(StatesGroup):
    donate = State()


@router.callback_query(lambda call: 'donate_' in call.data)
async def donate_view(call: types.CallbackQuery, state: FSMContext, db=AsyncDatabase()):
    recipient_id = call.data.replace('donate_', '')
    owner = await db.execute_query(
        query=sql_queries.SELECT_ALL_ALL_USERS_QUERY,
        params=(
            call.from_user.id,
        ),
        fetch='one'
    )
    balance = owner.get("BALANCE", 0)
    await bot.send_message(
        chat_id=call.from_user.id,
        text=f'How much money do you want to send? \n'
             f'Your Balance: {balance}'
    )
    await state.update_data(owner_id=recipient_id)
    await state.update_data(balance_limit=owner["BALANCE"])
    await state.set_state(DonateProcess.donate)



@router.message(DonateProcess.donate)
async def validate_donate(message: types.Message, state: FSMContext, db=AsyncDatabase()):
    data = await state.get_data()
    try:
        if int(message.text) <= int(data["balance_limit"]):
            await db.execute_query(
                query=sql_queries.UPDATE_DONATE_BALANCE_QUERY,
                params=(
                    message.text,
                    message.from_user.id
                ),
                fetch='none'
            )
            await db.execute_query(
                query=sql_queries.UPDATE_RECEPIENT_BALANCE_QUERY,
                params=(
                    message.text,
                    data['owner_id'],
                ),
                fetch='none'
            )
            await db.execute_query(
                query=sql_queries.INSERT_DONATE_QUERY,
                params=(
                    None,
                    message.from_user.id,
                    data['owner_id'],
                    message.text
                ),
                fetch='none'
            )
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You have successfully donated money 🥳"
            )
            await bot.send_message(
                chat_id=data['owner_id'],
                text="Somebody donated you money! \n"
                     f"Amount: {message.text}"
            )
        else:
            await bot.send_message(
                chat_id=message.from_user.id,
                text="You do not have enough money 😥"
            )
    except ValueError:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Please use a numeric value 😡"
        )
