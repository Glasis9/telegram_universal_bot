from aiogram.utils.exceptions import InvalidHTTPUrlContent

from loader import dp
from aiogram import types
from api.random_joke_api import give_random_joke
from keyboards.keyboard import keyboard


@dp.message_handler(commands=["give_joke"])
async def give_joke(message: types.Message):
    try:
        await message.answer(text=f"{give_random_joke()}", reply_markup=keyboard)
    except InvalidHTTPUrlContent:
        await message.answer(text="Connection error", reply_markup=keyboard)
