from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from environs import Env

from src.config.conf import RedisConfig


class BotConfig:
    env = Env()
    env.read_env()
    bot_token = env("TOKEN")

    web_server_host = env("WEB_SERVER_HOST")
    web_server_port = int(env("WEB_SERVER_PORT"))

    base_webhook_url = env("BASE_WEBHOOK_URL")
    webhook_path = env("WEBHOOK_PATH")

    webhook_url = f"{base_webhook_url}{webhook_path}"
    webhook_secret_token = env("WEBHOOK_SECRET")

    admins_ids = [int(_) for _ in env("ADMINS_IDS").split(", ")]

    redis_host = env("REDIS_HOST")
    redis_port = int(env("REDIS_PORT"))
    redis = RedisConfig.get_connection()
    red_storage = RedisStorage(redis)

    dp = Dispatcher(storage=red_storage)
    bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode="HTML"))

    scheduler = AsyncIOScheduler(
        timezone="UTC",
        jobstores={"default": RedisJobStore(host=redis_host, port=redis_port, db=0)},
    )


class MyStates(StatesGroup):
    wait_file_for_parse = State()
