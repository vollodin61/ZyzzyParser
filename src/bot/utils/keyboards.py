from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def add_file_keyboard_button():
    buttons = [
        [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, is_persistent=True)
    return kb
