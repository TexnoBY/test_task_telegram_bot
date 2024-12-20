from pyrogram_patch.fsm import StatesGroup, StateItem


class TaskGroup(StatesGroup):
    title = StateItem()
    message = StateItem()
