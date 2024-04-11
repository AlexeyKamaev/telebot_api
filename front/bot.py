import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_reader import config
from handlers import ending, my_conditions, cian_id_search, base, random

TOKEN=config.bot_token.get_secret_value()

async def main(TOKEN=TOKEN):

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp.include_routers(base.router, cian_id_search.router, my_conditions.router, ending.router, random.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__": 
    asyncio.run(main())
