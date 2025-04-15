import asyncio  # noqa
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from src.bot.commands.bot_commands import set_commands
from src.bot.config.bot_config import BotConfig
from src.bot.db.database import create_tables
from src.bot.handlers.setter_handlers import set_routers
from src.bot.middlewares.set_middlewares import set_middleware
from src.config import error_logger, info_logger

sys.path.insert(1, os.path.join(sys.path[0], '..'))


async def on_startup(bot: Bot, dp: Dispatcher = BotConfig.dp) -> None:
    # await set_admin_commands(bot)  ждёт, когда создам админские команды
    BotConfig.scheduler.start()
    await set_commands(bot)
    info_logger("Команды установлены")
    set_middleware(dp)
    info_logger("Миддлвари установлены")
    set_routers(dp)
    info_logger("Роутеры установлены")
    await bot.delete_webhook()
    info_logger("Вебхуки удалены")
    await bot.set_webhook(
        url=BotConfig.webhook_url,
        secret_token=BotConfig.webhook_secret_token,
        drop_pending_updates=True
    )
    info_logger(f"Вебхуки установлены на эндпоинт {BotConfig.webhook_url}")


def main():
    BotConfig.dp.startup.register(on_startup)
    app = web.Application()

    SimpleRequestHandler(
        dispatcher=BotConfig.dp,
        bot=BotConfig.bot,
        secret_token=BotConfig.webhook_secret_token
    ).register(
        app,
        path=BotConfig.webhook_path
    )

    setup_application(app, BotConfig.dp, bot=BotConfig.bot)

    web.run_app(
        app,
        host=BotConfig.web_server_host,
        port=BotConfig.web_server_port
    )
    asyncio.run(create_tables())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        main()
    except Exception as err:
        error_logger(f'При запуске бота ошибка: \n{repr(err)}')

# Если нет сервера для вебхуков, то можно на поллинге запустить
# async def old_main():
#     BotConfig.scheduler.start()
#     await set_commands(bot=BotConfig.bot)
#     set_middleware(dp=BotConfig.dp)
#     set_routers(dp=BotConfig.dp)
#     await BotConfig.bot.delete_webhook(drop_pending_updates=True)
#     await BotConfig.dp.start_polling(BotConfig.bot)
#     asyncio.run(create_tables())
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     try:
#         asyncio.run(old_main())
#     except Exception as e:
#         logging.exception(e)
