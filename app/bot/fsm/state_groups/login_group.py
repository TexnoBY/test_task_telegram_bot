from pyrogram_patch.fsm import StatesGroup, StateItem


class LoginGroup(StatesGroup):
    login = StateItem()
    name = StateItem()
