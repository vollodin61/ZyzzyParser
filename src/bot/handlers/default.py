from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

def_router = Router()


@def_router.message(CommandStart())
async def cmd_start_handler(msg: Message):
    await msg.answer("Hello, my friend! 🤗\n\nНажми на кнопку, получишь результат! 😉")
