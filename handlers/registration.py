from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline_keyboard import (
    inline_keyboard_exit_registration,
    inline_keyboard_check_user_data
)
from keyboards.keyboard import keyboard
from aiogram.types import ReplyKeyboardRemove
from loader import dp
from states.registration import Registration


@dp.message_handler(commands=["registration"])
async def registration(message: types.Message):
    if message.chat.id in Registration.info:
        await message.answer(
            text="You are already registered",
            reply_markup=inline_keyboard_check_user_data
        )
    else:
        await message.answer(
            text="Please, input your username:",
            reply_markup=inline_keyboard_exit_registration
        )
        await Registration.username.set()  # Задаем состояние, которое будем отлавливать


@dp.message_handler(state=Registration.username)
async def input_username(message: types.Message, state: FSMContext):
    _username = message.text

    # await state.update_data(username=username)  # 1-й вариант сохранения данных в FSM

    # await state.update_data(
    #     {
    #         "username": username
    #     }
    # )  # 2-й вариант сохранения данных в FSM

    async with state.proxy() as data:  # асинхронный генератор
        data["username"] = _username  # 3-й вариант сохранения данных в FSM

    await message.answer(text="Please, input your email:", reply_markup=ReplyKeyboardRemove())
    await Registration.email.set()  # Задаем состояние, которое будем отлавливать


@dp.message_handler(state=Registration.email)
async def input_email(message: types.Message, state: FSMContext):
    _email = message.text
    await state.update_data(email=_email)

    data = await state.get_data()  # Получаем данные из FSM
    _username = data.get("username")
    _email = data.get("email")
    await message.answer(text=f"Your username: {_username}\n"
                              f"Your email: {_email}")

    await message.answer(text="All right? (Yes/No)")
    await Registration.chat_id_user.set()  # Задаем состояние, которое будем отлавливать


@dp.message_handler(state=Registration.chat_id_user)
async def save_chat_id_user(message: types.Message, state: FSMContext):
    answer = message.text.lower()

    if answer == "yes":
        get_user_data = await state.get_data()
        username = get_user_data.get("username")
        email = get_user_data.get("email")
        chat_id_user = message.chat.id
        await state.update_data(chat_id_user=chat_id_user)
        await message.answer(text="Thank you for registering!", reply_markup=keyboard)
        Registration.info[chat_id_user] = [username, email]
        return await state.finish()
    elif answer == "no":
        return await registration(message)
    else:
        await message.answer(text="Incorrect answer!")
        await message.answer(text="You want to repeat the registration? (Yes/No)")
        return await Registration.repeat_registration.set()  # Задаем состояние, которое будем отлавливать


@dp.message_handler(state=Registration.repeat_registration)
async def repeat_registration(message: types.Message, state: FSMContext):
    answer = message.text.lower()

    if answer == "yes":
        del Registration.info[message.chat.id]
        return await registration(message)
    if answer == "no":
        await message.answer(text="Exit", reply_markup=keyboard)
        return await state.finish()
    else:
        await message.answer(text="Incorrect answer!")
        await message.answer(text="You want to repeat the registration? (Yes/No)")
        return await repeat_registration(message)


@dp.callback_query_handler(text="exit_registration", state="*")
# state="*" ловит все состояния, указывать обязательно при работе с FSM
async def exit_registration(callback: types.CallbackQuery, state: FSMContext):
    # if state is None:  # Проверяем состояние FSM
    #     return
    await callback.message.reply(text="You cancelled the registration", reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text="exit_reg", state="*")
# state="*" ловит все состояния, указывать обязательно при работе с FSM
async def exit_reg(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.reply(text="Exit", reply_markup=keyboard)
    await state.finish()


@dp.callback_query_handler(text="check_data")
async def check_data(callback: types.CallbackQuery):
    _user_data = Registration.info[callback.message.chat.id]
    _username = _user_data[0]
    _email = _user_data[1]
    await callback.message.answer(text=f"Your username: {_username}\n"
                                       f"Your email: {_email}")
    await callback.message.answer(text="Do you want to change the data? (Yes/No)")
    await Registration.repeat_registration.set()
