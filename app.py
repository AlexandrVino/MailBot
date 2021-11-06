from json import loads

from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.misc.check_updates import check_updates
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from datetime import datetime, timedelta
from utils.misc.get_dict import datetime_to_dict


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)  # set default commands
    await on_startup_notify(dispatcher)  # notify admins about startup


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

