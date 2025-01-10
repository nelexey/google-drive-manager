from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_file_type_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Промежуточный", callback_data="file_type:intermediate"),
            InlineKeyboardButton(text="Финальный", callback_data="file_type:final")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)