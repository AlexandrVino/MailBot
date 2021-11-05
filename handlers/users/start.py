from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db
from utils.misc.get_dict import get_dict


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    """
    :param message: aiogram.types.Message
    :returns: None
    function, which will register new user
    """
    await db.get_user_or_create(**await get_dict(**message.from_user.values))
    await message.answer(f"Hi, {message.from_user.full_name}!")
