import sqlite3

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline_keyboard import (
    inline_keyboard_exit_registration,
    inline_keyboard_check_user_data
)
from keyboards.keyboard import keyboard
from aiogram.types import ReplyKeyboardRemove
from loader import dp, db
from states.registration import Registration


@dp.message_handler(commands=["registration"])
async def registration(message: types.Message):

    # Проверка пользователя в словаре Registration.info
    # if message.chat.id in Registration.info:
    #     return await message.answer(
    #         text="You are already registered",
    #         reply_markup=inline_keyboard_check_user_data
    #     )

    # Проверка пользователя на наличие данных в БД sqlite
    user = db.select_user(user_id=message.from_user.id)  # Достаем пользователя из БД sqlite
    if user:  # Проверяем что бы пользователь был в БД иначе None
        return await message.answer(
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

    # Проверяем наличие такого username в БД, если есть,
    # то просим пользователя ввести другой, если нет - продолжаем регистрацию
    if db.select_user(username=_username) is None:

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
    else:
        await message.answer(
            text="This username is already busy, enter another username:",
            reply_markup=inline_keyboard_exit_registration
        )

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
        chat_id_user = message.from_user.id

        await state.update_data(chat_id_user=chat_id_user)
        await message.answer(text="Thank you for registering!", reply_markup=keyboard)

        # Сохраняем данные пользователя в словаре Registration.info
        # Registration.info[chat_id_user] = [username, email]

        # Сохраняем данные в БД sqlite
        try:
            db.add_user(chat_id_user, username, email)
        except sqlite3.IntegrityError as err:
            print(err)

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
        # try:
            # Удаляем пользователя из Registration.info
            # del Registration.info[message.chat.id]
        # except KeyError:
        #     pass

        # Удаляем пользователя из БД sqlite что бы обновить данные внесенные пользователем
        db.delete_user(id=message.from_user.id)
        return await registration(message)
    if answer == "no":
        await message.answer(text="Ok, exit", reply_markup=keyboard)
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
    # Получаем все данные пользователя из словаря Registration.info
    # _user_data = Registration.info[callback.message.chat.id]

    # Получаем все данные пользователя из БД sqlite
    _user_data = db.select_user(user_id=callback.from_user.id)
    _username = _user_data[2]
    _email = _user_data[3]
    await callback.message.answer(text=f"Your username: {_username}\n"
                                       f"Your email: {_email}")
    await callback.message.answer(text="Do you want to change the data? (Yes/No)")
    await Registration.repeat_registration.set()
