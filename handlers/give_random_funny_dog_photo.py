from aiogram import types
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import InvalidHTTPUrlContent, ValidationError
from api.random_funny_dog_photo_api import give_random_funny_dog
from handlers.registration import registration
from loader import bot, dp, db
from keyboards.inline_keyboard import (
    inline_keyboard,
    inline_keyboard_without_previous,
    inline_keyboard_for_media_group,
)
from keyboards.keyboard import keyboard
from states.photo_with_like_dislike import PhotoLikeDislike


@dp.message_handler(commands=["give_photo"])
async def give_photo(message: types.Message):
    try:
        # photo = give_random_funny_dog()
        # Проверка наличия списка с фото и user id в классе
        # if message.chat.id in PhotoLikeDislike.photo:
            # PhotoLikeDislike.photo[message.chat.id].append([photo, 0])
        photo = give_random_funny_dog()
        user_id = message.from_user.id
        if db.select_user(user_id=user_id) is not None:
            db.add_photo(user_id, photo)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                reply_markup=inline_keyboard_without_previous,
            )
        else:
            # PhotoLikeDislike.photo[message.chat.id] = [[photo, 0]]

            # Отправляем пользователя на регистрацию
            await message.answer(text="You have to be registered")
            await registration(message)

        PhotoLikeDislike.previous_photo = False
    except InvalidHTTPUrlContent:
        await message.answer(text="Connection error", reply_markup=keyboard)


@dp.callback_query_handler(text="next_photo")
async def next_photo(callback: types.CallbackQuery):
    try:
        PhotoLikeDislike.previous_photo = False
        photo = give_random_funny_dog()
        # PhotoLikeDislike.photo[callback.message.chat.id].append([photo, 0])

        # Добавляем фото в БД sqlite
        db.add_photo(user_id=callback.from_user.id, photo=photo)
        await callback.message.edit_media(
            media=InputMediaPhoto(photo), reply_markup=inline_keyboard
        )
    except InvalidHTTPUrlContent:
        await callback.message.answer(text="Connection error", reply_markup=keyboard)


@dp.callback_query_handler(text="previous_photo")
async def previous_photo(callback: types.CallbackQuery):
    try:
        PhotoLikeDislike.previous_photo = True
        # _previous_photo = PhotoLikeDislike.photo[callback.message.chat.id][-2][0]
        all_photo = db.select_all_user_photo(user_id=callback.from_user.id)
        _previous_photo = all_photo[-2][2]
        await callback.message.edit_media(
            media=InputMediaPhoto(_previous_photo),
            reply_markup=inline_keyboard_without_previous,
        )
    except InvalidHTTPUrlContent:
        await callback.message.answer(text="Connection error", reply_markup=keyboard)
    except KeyError:
        await callback.message.answer(
            text="Use the /give_photo button on the keyboard from below",
            reply_markup=keyboard
        )


@dp.callback_query_handler(text="like")
async def like(callback: types.CallbackQuery):
    try:
        if PhotoLikeDislike.previous_photo:
            index = -2
        else:
            index = -1

        # data = PhotoLikeDislike.photo[callback.message.chat.id][index]
        # if data[1] in (-1, 0):
        #     data[1] = 1
        #     await callback.answer(text="Like", show_alert=True)
        # if data[1] == 1:
        #     await callback.answer(text="You already like this picture", show_alert=True)

        data = db.select_all_user_photo(user_id=callback.from_user.id)[index]
        if data[3] in (-1, 0):
            db.update_like_dislike(photo=data[2], like_dislike=1)
            await callback.answer(text="Like", show_alert=True)
        if data[3] == 1:
            await callback.answer(text="You already like this picture", show_alert=True)

    except KeyError:
        await callback.message.answer(
            text="Use the /give_photo button on the keyboard from below",
            reply_markup=keyboard
        )


@dp.callback_query_handler(text="dislike")
async def dislike(callback: types.CallbackQuery):
    try:
        if PhotoLikeDislike.previous_photo:
            index = -2
        else:
            index = -1
        # data = PhotoLikeDislike.photo[callback.message.chat.id][index]
        # if data[1] in (1, 0):
        #     data[1] = -1
        #     await callback.answer(text="Dislike", show_alert=True)
        # if data[1] == -1:
        #     await callback.answer(text="You already dislike this picture", show_alert=True)

        data = db.select_all_user_photo(user_id=callback.from_user.id)[index]
        if data[3] in (1, 0):
            db.update_like_dislike(photo=data[2], like_dislike=-1)
            await callback.answer(text="Dislike", show_alert=True)
        if data[3] == -1:
            await callback.answer(text="You already dislike this picture", show_alert=True)
    except KeyError:
        await callback.message.answer(
            text="Use the /give_photo button on the keyboard from below",
            reply_markup=keyboard
        )


@dp.callback_query_handler(text="photo_history")
async def photo_history(callback: types.CallbackQuery):
    try:
        # photo_group.attach_photo()
        # for photo_url in PhotoLikeDislike.photo[callback.message.chat.id]:
        #     photo_group.attach_photo(InputMediaPhoto(photo_url[0]))

        all_photo = db.select_all_user_photo(user_id=callback.from_user.id)
        if len(all_photo) > 0:
            while len(all_photo) != 0:
                photo_group = types.MediaGroup()
                for photo_url in all_photo[:10]:
                    photo_group.attach_photo(photo_url[2])
                del all_photo[:10]
                await bot.send_media_group(chat_id=callback.message.chat.id, media=photo_group)

        # await bot.send_media_group(chat_id=callback.message.chat.id, media=photo_group)

            await callback.message.answer(
                text="Additional action:", reply_markup=inline_keyboard_for_media_group
            )
        else:
            await callback.message.answer(
                text="The archive is empty, click /give_photo", reply_markup=keyboard
            )
    except KeyError:
        await callback.message.answer(
            text="Use the /give_photo button on the keyboard from below",
            reply_markup=keyboard
        )


@dp.message_handler(commands=["photo_history"])
async def photo_history(message: types.Message):
    try:
        all_photo = db.select_all_user_photo(user_id=message.from_user.id)
        if len(all_photo) > 0:
            while len(all_photo) != 0:
                photo_group = types.MediaGroup()
                for photo_url in all_photo[:10]:
                    photo_group.attach_photo(photo_url[2])
                del all_photo[:10]
                await bot.send_media_group(chat_id=message.chat.id, media=photo_group)

            await message.answer(
                text="Additional action:", reply_markup=inline_keyboard_for_media_group
            )
        else:
            await message.answer(
                text="The archive is empty, click /give_photo", reply_markup=keyboard
            )
    except KeyError:
        await message.answer(
            text="Use the /give_photo button on the keyboard from below",
            reply_markup=keyboard
        )


@dp.callback_query_handler(text="more_photo")
async def more_photo(callback: types.CallbackQuery):
    try:
        photo = give_random_funny_dog()
        # PhotoLikeDislike.photo[callback.message.chat.id].append([photo, 0])

        db.add_photo(user_id=callback.from_user.id, photo=photo)

        PhotoLikeDislike.previous_photo = False
        await bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=photo,
            reply_markup=inline_keyboard_without_previous,
        )
    except InvalidHTTPUrlContent:
        await callback.message.answer(text="Connection error", reply_markup=keyboard)
    except KeyError:
        await callback.message.answer(
            text="Use the /give_photo button on the keyboard from below",
            reply_markup=keyboard
        )


@dp.callback_query_handler(text="clear_history")
async def clear_history(callback: types.CallbackQuery):
    # PhotoLikeDislike.photo.clear()
    db.clear_all_user_photo(callback.from_user.id)
    await callback.message.answer(
        text="The photo album is cleared", reply_markup=keyboard
    )


@dp.callback_query_handler(text="exit_photo")
async def exit_photo(callback: types.CallbackQuery):
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
