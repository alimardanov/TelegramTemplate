import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from data.config import ADMINS, CHANNELS
from keyboards.inline.inline_manager import confirmer_keyboards, post_callback
from loader import dp, bot
from states.newpost import NewPost

@dp.message_handler(Command("create_post"))
async def create_post(message: Message):
    await message.answer("Chop etish uchun port yuboring")
    await NewPost.Post.set()

@dp.message_handler(state=NewPost.Post)
async def enter_message(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer("Postni tekshirish uchun yuboraymi?", reply_markup=confirmer_keyboards)
    await NewPost.next()


# @dp.callback_query_handler(post_callback.filter(action='post'), state=NewPost.Confirm)
# async def confirm_post(call: CallbackQuery, state:FSMContext):
#     async with state.proxy() as data:
#         text = data.get('text')
#         mention = data.get('mention')
#     await state.finish()
#     await call.message.edit_reply_markup()
#     await call.message.answer("Post tasdiqlash uchun adminga yuborildi")
#     await Bot.send_message(self=Bot, chat_id=ADMINS[0], text=f"Foydalanuvchi {mention} quyidagi postni kanalda chop etmoqchi:")
#     await Bot.send_message(self=Bot, chat_id=ADMINS[0], text=text, parse_mode='HTML', reply_markup=confirmer_keyboards)

@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Post Adminga yuborildi")
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {mention} quyidagi postni chop etmoqchi:")
    await bot.send_message(ADMINS[0], text, parse_mode="HTML", reply_markup=confirmer_keyboards)

@dp.callback_query_handler(post_callback.filter(action='cancel'), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state:FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer('Post rad etildi.')


@dp.callback_query_handler(state=NewPost.Confirm)
async def post_unknown(message:Message):
    await message.answer("Chop etish yoki Rad etishni tanlang.")

# @dp.callback_query_handler(post_callback.filter(action='post'), user_id=ADMINS)
# async def approve_post(call:CallbackQuery):
#     await call.answer("Chop etishni ma'qulladingiz.", show_alert=True)
#     target_channel = CHANNELS[0]
#     msg = await call.message.edit_reply_markup()
#     await msg.send_copy(chat_id=target_channel)


@dp.callback_query_handler(post_callback.filter(action="post"), user_id=ADMINS)
async def approve_post(call: CallbackQuery):
    await call.answer("Chop etishga ruhsat berdingiz.", show_alert=True)
    target_channel = CHANNELS
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_channel)  


@dp.callback_query_handler(post_callback.filter(action='cancel'), user_id=ADMINS)
async def reject_post(call:CallbackQuery):
    await call.answer("Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()