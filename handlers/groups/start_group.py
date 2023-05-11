from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from filters import IsPrivate, IsGroupChat, AdminFilter

from loader import dp

@dp.message_handler(IsGroupChat(), CommandStart())
async def bot_start(message: types.Message):
    text = f"Salom, {message.from_user.full_name}! Welcome to you group chat!"

    await message.answer(text)
