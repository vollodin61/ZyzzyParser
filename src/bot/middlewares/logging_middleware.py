import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message, TelegramObject, Update


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage
        self.loggers = {}

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any],
    ):
        if isinstance(event.message, Message):
            await self.on_process_message(event.message, data)
        elif isinstance(event.callback_query, CallbackQuery):
            await self.on_process_callback_query(event.callback_query, data)

        return await handler(event, data)

    async def on_process_message(self, msg: Message, data: dict):  # noqa
        msg_text = msg.caption if msg.caption else msg.text
        file_id = self.file_id_extractor(msg)
        await self.log_user_action(
            msg.from_user.id, msg.message_id, msg.content_type.lower(), file_id, msg_text
        )

    async def on_process_callback_query(self, callback: CallbackQuery, data: dict):  # noqa
        await self.log_user_action(
            callback.from_user.id, callback.message.message_id, callback.message.content_type.lower(), callback.data,
        )

    def file_id_extractor(self, msg: Message):
        file_id = ''
        if msg.photo:
            file_id = msg.photo[-1].file_id
        else:
            dict_from_msg = msg.model_dump(exclude_unset=True)
            for k, v in dict_from_msg.items():
                try:
                    file_id = v.get('file_id')
                    if file_id:
                        break
                except:
                    continue
        return file_id

    def get_user_logger(self, user_id):
        if user_id not in self.loggers:
            log_file = f"src/bot/logs/{user_id}.log"
            user_logger = logging.getLogger(f"user_{user_id}")
            user_logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
            user_logger.addHandler(file_handler)

            self.loggers[user_id] = user_logger
        return self.loggers[user_id]

    async def log_user_action(
            self, user_id: int, message_id: int, content_type: str, file_id: str = None, text: str = None
    ):
        user_logger = self.get_user_logger(user_id)
        from datetime import datetime
        date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        action = f"{date_time} | msg_id: {message_id}, content_type: {content_type}, file_id: {file_id}, text: {text}"
        user_logger.info(action)
