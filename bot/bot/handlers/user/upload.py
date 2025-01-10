import os
import uuid
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.misc.states import UploadFiles
from bot.keyboards.inline.upload_keyboard import get_file_type_keyboard
from datetime import datetime
import json
from bot.web.requests.google_drive_service import upload_files_to_drive

upload_router = Router()

@upload_router.message(F.document | F.video | F.photo)
async def handle_file(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    # Если состояние не установлено, запрашиваем номер договора
    if not current_state:
        await message.answer("Пожалуйста, сначала введите номер договора:")
        await state.set_state(UploadFiles.waiting_contract)
        # Сохраняем первый файл во временном хранилище
        await state.update_data(temp_message=message)
        return

    # Если ожидаем номер договора, игнорируем файлы
    if current_state == UploadFiles.waiting_contract:
        await message.answer("Пожалуйста, сначала введите номер договора:")
        return

    # Обработка файлов
    data = await state.get_data()
    if 'upload_uid' not in data:
        data['upload_uid'] = str(uuid.uuid4())
        data['files'] = []
        await state.set_data(data)
        
    # Создаем временную директорию
    temp_path = f"temp/{message.chat.id}/{data['upload_uid']}"
    os.makedirs(temp_path, exist_ok=True)
    
    # Скачиваем файл
    if message.document:
        file = message.document
        file_path = f"{temp_path}/{file.file_name}"
    elif message.video:
        file = message.video
        file_path = f"{temp_path}/video_{file.file_id}.mp4"
    else:  # photo
        file = message.photo[-1]
        file_path = f"{temp_path}/photo_{file.file_id}.jpg"
    
    await message.bot.download(file, file_path)
    
    # Сохраняем путь к файлу
    data['files'].append(file_path)
    await state.set_data(data)
    
    # Спрашиваем тип файла
    await message.answer(
        "Это промежуточные или финальные файлы?",
        reply_markup=get_file_type_keyboard()
    )

@upload_router.message(UploadFiles.waiting_contract)
async def handle_contract_number(message: Message, state: FSMContext):
    contract_number = message.text.strip()
    
    # Проверка формата номера договора если нужно
    if not contract_number:
        await message.answer("Пожалуйста, введите корректный номер договора")
        return
        
    # Сохраняем номер договора
    await state.update_data(contract_number=contract_number)
    await state.set_state(UploadFiles.uploading)
    
    # Обрабатываем сохраненный файл если он есть
    data = await state.get_data()
    if temp_message := data.get('temp_message'):
        await handle_file(temp_message, state)
        # Удаляем временное сообщение
        await state.update_data(temp_message=None)

@upload_router.callback_query(F.data.startswith("file_type:"))
async def process_file_type(callback: CallbackQuery, state: FSMContext):
    file_type = callback.data.split(":")[1]
    data = await state.get_data()
    
    # Формируем новую структуру запроса
    result = {
        "source": "Telegram",
        "folder_name": data['contract_number'],
        "stage": file_type,
        "files": [os.path.basename(f) for f in data['files']],
        "filesdir": os.path.abspath(f"temp/{callback.message.chat.id}/{data['upload_uid']}")
    }
    
    try:
        response = await upload_files_to_drive(result)
        await callback.message.answer("Файлы успешно отправлены на обработку!")
            
    except Exception as e:
        await callback.message.answer("Произошла ошибка при отправке файлов. Попробуйте позже.")
        print('Error:', str(e))
    
    finally:
        await state.clear()