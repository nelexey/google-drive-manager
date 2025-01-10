from aiogram.fsm.state import State, StatesGroup

class UploadFiles(StatesGroup):
    waiting_contract = State()  # Ожидание номера договора
    uploading = State()         # Загрузка файлов