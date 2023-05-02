from aiogram.dispatcher.filters.state import StatesGroup, State


class Weather(StatesGroup):
    city = State()
