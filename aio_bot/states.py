from aiogram.fsm.state import StatesGroup, State


class UserForm(StatesGroup):
    GetChannel = State()
    RemoveChannel = State()


class AdminForm(StatesGroup):
    Admin = State()
    GetAdmin = State()
    RemoveAdmin = State()
