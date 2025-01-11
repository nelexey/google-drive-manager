import os.path
import json
import logging
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class GoogleDriveService:
    """Сервис для работы с Google Drive API"""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self):
        self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def _authenticate(self):
        """Аутентификация через token.json"""
        token_path = 'secrets/token.json'
        
        if not os.path.exists(token_path):
            raise FileNotFoundError(f"Файл токена не найден: {token_path}")
            
        try:
            with open(token_path, 'r') as token_file:
                token_data = json.load(token_file)
                self.creds = Credentials.from_authorized_user_info(token_data, self.SCOPES)
        except Exception as e:
            raise Exception(f"Ошибка загрузки учетных данных: {str(e)}")
    
    async def find_or_create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """
        Поиск папки по имени или создание новой
        
        Args:
            folder_name: Название папки
            parent_id: ID родительской папки
            
        Returns:
            ID папки
        """
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        items = results.get('files', [])
        
        if items:
            return items[0]['id']
        
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        if parent_id:
            folder_metadata['parents'] = [parent_id]
        
        file = self.service.files().create(
            body=folder_metadata,
            fields='id'
        ).execute()
        
        return file.get('id')