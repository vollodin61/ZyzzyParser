import functools
import inspect
from traceback import format_exc

from src.config import error_logger, info_logger


def safe_call_dec(func):
    """
    Декоратор, обрабатывающий и синхронные, и асинхронные функции:
    - Логирует в файл и консоль в случае возникновения ошибки.
    """
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                err_msg = (f'Ошибка в функции {func.__name__}: {repr(e)}\n'
                           f'Трейсбэк: {format_exc()}')
                error_logger(err_msg)
                # return None
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                err_msg = (f'Ошибка в функции {func.__name__}: {repr(e)}\n'
                           f'Трейсбэк: {format_exc()}')
                error_logger(err_msg)
#                 return None

    return wrapper
