import asyncio
from datetime import datetime, timedelta
from json import loads, dumps
from os import remove

from aiogram.types.input_file import InputFile

from loader import db, dp
from utils.misc.get_dict import datetime_to_dict
from utils.misc.gmail_api import *


async def check_updates() -> None:
    while True:
        users = await db.get_users()
        if users is None:
            continue
        for user in users:
            now_delta = timedelta(**await datetime_to_dict(datetime.now()))

            if not (user.get('last_search') is None or now_delta - timedelta(**loads(user.get('last_search'))) >
                    timedelta(minutes=1)):
                continue
            if user.get('mails') is None:
                continue

            for mail in loads(user.get('mails')):
                messages = await get_inbox(username=mail['address'], password=mail['password'], path='data/static/')
                messages = [await reformat_mail(message) for message in messages]
                for message in messages:
                    for chat_id in mail['send_to']:

                        await dp.bot.send_message(chat_id, message['body'])
                        if message.get('files') is not None:
                            for i, file_name in enumerate(message.get('files')):
                                file = InputFile(file_name)
                                await dp.bot.send_document(chat_id=chat_id, document=file)
                                remove(file_name)

            await db.update_user_last_search(**{
                'chat_id': user.get('chat_id'),
                'last_search': dumps(await datetime_to_dict(datetime.now()))
            })
        await asyncio.sleep(60)
