from aiogram import Router
from aiogram.types import Message


other_router = Router()

@other_router.message()
async def please_use_commands(msg: Message):
    """Обработчик для неизвестных команд"""
    await msg.answer('Я не могу обработать эту команду')
