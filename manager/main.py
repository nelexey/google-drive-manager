import asyncio
from web.server import init_web_server
import logging

# Настраиваем логирование один раз при запуске приложения
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    # Configure the web server
    config = {
        'host': 'localhost',
        'port': 8000,
        'timeout': 60,
        'max_connections': 100
    }
    
    # Start the web server
    try:
        await init_web_server(config)
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\nShutting down the server...")


if __name__ == '__main__':
    asyncio.run(main())