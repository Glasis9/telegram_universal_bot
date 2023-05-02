from aiogram.dispatcher.filters.state import StatesGroup, State


class Count(StatesGroup):
    count = State()
