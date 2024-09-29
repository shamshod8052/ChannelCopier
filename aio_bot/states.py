from aiogram.fsm.state import StatesGroup, State


class ChannelForm(StatesGroup):
    Channel = State()
    GetChannel = State()
    RemoveChannel = State()


class AdminForm(StatesGroup):
    Admin = State()
    GetAdmin = State()
    RemoveAdmin = State()


class MyChannelForm(StatesGroup):
    MyChannel = State()
    GetMyChannel = State()
    RemoveChannel = State()
