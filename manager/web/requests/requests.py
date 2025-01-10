from typing import Optional, Dict
from .Service import Service
from .GoogleDriveService import GoogleDriveService

# Initialize services
drive_service = GoogleDriveService()

async def get_folder(folder_name: str) -> Dict[str, str]:
    """
    Find or create a folder with given name in Google Drive.
    
    Args:
        folder_name (str): Name of the folder to search/create
        
    Returns:
        Dict[str, str]: Dictionary containing folder_id and status
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
