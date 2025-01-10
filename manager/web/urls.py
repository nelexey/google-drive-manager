from typing import Dict, List
from web.handlers.handlers import upload_file_handler

urls: List[Dict[str, str]] = [
    {
        'method': 'POST',
        'path': '/transit_files/',
        'handler': upload_file_handler
    }
]
