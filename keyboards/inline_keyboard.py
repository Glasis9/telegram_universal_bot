from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


like_btn = InlineKeyboardButton(text="❤️", callback_data="like")
dislike_btn = InlineKeyboardButton(text="👎🏻", callback_data="dislike")
previous_photo_btn = InlineKeyboardButton(text="Previous 🏞️", callback_data="previous_photo")
next_photo_btn = InlineKeyboardButton(text="Next 🏞️", callback_data="next_photo")
photo_history = InlineKeyboardButton(text="Photo history", callback_data="photo_history")
exit_photo = InlineKeyboardButton(text="Exit📤", callback_data="exit_photo")

inline_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [like_btn, dislike_btn],
    [previous_photo_btn, next_photo_btn],
    [photo_history, exit_photo],
])

inline_keyboard_without_previous = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [like_btn, dislike_btn],
    [next_photo_btn],
    [exit_photo],
])

inline_keyboard_for_media_group = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Clear the history of the photo", callback_data="clear_history")],
    [
        InlineKeyboardButton(text="Get more photo", callback_data="more_photo"),
        exit_photo,
    ],
])

inline_keyboard_check_user_data = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Check data", callback_data="check_data"),
     ],
    [InlineKeyboardButton(text="Exit📤", callback_data="exit_reg")]
])


inline_keyboard_exit_count = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Exit📤", callback_data="exit_count")]
])

inline_keyboard_exit_registration = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Exit📤", callback_data="exit_registration")]
])

inline_keyboard_exit_weather = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Exit📤", callback_data="exit_weather")]
])
