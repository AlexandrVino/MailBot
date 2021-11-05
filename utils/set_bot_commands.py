from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Launch bot"),
            types.BotCommand("help", "Display skills"),
            types.BotCommand("add_mail", "Get info about your account"),
            types.BotCommand("delete_mail", "Reset you server address")
        ]
    )
