from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def add_file_keyboard_button():
    buttons = [
        [KeyboardButton(text='Загрузить файл')]
    ]
    kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, is_persistent=True)
    return kb
