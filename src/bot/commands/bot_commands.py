from aiogram import Bot
from aiogram.types import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
)

from src.bot.config.bot_config import BotConfig


async def set_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Стартуем! Сегодня мы с тобой стартуем! 😁"),
        ],
        scope=BotCommandScopeAllPrivateChats()
    )
