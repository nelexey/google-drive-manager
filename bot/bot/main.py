import asyncio
import logging
from aiogram import Bot, Dispatcher, Router

from bot.misc.env import settings
from bot.web.server import init_web_server
from bot.handlers.main import register_all_handlers
from bot.database.models import register_models

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main() -> None:
    """
    Инициализация и запуск бота
    Настраивает веб-сервер и регистрирует обработчики
    """
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    try:
        # Start web server
        logger.info("Запуск веб-сервера...")
        await init_web_server(settings.web_config, bot)
        logger.info(f"Веб-сервер запущен на {settings.web_config['host']}:{settings.web_config['port']}")

        # Register bot handlers
        logger.info("Регистрация обработчиков...")
        main_router = Router()
        await register_all_handlers(main_router, bot=bot)
        dp.include_router(main_router)

        # Start polling
        logger.info("Запуск поллинга...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        await bot.session.close()

    finally:
        # Ensure bot session closes when program ends
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Произошла неожиданная ошибка: {e}")
