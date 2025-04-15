import os
from datetime import datetime

import pandas as pd
from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.config.bot_config import MyStates
from src.bot.db.database import save_data_from_tables_to_db
from src.bot.utils.keyboards import add_file_keyboard_button
from src.bot.utils.utils import get_file_data_for_answer, validate_file_structure
from src.config import error_logger

def_router = Router()


@def_router.message(CommandStart())
async def cmd_start_handler(msg: Message, state: FSMContext):
    await msg.answer("Hello, my friend! 🤗\n\nНажми на кнопку, получишь результат! 😉",
                     reply_markup=await add_file_keyboard_button())
    await state.set_state(MyStates.wait_file_for_parse)


@def_router.message(StateFilter(MyStates.wait_file_for_parse))
async def wait_file_for_parse_handler(msg: Message, state: FSMContext, bot: Bot):
    if not msg.document.file_name.endswith(('.xlsx', '.xls')) or not msg.document:
        await msg.answer("Это не то, что я ожидаю)) Пришли файл Excel-формата")
        return

    dt_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f'temp/{msg.chat.id}_{dt_now}_{msg.document.file_name}'
    os.makedirs("temp", exist_ok=True)

    file_info = await bot.get_file(msg.document.file_id)
    await bot.download_file(file_info.file_path, file_path)

    try:
        await validate_file_structure(file_path)
    except Exception as e:
        await msg.answer(f"Файл не является корректным Excel-файлом. Ошибка {str(e)}")
        error_logger(f"Файл не является корректным Excel-файлом. Ошибка {repr(e)}")
        os.remove(file_path)
        return

    full_file_path = os.path.abspath(file_path)
    file_data_for_answer = await get_file_data_for_answer(full_file_path)
    await msg.answer('Файл получен и проверен успешно. Вот его содержание:')
    await msg.answer(file_data_for_answer)
    await state.clear()
    await save_data_from_tables_to_db(full_file_path)
