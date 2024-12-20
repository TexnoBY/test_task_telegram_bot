from pyrogram.types import ReplyKeyboardMarkup

main_keyboard = ReplyKeyboardMarkup(
    [
        ["Create task", "Show tasks"],
        ["Options"],
    ],
    resize_keyboard=True
)
