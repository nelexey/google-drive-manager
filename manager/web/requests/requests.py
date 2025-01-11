from typing import Optional, Dict
from .Service import Service
from .GoogleDriveService import GoogleDriveService


drive_service = GoogleDriveService()

async def get_folder(folder_name: str) -> Dict[str, str]:
    """
    Поиск или создание папки в Google Drive
    
    Args:
        folder_name: Название папки
        
    Returns:
        Словарь с ID папки и статусом операции
    """
    try:
        folder_id = await drive_service.find_or_create_folder(folder_name)
        return {
            'status': 'success',
            'folder_id': folder_id
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
