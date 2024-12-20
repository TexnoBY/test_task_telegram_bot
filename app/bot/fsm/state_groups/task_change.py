from pyrogram_patch.fsm import StatesGroup, StateItem


class TaskChangeGroup(StatesGroup):
    title = StateItem()
    message = StateItem()
