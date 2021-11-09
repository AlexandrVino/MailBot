import asyncio
import logging
from datetime import datetime, timedelta
from json import loads, dumps
from os import remove

from asyncpg import Record
from aiogram.types.input_file import InputFile

from loader import db, dp
from utils.misc.get_dict import datetime_to_dict
from utils.misc.gmail_api import get_inbox
from aiogram.utils.exceptions import CantParseEntities, CantInitiateConversation


async def check_updates() -> None:
    """
    :param: None
    :return: None

    Function, which in endless cycle takes user from database
    And parse his mails with interval in 1 minute
    """

    while True:
        users: list[Record] = await db.get_users()
        if users is None:  # No any users yet
            continue
        files = []
        for user in users:
            now_delta = timedelta(**await datetime_to_dict(datetime.now()))

            if user.get('mails') is None:  # user haven't any mail yet
                continue
            if not (user.get('last_search') is None or now_delta - timedelta(**loads(user.get('last_search'))) >
                    timedelta(minutes=1)):  # even 30 minutes parse all user mails
                continue

            for mail in loads(user.get('mails')):
                messages: list[dict] = await get_inbox(
                    username=mail['address'],
                    password=mail['password'],
                    path='data/static/'
                )

                for message in messages:

                    for chat_id in mail['send_to']:
                        try:
                            # send mail message
                            await dp.bot.send_message(chat_id, message['body'])

                            # if mail have some files
                            if message.get('files') is not None:
                                for i, file_name in enumerate(message.get('files')):
                                    try:
                                        file = InputFile(file_name)
                                    except FileNotFoundError:
                                        continue
                                    files += [file_name]
                                    await dp.bot.send_document(chat_id=chat_id, document=file)
                        except (CantParseEntities, CantInitiateConversation):
                            pass

            await db.update_user_last_search(**{
                'chat_id': user.get('chat_id'),
                'last_search': dumps(await datetime_to_dict(datetime.now()))
            })

        for file_name in files:
            try:
                remove(file_name)
            except FileNotFoundError:
                continue


        await asyncio.sleep(60)
