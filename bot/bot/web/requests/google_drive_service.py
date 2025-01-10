from typing import Dict
from .Service import Service
from bot.misc.env import settings

# Инициализируем сервис с URL из настроек
google_drive_service = Service(settings.googel_drive_api_connector)

async def upload_files_to_drive(data: Dict) -> Dict:
    """
    Отправляет запрос на загрузку файлов в Google Drive.

    Args:
        data (Dict): Словарь с данными о файлах и параметрах загрузки:
            - uid: уникальный идентификатор загрузки
            - chat_id: ID чата
            - contract_number: номер договора
            - stage: тип файлов (intermediate/final)
            - files: список путей к файлам
            - timestamp: время загрузки

    Returns:
        Dict: Ответ от сервиса
    """
    return await google_drive_service.make_request(
        method='POST',
        data=data,
        uri='transit_files/',
        r_type='json'
    ) 