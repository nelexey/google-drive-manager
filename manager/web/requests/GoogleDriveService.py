import os.path
import json
import logging
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class GoogleDriveService:
    """Service for interacting with Google Drive API."""
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    def __init__(self):
        """Initialize the Google Drive service with credentials."""
        self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def _authenticate(self):
        """Authenticate using token.json file."""
        token_path = 'secrets/token.json'
        
        if not os.path.exists(token_path):
            raise FileNotFoundError(f"Token file not found at {token_path}")
            
        try:
            with open(token_path, 'r') as token_file:
                token_data = json.load(token_file)
                self.creds = Credentials.from_authorized_user_info(token_data, self.SCOPES)
        except Exception as e:
            raise Exception(f"Failed to load credentials: {str(e)}")
    
    async def find_or_create_folder(self, folder_name: str, parent_id: str = None) -> str:
        """
        Find folder by name or create if it doesn't exist
        
        Args:
            folder_name (str): Name of the folder to search/create
            parent_id (str, optional): ID of parent folder
            
        Returns:
            str: Folder ID
        """
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        items = results.get('files', [])
        
        # Return existing folder ID if found
        if items:
            return items[0]['id']
        
        # Create new folder if not found
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