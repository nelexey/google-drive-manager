from aiohttp import web
import logging
from typing import Dict
from ..utils.drive_operations import DriveOperations

logger = logging.getLogger(__name__)

drive_ops = DriveOperations()

async def upload_file_handler(request: web.Request) -> web.Response:
    """
    Handles file upload requests to Google Drive.
    Expects JSON with:
        - source: source of files (Telegram, VK, etc)
        - folder_name: contract number as folder name
        - stage: intermediate or final
        - files: list of filenames
        - filesdir: directory containing the files
    """
    try:
        data: Dict = await request.json()
        
        # Validate required parameters
        required_fields = ['source', 'folder_name', 'stage', 'files', 'filesdir']
        for field in required_fields:
            if field not in data:
                return web.json_response({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, status=400)
        
        # Process files using DriveOperations
        result = await drive_ops.process_files(data)
        
        return web.json_response(result)
        
    except Exception as e:
        return web.json_response({
            'status': 'error',
            'message': str(e)
        }, status=500)
