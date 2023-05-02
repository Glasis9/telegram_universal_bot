from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from api.weather_api import give_current_weather
from states import Weather
from keyboards.inline_keyboard import inline_keyboard_exit_weather
from keyboards.keyboard import keyboard


@dp.message_handler(commands=["weather"])
async def give_weather(message: types.Message):
    await message.answer(text="Input your city:", reply_markup=inline_keyboard_exit_weather)
    await Weather.city.set()


@dp.message_handler(state=Weather.city)
async def weather(message: types.Message, state: FSMContext):
    _weather = give_current_weather(message.text)
    if _weather != "The city is not found":
        await message.reply(text=f"{_weather}", reply_markup=keyboard)
        await state.finish()
    else:
        await message.answer(text="The city is not found, repeat input:")
        await give_weather(message)
        await state.finish()


@dp.callback_query_handler(text="exit_weather", state="*")
async def exit_weather(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer(text="Exit", reply_markup=keyboard)
