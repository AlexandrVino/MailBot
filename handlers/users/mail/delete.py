import json

from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.callback_datas import mail_callback
from keyboards.inline.mail import get_mail_keyboard
from loader import dp, db
from utils.misc.get_dict import get_dict


@dp.message_handler(Command('delete_mail'))
async def choose_computer(message: types.Message):
    """
    :param message: aiogram.types.Message - user message
    :returns: None
    """

    data = await db.get_user_mails(chat_id=message.from_user.id)
    data = json.loads(data)
    if any(data):
        await message.answer(f"Choose any of mails:",
                             reply_markup=await get_mail_keyboard(data))
    else:
        await message.answer(f"You haven't any mails yet")


@dp.callback_query_handler(mail_callback.filter())
async def on_pc_callback(call: types.CallbackQuery, callback_data: dict):
    """
    :param call: aiogram.types.CallbackQuery - callback (button which push user)
    :param callback_data: dict
    :returns: None
    function, which will delete pc
    """

    await call.answer(cache_time=60)
    _, address, send_to, password = callback_data.values()

    kwargs = await get_dict(**call.from_user.values)
    mails = [pc for pc in json.loads(await db.get_user_mails(**kwargs)) if pc['address'] != address]
    kwargs['mails'] = json.dumps(mails)
    await db.update_user_mails(**kwargs)

    if any(mails):
        await call.message.edit_reply_markup(
            reply_markup=await get_mail_keyboard(mails))

    else:
        await call.message.edit_reply_markup()
        await call.message.edit_text(f'Delete successfully!')
