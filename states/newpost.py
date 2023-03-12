from aiogram.dispatcher.filters.state import StatesGroup, State


class NewPost(StatesGroup):
    Post = State()
    Confirm = State()