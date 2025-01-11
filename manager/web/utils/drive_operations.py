import os
import logging
from typing import Dict, List
from ..requests.GoogleDriveService import GoogleDriveService
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)

class DriveOperations:
    def __init__(self):
        self.drive_service = GoogleDriveService()

    async def process_files(self, data: Dict) -> Dict:
        """
        Загружает файлы в Google Drive в соответствующие папки
        
        Args:
            data: Словарь с параметрами:
                source - источник файлов
                folder_name - название папки (номер договора)
                stage - тип файлов (intermediate/final)
                files - список полных путей к файлам
                filesdir - путь к директории
        """
        try:
            main_folder_id = await self.drive_service.find_or_create_folder(data['folder_name'])
            stage_folder_id = await self.drive_service.find_or_create_folder(
                data['stage'],
                parent_id=main_folder_id
            )
            
            uploaded_files = []
            for filename in data['files']:
                file_path = os.path.join(data['filesdir'], filename)
                
                if not os.path.exists(file_path):
                    logger.error(f"Файл не найден: {file_path}")
                    continue
                    
                logger.info(f"Загрузка файла: {filename}")
                file_metadata = {
                    'name': filename,
                    'parents': [stage_folder_id]
                }
                
                try:
                    media = MediaFileUpload(file_path, resumable=True)
                    file = self.drive_service.service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                    ).execute()
                    logger.info(f"Файл {filename} загружен, ID: {file.get('id')}")
                    
                    uploaded_files.append({
                        'name': filename,
                        'id': file.get('id')
                    })
                except Exception as upload_error:
                    logger.error(f"Ошибка загрузки {filename}: {str(upload_error)}")
                    continue
            
            return {
                'status': 'success',
                'message': 'Файлы успешно загружены',
                'uploaded_files': uploaded_files
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

def upload_file_to_drive(file_path, folder_id=None):
    """
    Загружает файл в Google Drive
    
    Args:
        file_path: Путь к загружаемому файлу
        folder_id: ID папки в Google Drive (опционально)
    
    Returns:
        ID загруженного файла
    """
    # Остальной код функции...

def get_file_from_drive(file_id):
    """
    Получает файл из Google Drive по его ID
    
    Args:
        file_id: ID файла в Google Drive
        
    Returns:
        Объект файла из Google Drive
    """
    # Остальной код функции... 