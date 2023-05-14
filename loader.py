from aiogram import Dispatcher, Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import TELEGRAM_TOKEN
from utils.db_api.sqlite import Database

bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
db = Database()

# """Для отправки (сообщения) в синхронной функции"""
# dp.loop.run_until_complete(bot.send_message(chat_id="", text=""))
