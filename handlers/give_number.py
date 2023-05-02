import random

from loader import dp
from aiogram import types
from keyboards.keyboard import keyboard


@dp.message_handler(commands=["give_number"])
async def give_number(message: types.Message):
    await message.answer(
        text=f"Hold the number: '{str(random.randint(1, 13))}'",
        reply_markup=keyboard
    )
