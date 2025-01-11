from aiogram import Router
from bot.handlers import user, admin
from .other import other_router

async def register_all_handlers(up_router: Router, **kwargs) -> None:
    """
    Регистрация всех обработчиков в основном роутере
    
    Args:
        up_router: Основной роутер
        **kwargs: Дополнительные параметры (например, bot)
    """
    routers = (
        *admin.register_handlers(up_router),
        *user.register_handlers(up_router, bot=kwargs['bot']),
        other_router
    )

    up_router.include_routers(*routers)
