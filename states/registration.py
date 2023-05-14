from aiogram.dispatcher.filters.state import (
    StatesGroup,
    State
)


class Registration(StatesGroup):
    username = State()
    email = State()
    chat_id_user = State()
    repeat_registration = State()
    info = {}
