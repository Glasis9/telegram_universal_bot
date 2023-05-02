import random
import string
from loader import dp
from aiogram import types
from keyboards.keyboard import keyboard


@dp.message_handler(commands=["give_letter"])
async def give_letter(message: types.Message):
    await message.answer(
        text=f"Hold the letter: '{random.choice(string.ascii_uppercase)}'",
        reply_markup=keyboard
    )
