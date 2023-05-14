from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from states.count import Count
from keyboards.inline_keyboard import inline_keyboard_exit_count
from keyboards.keyboard import keyboard
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(commands=["count_it"])
async def count_it(message: types.Message):
    await message.answer(
        text="Input task for example: (2 * 4 / 2) ** 2",
        reply_markup=inline_keyboard_exit_count
    )
    await Count.count.set()


@dp.message_handler(state=Count.count)
async def count(message: types.Message, state: FSMContext):
    try:
        await message.reply(text=f"{eval(''.join(message.text))}", reply_markup=keyboard)
    except ZeroDivisionError:
        await message.reply(text="You can't divide by 0")
        await count_it(message)
    except (NameError, SyntaxError):
        await message.reply(text="Incorrect data")
        await count_it(message)
    await state.finish()


@dp.callback_query_handler(text="exit_count", state="*")
async def exit_count(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer(text="Exit", reply_markup=keyboard)
    await callback.message.delete()
