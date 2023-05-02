from aiogram.dispatcher.filters.state import StatesGroup, State


class PhotoLikeDislike(StatesGroup):
    previous_photo = bool
    photo = {}
