from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = (
        "List of commands: ",
        "/start - Start dialog",
        "/help - Get bot skills",
        "/add_mail add mail address",
        "/delete_mail delete mail address"
    )

    await message.answer("\n".join(text))
