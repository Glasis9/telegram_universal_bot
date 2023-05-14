from loader import db


async def on_startup(_):
    from utils.misc.logging import logging

    # Пробуем создать БД, если она уже есть, то подключаемся к ней
    try:
        db.create_table_users()
        db.create_table_photo()
    except Exception as e:
        print(e)

    print("Bot is ready, Hello 👋🏻")


async def on_shutdown(_):
    print("Bye✋🏻")


if __name__ == "__main__":
    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(
        dispatcher=dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown
    )
