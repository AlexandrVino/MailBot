from aiogram.dispatcher.filters.state import State, StatesGroup


class AddMailForm(StatesGroup):
    address = State()
    password = State()
    send_to = State()
