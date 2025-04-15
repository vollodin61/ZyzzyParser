from .antispam_middleware import Antispam
from .chat_member_middleware import NewChatMemberVerificationMiddleware
from .scheduler_middleware import SchedulerMiddleware
from .logging_middleware import LoggingMiddleware

from src.bot.config.bot_config import BotConfig


def set_middleware(dp):
	dp.update.outer_middleware.register(LoggingMiddleware(storage=BotConfig.red_storage))
	dp.message.outer_middleware.register(Antispam(storage=BotConfig.red_storage))
	dp.message.outer_middleware.register(NewChatMemberVerificationMiddleware())
	dp.update.middleware.register(SchedulerMiddleware(scheduler=BotConfig.scheduler))
