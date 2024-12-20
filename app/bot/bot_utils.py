from typing import Callable, Iterable

from pyrogram.types import InlineKeyboardButton


def get_inline_keyboard(sequence: Iterable, item_handling: Callable, command: str = '', offset: int = 0,
                        step: int = 10) -> list:
    """
    Возвращает list InlineKeyboardButton по входной последовательности

    @param sequence: Iterable
    @param item_handling: Callable
    @param command: str
    @param offset: offset
    @param step: step
    @return:
    """
    try:
        keyboard: list = []
        for id_, name in (item_handling(item) for item in sequence):
            callback_data = f'{command},id:{str(id_)}offset:{offset}'
            keyboard.append([InlineKeyboardButton(text=name,
                                                  callback_data=callback_data)])
        options: list = []
        if offset - step >= 0:
            options.append(

                InlineKeyboardButton(text='Назад',
                                     callback_data=f'{command}offset,offset:{offset - step}'),

            )
        if keyboard:
            options.append(
                InlineKeyboardButton(text='Далее',
                                     callback_data=f'{command}offset,offset:{offset + step}')
            )
        if options:
            keyboard.append(options)
        return keyboard
    except Exception as exc:
        print(exc)
    pass
