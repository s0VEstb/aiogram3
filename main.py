from config import dp, bot
import asyncio
from handlers import setup_routers
from database.a_db import AsyncDatabase


async def main():
    db = AsyncDatabase()
    await db.create_tables()
    router = setup_routers()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())