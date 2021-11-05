import json
from re import findall

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp, db
from states.mails import *
from utils.misc.get_dict import get_dict
from validate_email import validate_email


@dp.message_handler(Command('add_mail'))
async def add_pc(message: types.Message) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message
    :returns: types.Message.answer
    function, which will start add_pc state and ask computer name
    """

    await AddMailForm.address.set()
    return await message.answer("Please write mail address")


@dp.message_handler(state=AddMailForm.address)
async def process_name(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message - message, which send user 
    :param state: aiogram.dispatcher.FSMContext - storage with data
    :return: types.Message.answer
    function, which will ask computer mac address
    """
    address = message.text
    if not validate_email(address):
        return await message.answer("Incorrect mail address (Example: foo@example.com)")

    mails = json.loads(await db.get_user_mails(**await get_dict(**message.from_user.values)))

    if any([item.get("address") == address for item in mails]):
        return await message.answer("Mail with this address have already added")

    async with state.proxy() as mails_data:
        mails_data['address'] = address

    await AddMailForm.send_to.set()
    return await message.answer("Please write for whom send notify")


@dp.message_handler(state=AddMailForm.send_to)
async def process_name(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message - message, which send user
    :param state: aiogram.dispatcher.FSMContext - storage with data
    :return: types.Message.answer
    function, which will ask computer mac address
    """
    send_to = message.text.replace(' ', "").replace(';', ",").split(',')
    if not all([chat_id.isdigit() for chat_id in send_to]):
        return await message.answer("Incorrect ides (Example: 568940763, 1025634)")
    async with state.proxy() as mails_data:
        mails_data['send_to'] = [int(chat_id) for chat_id in send_to]

    await AddMailForm.password.set()
    return await message.answer("Please write password")


@dp.message_handler(state=AddMailForm.password)
async def process_mac(message: types.Message, state: FSMContext) -> types.Message.answer:
    """
    :param message: aiogram.types.Message - user message - message, which send user
    :param state: aiogram.dispatcher.FSMContext - storage with data
    :return: types.Message.answer
    function, which will add computer to database
    """
    password = message.text

    kwargs = await get_dict(**message.from_user.values)
    user_mails = await db.get_user_mails(**kwargs)
    user_mails = json.loads(user_mails)

    async with state.proxy() as computer_data:
        computer_data['password'] = password
        user_mails += [{key: value for key, value in computer_data._data.items()}]
    kwargs['mails'] = json.dumps(user_mails)
    await db.update_user_mails(**kwargs)
    await state.finish()

    return await message.answer("Mail added successfully")
