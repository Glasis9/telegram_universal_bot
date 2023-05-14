from aiogram import types
from loader import dp, db
from keyboards.keyboard import keyboard


HELP_COMMANDS = """
Select the action:
<b>/give_photo</b> - рандомное фото собаки
<b>/photo_history</b> - выведет архив фото, если они есть
<b>/give_joke</b> - рандомная шутка
<b>/give_number</b> - кинуть два кубика
<b>/give_letter</b> - рандомная буква алфавита
<b>/count_it</b> - считает введенный пример
<b>/registration</b> - регистрация в боте
"""


"""
content_types=types.ContentTypes.TEXT - по умолчанию в хендлере 
(для того что бы принимать другой тип данных нужно явно это указать 
(вместо TEXT например написать PHOTO, VIDEO)
"""
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(text=HELP_COMMANDS, reply_markup=keyboard)
