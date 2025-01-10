from aiogram import Router, Bot
from typing import Tuple

from .commands import commands_router
from .upload import upload_router

def register_handlers(up_router: Router, **kwargs) -> Tuple[Router, ...]:
    routers = (
        commands_router,
        upload_router,
    )
    
    return routers