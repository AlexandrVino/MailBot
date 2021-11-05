import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    """
    :param dp: Dispatcher
    :returns: None
    function, which will notify admins about launch bot
    """
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot Launched")

        except Exception as err:
            logging.exception(err)
