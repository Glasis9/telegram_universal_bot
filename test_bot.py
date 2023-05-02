#!venv/bin/python
import logging
import os
import random
import string
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


load_dotenv()


HELP_COMMAND = """
Список команд
<b>/help</b> - список команд
<b>/test1</b> - ответ с ретвитом
<b>/test2</b> - простой ответ
<b>/weather</b> - вернет прогноз погоды
<b>/give_letter</b> - вернет рандомную букву в верхнем регистре
<b>/give_number</b> - вернет рандомное число от 1 до 12
<b>/hello</b> - бот поздоровается с тобой
<b>/photo</b> - отправит рандомное фото
<b>/location</b> - отправит рандомную локацию
<b>/vote</b> - отправит рандомное фото кошки с вопросом

<em>Любое сообщение более 2 слов вернет .upper(),
меньше 2 слов - вернет ошибку!</em>
"""


# Объект бота
bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Создаем клавиатуру
keyboard = ReplyKeyboardMarkup(  # ReplyKeyboardMarkup - Создает объект клавиатуры
    resize_keyboard=True,  # Автоподгон размера клавиатуру
    one_time_keyboard=True  # default = False (автозакрытие клавиатуры (можем открыть кнопкой сбоку))
)
keyboard.add(KeyboardButton("/help"))  # KeyboardButton - Создает кнопку
keyboard.add(KeyboardButton("/test1")).insert(KeyboardButton("/test2"))  # .insert добавит в одну строку кнопку
keyboard.add(KeyboardButton("/give_letter")).insert(KeyboardButton("/give_number"))  # .add добавит снизу кнопку
# keyboard.add((KeyboardButton("/hello"))).insert(KeyboardButton("/photo")).insert(KeyboardButton("/location"))
# Тоже самое что и верхняя строчка
keyboard.add((KeyboardButton("/hello")), KeyboardButton("/photo"), KeyboardButton("/location"))


# Инлайн клавиатура (кнопки на экране)
inline_keyboard = InlineKeyboardMarkup(row_width=2)
inline_keyboard.add(
    InlineKeyboardButton(
        text="Видео по InlineKeyboard",
        url="https://www.youtube.com/watch?v=5_EHfHbzUCo&list=PLe-iIMbo5JOJm6DRTjhleHojroS-Bbocr&index=11"),
    InlineKeyboardButton(
        text="Практика по InlineKeyboard",
        url="https://www.youtube.com/watch?v=pWqzA8fRrNs&list=PLe-iIMbo5JOJm6DRTjhleHojroS-Bbocr&index=12"),
)


PHOTO_CATS = [
        "https://i.pinimg.com/736x/ba/92/7f/ba927ff34cd961ce2c184d47e8ead9f6.jpg",
        "https://wallpapers-clan.com/wp-content/uploads/2022/07/funny-cat-3.jpg",
        "https://wallpapers-clan.com/wp-content/uploads/2022/07/funny-cat-1.jpg",
        "https://i.ytimg.com/vi/OOFGdRmN70k/maxresdefault.jpg",
    ]


@dp.message_handler(commands=["help", "start"])
async def help_command(message: types.Message):
    await message.answer(
        text=f"{HELP_COMMAND}",
        parse_mode="HTML",  # Что бы обрабатывалась html разметка в строке
        reply_markup=inline_keyboard  # Добавляет клавиатуру
        # reply_markup=ReplyKeyboardRemove()  # Удаляет клавиатуру
    )
    await message.delete()


# Хэндлер на команду /test1
@dp.message_handler(commands=["test1"])
async def cmd_test1(message: types.Message):
    await message.reply("Это ответ с ретвитом " + message.text.upper())


@dp.message_handler(commands=["test2"])
async def cmd_test2(message: types.Message):
    await message.answer("Это простой ответ", reply_markup=keyboard)


"""Получение рандомной буквы алфавита"""
@dp.message_handler(commands=["give_letter"])
async def random_char(message: types.Message):
    await message.answer("Держи букву: " + random.choice(string.ascii_uppercase) + " 😛")


"""Получение рандомной цифры от 1 до 12"""
@dp.message_handler(commands=["give_number"])
async def random_int(message: types.Message):
    await message.answer("Держи число: " + str(random.randint(1, 13)))


@dp.message_handler(commands=["hello"])
async def hello_sticker(message: types.Message):
    await bot.send_sticker(
        chat_id=message.from_user.id,
        sticker="CAACAgIAAxkBAAEIpj5kQQ6jRe3UbCAYfDl3HMjGyPpkVgACoAADlp-MDmce7YYzVgABVS8E",
    )


@dp.message_handler(commands=["photo"])
async def photo(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=random.choice(PHOTO_CATS))


@dp.message_handler(commands=["location"])
async def location(message: types.Message):
    await bot.send_location(
        chat_id=message.chat.id,
        latitude=random.randrange(1, 101),
        longitude=random.randrange(1, 101)
    )


"""Хендлер ловит любые сообщения и проверяет их на длину"""
@dp.message_handler()
async def all_handler(message: types.Message):
    if len(message.text.split()) >= 2:
        await message.answer(message.text.upper() + " " + "😛")
    else:
        await message.answer("Sorry, your message is less than 2 words")


@dp.message_handler(commands=["vote"])
async def links(message: types.Message):
    inline_keyboard = InlineKeyboardMarkup(row_width=2)
    inline_keyboard.add(
        InlineKeyboardButton(text="❤️", callback_data="like"),
        InlineKeyboardButton(text="👎🏻", callback_data="dislike"),
    )
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=random.choice(PHOTO_CATS),
                         caption="Do you like this photo?",
                         reply_markup=inline_keyboard)


@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == "like":
        return await callback.answer(text="Like")
    await callback.answer(text="dislike")


async def on_startup(_):
    print("Hello 👋🏻")


async def on_shutdown(_):
    print("Bye ✋🏻")


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(
        dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )


"""
chat_id=message.from_user.id - отправит сообщение в личный чат пользователя
chat_id=message.chat.id - отправит сообщение в текущий чат откуда пришел запрос
message.answer("message") - тоже отправит сообщение в текущий чат откуда пришел запрос
"""
