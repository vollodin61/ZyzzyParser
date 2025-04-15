from aiogram import Dispatcher

from .default import def_router


def set_routers(dp: Dispatcher):
    dp.include_router(def_router)
