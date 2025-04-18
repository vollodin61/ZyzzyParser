import os

import pandas as pd
from typing import Tuple, Optional

from src.bot.utils.exceptions import MissingColumnsError, FileValidationError
from src.config import error_logger, info_logger


async def get_file_data_for_answer(file_path: str) -> str:
    """
    Формирует строку с содержимым Excel-файла для отправки пользователю

    :param file_path: Полный путь к файлу
    :return: Строка с содержимым файла
    """
    try:
        df = pd.read_excel(file_path)
        len_df = len(df)
        info_logger(f'Строк в файле: {len_df}')
        # Ограничим количество строк для вывода (например, первые 20)
        max_rows_to_show = 20
        if len_df > max_rows_to_show:
            df = df.head(max_rows_to_show)
            row_count_info = f"\n\nПоказано первые {max_rows_to_show} строк из {len_df}"
        else:
            row_count_info = f"\n\nВсего строк: {len_df}"

        # Форматируем DataFrame в строку
        result = []

        file_name = os.path.basename(file_path)
        result.append(f"📄 Файл: {file_name}")

        # Добавляем список листов (если их несколько)
        with pd.ExcelFile(file_path) as xls:
            if len(xls.sheet_names) > 1:
                result.append(f"\n📑 Листы: {', '.join(xls.sheet_names)}")

        # Добавляем содержимое DataFrame
        result.append("\n\nСодержимое:")
        result.append(df.to_string(index=False))
        result.append(row_count_info)

        return "\n".join(result)

    except Exception as e:
        error_logger(f"Ошибка при чтении файла {file_path}: {repr(e)}")
        return "Не удалось прочитать содержимое файла"


async def validate_file_structure(file_path: str) -> Tuple[bool, Optional[str], Optional[pd.DataFrame]]:
    """
    Проверяет структуру Excel-файла на соответствие требованиям.
    Вначале просто пытается открыть, тем самым проверяя excel это или нет.
    Потом смотрит наличие обязательных колонок.

    :param file_path: Путь к файлу
    :return: None или рейзит ошибку
    """
    try:
        df = pd.read_excel(file_path)

        required_columns = {'title', 'url', 'xpath'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise MissingColumnsError(missing)
    except FileValidationError:
        raise
    except Exception as e:
        raise FileValidationError(f"Ошибка при чтении файла {str(e)}")

