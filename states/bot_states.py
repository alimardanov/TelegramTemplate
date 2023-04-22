from aiogram.dispatcher.filters.state import State, StatesGroup


class UploadWaiterState(StatesGroup):
    Upload = State()


class AskQuestion(StatesGroup):
    Ask = State(),
    Response = State()