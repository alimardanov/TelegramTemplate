from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

class IsPrivate(BoundFilter):
    async def check(self, messsage: types.Message()):
        return messsage.chat.type == types.ChatType().PRIVATE