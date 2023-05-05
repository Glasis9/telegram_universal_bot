from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [KeyboardButton("/give_photo"), KeyboardButton("/give_joke")],
    [KeyboardButton("/give_number"), KeyboardButton("/give_letter")],
    [KeyboardButton("/weather"), KeyboardButton("/count_it")],
    [KeyboardButton("/registration")]
])
