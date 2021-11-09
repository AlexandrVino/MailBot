from keyboards.inline.callback_datas import mail_callback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_mail_keyboard(data: [dict]) -> InlineKeyboardMarkup or bool:
    """
    ::param data: list with json objects (name: str - name of a computer, mac: str - MAC address of current pc)
    ::param data:example: [{'address': 'foo@example.com', 'password': '123321'}]
    ::returns: inline keyboard with computers added to the list
    """

    keyboard = InlineKeyboardMarkup(row_width=1)
    for button_data in data:
        del button_data['send_to']
        keyboard.insert(InlineKeyboardButton(button_data['address'], callback_data=mail_callback.new(**button_data)))
    keyboard.row(InlineKeyboardButton('Cancel', callback_data='cancel'))

    return keyboard


