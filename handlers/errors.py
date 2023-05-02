from aiogram.utils.exceptions import BotBlocked
from loader import dp
from aiogram import types


# Для отлавливания ошибки блокировки бота
# (отправляем сообщение пользователю, а он заблокировал наш бот)
@dp.errors_handler(exception=BotBlocked)
async def error_bot_block_handler(update: types.Update, exception: BotBlocked) -> bool:
    print("Bot was blocked by the user")
    return True
