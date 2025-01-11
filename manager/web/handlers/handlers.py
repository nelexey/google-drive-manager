from aiohttp import web
import logging
from typing import Dict
from ..utils.drive_operations import DriveOperations

logger = logging.getLogger(__name__)

drive_ops = DriveOperations()

async def upload_file_handler(request: web.Request) -> web.Response:
    """
    Обработчик загрузки файлов в Google Drive
    
    Ожидает JSON с параметрами:
        source - источник файлов
        folder_name - название папки (номер договора)
        stage - тип файлов (intermediate/final)
        files - список файлов
        filesdir - путь к директории
    """
    try:
        data: Dict = await request.json()
        
        required_fields = ['source', 'folder_name', 'stage', 'files', 'filesdir']
        for field in required_fields:
            if field not in data:
                return web.json_response({
                    'status': 'error',
                    'message': f'Отсутствует обязательное поле: {field}'
                }, status=400)
        
        result = await drive_ops.process_files(data)
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({
            'status': 'error',
            'message': str(e)
        }, status=500)
