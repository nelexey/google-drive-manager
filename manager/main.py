import asyncio
from web.server import init_web_server
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    config = {
        'host': 'localhost',
        'port': 8000,
        'timeout': 60,
        'max_connections': 100
    }
    
    try:
        await init_web_server(config)
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\nЗавершение работы сервера...")

if __name__ == '__main__':
    asyncio.run(main())