class FileValidationError(Exception):
    """Базовый класс для ошибок валидации файлов"""
    pass


class MissingColumnsError(FileValidationError):
    """Ошибка отсутствия обязательных колонок"""
    def __init__(self, missing_columns):
        self.missing_columns = missing_columns
        message = f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}"
        super().__init__(message)
