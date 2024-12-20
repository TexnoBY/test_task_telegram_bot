from pyrogram_patch.fsm import StatesGroup, StateItem


class NavigationGroup(StatesGroup):
    registration = StateItem()
    main_menu = StateItem()
    add_task = StateItem()
