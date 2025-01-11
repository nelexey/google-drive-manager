from typing import List, Tuple
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def create_inline_keyboard(data: List[Tuple[str, str]], row_width: int = 3) -> InlineKeyboardMarkup:
    """
    Создает инлайн клавиатуру с заданными кнопками и шириной строки
    
    Args:
        data: Список кортежей (текст кнопки, callback_data)
        row_width: Максимальное количество кнопок в строке
        
    Returns:
        Объект инлайн клавиатуры
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data=callback_data)
                for text, callback_data in data[i:i + row_width]
            ]
            for i in range(0, len(data), row_width)
        ]
    )
