from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class AdminFilter(BoundFilter):
    async def check(self, messsage: types.Message) -> bool:
        member = await messsage.chat.get_member(messsage.from_user.id)
        return member.is_chat_admin()