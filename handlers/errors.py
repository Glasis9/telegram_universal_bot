import logging

from aiogram.types import Update
from aiogram.utils.exceptions import BotBlocked
from loader import dp
from aiogram import types


# Для отлавливания ошибки блокировки бота
# (отправляем сообщение пользователю, а он заблокировал наш бот)
@dp.errors_handler(exception=BotBlocked)
async def error_bot_block_handler(update: types.Update, exception: BotBlocked) -> bool:
    print("Bot was blocked by the user")
    return True


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """
    from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                          CantDemoteChatCreator, MessageNotModified,
                                          MessageToDeleteNotFound, MessageTextIsEmpty,
                                          RetryAfter, CantParseEntities, MessageCantBeDeleted, BadRequest)

    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can`t demote chat creator")
        return True
    if isinstance(exception, MessageNotModified):
        logging.debug("Message is not modified")
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.info("Message can`t be deleted")
        return True
    if isinstance(exception, MessageToDeleteNotFound):
        logging.info("Message to delete not found")
        return True
    if isinstance(exception, MessageTextIsEmpty):
        logging.debug("Message text is empty")
        return True
    if isinstance(exception, Unauthorized):
        logging.info(f"Unauthorized: {exception}")
        return True
    if isinstance(exception, InvalidQueryID):
        logging.exception(f"Invalid query id: {exception} \nUpdate: {update}")
        return True
    if isinstance(exception, CantParseEntities):
        await Update.get_current().message.answer(f"Can`t parse entities: {exception}")
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f"Retry after: {exception} \nUpdate: {update}")
        return True
    if isinstance(exception, BadRequest):
        logging.exception(f"Can`t parse entities: {exception} \nUpdate: {update}")
        return True
    if isinstance(exception, TelegramAPIError):
        logging.exception(f"Telegram api error: {exception} \nUpdate: {update}")
        return True

    logging.exception(f"Update: {update} \n{exception}")
