from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from bot.keyboards.inline import create_inline_keyboard

commands_router = Router()

@commands_router.message(Command('start'))
async def start_command(m: Message):
    """Обработчик команды /start"""
    await m.answer(f'Привет, {m.chat.id}')