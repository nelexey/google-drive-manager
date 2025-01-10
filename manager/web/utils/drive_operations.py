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
        Обрабатывает файлы и загружает их в Google Drive.
        
        Args:
            data (Dict): Словарь с данными:
                - source: источник файлов (Telegram, VK, etc)
                - folder_name: название папки (номер договора)
                - stage: тип файлов (intermediate/final)
                - files: список имен файлов
                - filesdir: путь к директории с файлами
                
        Returns:
            Dict: Результат операции
        """
        try:
            # 1. Создаем или находим основную папку (номер договора)
            main_folder_id = await self.drive_service.find_or_create_folder(data['folder_name'])
            
            # 2. Создаем или находим подпапку stage (intermediate/final)
            stage_folder_id = await self.drive_service.find_or_create_folder(
                data['stage'],
                parent_id=main_folder_id
            )
            
            # 3. Загружаем файлы
            uploaded_files = []
            for filename in data['files']:
                file_path = os.path.join(data['filesdir'], filename)
                
                if not os.path.exists(file_path):
                    logger.error(f"File not found: {file_path}")
                    continue
                    
                logger.info(f"Preparing to upload file: {filename}")
                file_metadata = {
                    'name': filename,
                    'parents': [stage_folder_id]
                }
                
                try:
                    media = MediaFileUpload(
                        file_path,
                        resumable=True
                    )
                    logger.info(f"Created MediaFileUpload for {filename}")
                    
                    file = self.drive_service.service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                    ).execute()
                    logger.info(f"Successfully uploaded {filename} with ID: {file.get('id')}")
                    
                    uploaded_files.append({
                        'name': filename,
                        'id': file.get('id')
                    })
                except Exception as upload_error:
                    logger.error(f"Error uploading {filename}: {str(upload_error)}")
                    continue
            
            return {
                'status': 'success',
                'message': 'Files uploaded successfully',
                'uploaded_files': uploaded_files
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            } 