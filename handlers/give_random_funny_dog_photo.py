from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import InvalidHTTPUrlContent
from api.random_funny_dog_photo_api import give_random_funny_dog
from loader import bot, dp
from keyboards.inline_keyboard import inline_keyboard, inline_keyboard_without_previous, inline_keyboard_for_media_group
from keyboards.keyboard import keyboard
from states.photo_with_like_dislike import PhotoLikeDislike


@dp.message_handler(commands=["give_photo"])
async def give_photo(message: types.Message):
    try:
        photo = give_random_funny_dog()
        if message.chat.id in PhotoLikeDislike.photo:
            PhotoLikeDislike.photo[message.chat.id].append([photo, 0])
        else:
            PhotoLikeDislike.photo[message.chat.id] = [[photo, 0]]
        PhotoLikeDislike.previous_photo = False
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            reply_markup=inline_keyboard_without_previous
        )
    except InvalidHTTPUrlContent:
        await message.answer(text="Connection error", reply_markup=keyboard)


@dp.callback_query_handler(text="next_photo")
async def next_photo(callback: types.CallbackQuery):
    try:
        PhotoLikeDislike.previous_photo = False
        photo = give_random_funny_dog()
        await callback.message.edit_media(
            media=InputMediaPhoto(photo),
            reply_markup=inline_keyboard
        )
        PhotoLikeDislike.photo[callback.message.chat.id].append([photo, 0])
    except InvalidHTTPUrlContent:
        await callback.message.answer(text="Connection error", reply_markup=keyboard)


@dp.callback_query_handler(text="previous_photo")
async def previous_photo(callback: types.CallbackQuery):
    try:
        PhotoLikeDislike.previous_photo = True
        previous_photo = PhotoLikeDislike.photo[callback.message.chat.id][-2][0]
        await callback.message.edit_media(
            media=InputMediaPhoto(previous_photo),
            reply_markup=inline_keyboard_without_previous
        )
    except InvalidHTTPUrlContent:
        await callback.message.answer(text="Connection error", reply_markup=keyboard)


@dp.callback_query_handler(text="like")
async def like(callback: types.CallbackQuery):
    if PhotoLikeDislike.previous_photo:
        index = -2
    else:
        index = -1
    data = PhotoLikeDislike.photo[callback.message.chat.id][index]
    if data[1] in (-1, 0):
        data[1] = 1
        await callback.answer(text="Like")
    if data[1] == 1:
        await callback.answer(text="You already like this picture")


@dp.callback_query_handler(text="dislike")
async def dislike(callback: types.CallbackQuery):
    if PhotoLikeDislike.previous_photo:
        index = -2
    else:
        index = -1
    data = PhotoLikeDislike.photo[callback.message.chat.id][index]
    if data[1] in (1, 0):
        data[1] = -1
        await callback.answer(text="Dislike")
    if data[1] == -1:
        await callback.answer(text="You already dislike this picture")


@dp.callback_query_handler(text="photo_history")
async def photo_history(callback: types.CallbackQuery):
    photo_group = types.MediaGroup()
    for photo_url in PhotoLikeDislike.photo[callback.message.chat.id]:
        photo_group.attach_photo(InputMediaPhoto(photo_url[0]))
    await bot.send_media_group(chat_id=callback.message.chat.id, media=photo_group)
    await callback.message.answer(text="Additional action:", reply_markup=inline_keyboard_for_media_group)


@dp.callback_query_handler(text="more_photo")
async def more_photo(callback: types.CallbackQuery):
    try:
        photo = give_random_funny_dog()
        PhotoLikeDislike.photo[callback.message.chat.id].append([photo, 0])
        PhotoLikeDislike.previous_photo = False
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=photo,
            reply_markup=inline_keyboard_without_previous
        )
    except InvalidHTTPUrlContent:
        await callback.message.answer(text="Connection error", reply_markup=keyboard)


@dp.callback_query_handler(text="clear_history")
async def clear_history(callback: types.CallbackQuery):
    PhotoLikeDislike.photo.clear()
    await callback.message.answer(text="The photo album is cleared", reply_markup=keyboard)


@dp.callback_query_handler(text="exit")
async def _exit(callback: types.CallbackQuery):
    await callback.message.answer(text="Exit", reply_markup=keyboard)


# --------------------------------------------------------------------------------------------
#
#
# @dp.message_handler(commands=["give_photo"], state=None)
# async def give_photo(message: types.Message, state: FSMContext):
#     try:
#         photo_2 = give_random_funny_dog()
#         await state.update_data(
#             {
#                 "photo_2": photo_2,
#             },
#         )
#         await bot.send_photo(
#             chat_id=message.chat.id,
#             photo=photo_2,
#             reply_markup=inline_keyboard_without_previous
#         )
#     except InvalidHTTPUrlContent:
#         await state.finish()
#         await message.answer(text="Connection error", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="next_photo", state="*")
# async def next_photo(callback: types.CallbackQuery, state: FSMContext):
#     try:
#         data = await state.get_data()
#         photo_1 = data.get("photo_2")
#         photo_2 = give_random_funny_dog()
#         await state.update_data(
#             {
#                 "photo_1": photo_1,
#                 "photo_2": photo_2,
#             },
#         )
#         await callback.message.edit_media(
#             media=InputMediaPhoto(photo_2),
#             reply_markup=inline_keyboard
#         )
#         PhotoLikeDislike.photo[callback.message.chat.id].append([photo_2, 0])
#     except InvalidHTTPUrlContent:
#         await state.finish()
#         await callback.message.answer(text="Connection error", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="previous_photo", state="*")
# async def previous_photo(callback: types.CallbackQuery, state: FSMContext):
#     try:
#         data = await state.get_data()
#         photo_1 = data.get("photo_1")
#
#         await callback.message.edit_media(
#             media=InputMediaPhoto(photo_1),
#             reply_markup=inline_keyboard_without_previous
#         )
#     except InvalidHTTPUrlContent:
#         await state.finish()
#         await callback.message.answer(text="Connection error", reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="exit", state="*")
# async def _exit(callback: types.CallbackQuery, state: FSMContext):
#     await state.finish()
#     await callback.message.answer(text="Exit", reply_markup=keyboard)

# --------------------------------------------------------------------------------------------

# PREVIOUS_URL = []
#
#
# async def send_photo(message: types.Message, previous=None):
#     if len(PREVIOUS_URL):
#         if previous:
#             photo = PREVIOUS_URL[-2]
#             PREVIOUS_URL.clear()
#             PREVIOUS_URL.append(photo)
#             return await bot.send_photo(
#                 chat_id=message.chat.id,
#                 photo=f"{photo}",
#                 reply_markup=inline_keyboard_without_previous,
#             )
#         url_photo = give_random_funny_dog()
#         PREVIOUS_URL.append(url_photo)
#         return await bot.send_photo(
#             chat_id=message.chat.id, photo=f"{url_photo}", reply_markup=inline_keyboard
#         )
#
#     url_photo = give_random_funny_dog()
#     PREVIOUS_URL.append(url_photo)
#     await bot.send_photo(
#         chat_id=message.chat.id,
#         photo=f"{url_photo}",
#         reply_markup=inline_keyboard_without_previous,
#     )
#
#
# @dp.message_handler(commands=["give_photo"])
# async def give_photo(message: types.Message):
#     await message.answer(text="Hold the photo..", reply_markup=ReplyKeyboardRemove())
#     await send_photo(message)
