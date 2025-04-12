import logging
from typing import Any

from emoji import emojize
from environs import Env
from loguru import logger
from redis.asyncio.client import Redis
from redis.backoff import ExponentialBackoff
from redis.exceptions import BusyLoadingError, ConnectionError, TimeoutError
from redis.retry import Retry
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

env = Env()
env.read_env()

info_logger = logger.info
error_logger = logger.error
warning_logger = logger.warning
exception_logger = logger.exception
debug_logger = logger.debug

logging.basicConfig(level=logging.INFO)


class BaseConfig:
    TIMEOUT = 4
    RETRY = 4

    @staticmethod
    def log_action(service_name: str = None, action: Any = None):
        log_file = f"src/logs/{service_name}.log"
        service_logger = logging.getLogger(f"service_{service_name}")
        service_logger.setLevel(logging.INFO)
        if not service_logger.handlers:
            file_handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            service_logger.addHandler(file_handler)

        service_logger.info(action)

    @staticmethod
    def log_retry_attempt(retry_state):
        exception = retry_state.outcome.exception()
        BaseConfig.log_action(
            service_name=retry_state.fn.__qualname__, action=exception
        )

    @staticmethod
    def log_final_exception(retry_state):
        exception = retry_state.outcome.exception()
        BaseConfig.log_action(
            service_name=retry_state.fn.__qualname__, action=exception
        )

    base_retry = retry(
        stop=stop_after_attempt(RETRY),
        wait=wait_fixed(TIMEOUT),
        retry=retry_if_exception_type(Exception),
        after=log_retry_attempt,
        retry_error_callback=log_final_exception,
    )


class RedisConfig(BaseConfig):
    redis_instance = None
    RETRY = 3
    TIMEOUT = 3

    @staticmethod
    @BaseConfig.base_retry
    def get_connection():
        redis_host = env("REDIS_HOST")
        # redis_host = "localhost"
        redis_port = env("REDIS_PORT")
        if not RedisConfig.redis_instance:
            RedisConfig.redis_instance = Redis(
                host=redis_host,
                port=int(redis_port),
                socket_timeout=RedisConfig.TIMEOUT,
                retry=Retry(ExponentialBackoff(), RedisConfig.RETRY),
                retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError],
            )
            info_logger("Redis подключен")

        return RedisConfig.redis_instance


class Emo:
    #  Эмодзи тут -> нажми Meta + .
    @staticmethod
    def get_emoji(smile):
        return emojize(smile, variant="emoji_type")

    ruble = get_emoji("₽")
    big_smile = get_emoji(":grinning_face_with_big_eyes:")
    hugs = get_emoji(":smiling_face_with_open_hands:")
    hand_over_mouth = get_emoji(":face_with_hand_over_mouth:")
    hundred = get_emoji(":hundred_points:")
    quiet = get_emoji(":shushing_face:")
    heart = get_emoji("❤️")
    omg_cat_face = get_emoji("🙀")
    red_exclamation = get_emoji("❗️")
    nerd_face = get_emoji(":nerd_face:")
    sunglasses = get_emoji("😎")
    explosive_head = get_emoji("🤯")
    hi = get_emoji("👋")
    just_smile = get_emoji("🙂")
    zero = get_emoji("0️⃣")
    one = get_emoji("1️⃣")
    two = get_emoji("2️⃣")
    three = get_emoji("3️⃣")
    four = get_emoji("4️⃣")
    five = get_emoji("5️⃣")
    six = get_emoji("6️⃣")
    seven = get_emoji("7️⃣")
    eight = get_emoji("8️⃣")
    nine = get_emoji("9️⃣")
    ten = get_emoji("🔟")
    hz = get_emoji("🤷‍♂️")
    please_eyes = get_emoji("🥺")
    please = get_emoji("🙏")
    arrow_left = get_emoji("⬅️")
    arrow_right = get_emoji("➡️️")
    arrow_up = get_emoji("⬆️")
    arrow_down = get_emoji("⬇️")
    write = get_emoji("✍️")
    confused = get_emoji("😕")
    airplane = get_emoji("🛫")
