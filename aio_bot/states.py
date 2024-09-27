from aiogram.fsm.state import StatesGroup, State


class UserForm(StatesGroup):
    GetChannel = State()
    RemoveChannel = State()
