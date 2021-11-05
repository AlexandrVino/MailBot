import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.sql import create_pool, DBSession

loop = asyncio.get_event_loop()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

db: DBSession = dp.loop.run_until_complete(
    create_pool(
        # host='database',  # database container name
        host=config.DB_HOST,  # database host, when you launch bot on you localhost
        user=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        port=config.DB_PORT,
        path='utils/db_api/'))
