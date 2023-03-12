from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

post_callback = CallbackData("create_post", "action")

confirmer_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton("Chop Etish", callback_data=post_callback.new(action="post")),
        InlineKeyboardButton("Rad Etish", callback_data=post_callback.new(action='cancel')),
    ],
    ]
)

