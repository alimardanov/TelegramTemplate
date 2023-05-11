from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class IsGroupChat(BoundFilter):
    async def check(self, messsage:types.Message):
        return types.ChatType().SUPERGROUP == messsage.chat.type