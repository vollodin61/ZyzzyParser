from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject

from src.bot.db.database import user_in_base, is_excluded_chat
from src.bot.scheduler.scheduler_functions import auto_ban_unban_n_del_verif_msg
from src.bot.utils.keyboards import verification_in_chat_markup
from src.config import RedisConfig
from src.bot.requests.api_requests import get_verification_in_chat_text


class NewChatMemberVerificationMiddleware(BaseMiddleware):
    """Middleware для принуждения к переходу в бот и его запуску (проверка антибот),
    чтобы потом можно было писать людям сообщения (отправлять напоминалки участникам группы Кошки).
    Игнорирует event из чатов исключенных из этой проверки.
    """

    def __init__(self):
        ...

    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: dict[str, Any]
                       ):
        if event.new_chat_members and not await is_excluded_chat(event.chat.id):
            bot: Bot = data['bot']
            verification_text = await get_verification_in_chat_text()

            for member in event.new_chat_members:

                if await user_in_base(member.id) or member.id == bot.id:
                    continue

                text_to_send = f'<strong>@{member.username}</strong>, {verification_text}'
                markup = await verification_in_chat_markup(chat_id=event.chat.id)
                msg = await bot.send_message(chat_id=event.chat.id,
                                             text=text_to_send,
                                             reply_to_message_id=event.message_id,
                                             reply_markup=markup)

                name_for_redis = f"verification:{event.chat.id}:{member.id}"
                await RedisConfig.get_connection().hset(name=name_for_redis,
                                                        mapping={
                                                            "msg_id": msg.message_id,
                                                            "chat_id": event.chat.id,
                                                            "user_id": member.id,
                                                        })
                await RedisConfig.get_connection().expire(name=name_for_redis, time=666)

                await auto_ban_unban_n_del_verif_msg(msg_id=msg.message_id,
                                                     chat_id=event.chat.id,
                                                     user_id=member.id)
        return await handler(event, data)
