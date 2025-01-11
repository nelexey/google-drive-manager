from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    """Настройки приложения из переменных окружения"""
    
    BOT_TOKEN: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    WEB_HOST: str
    WEB_PORT: int
    WEB_TIMEOUT: int
    WEB_MAX_CONNECTIONS: int

    WEB_SERVICE_HOST: str
    WEB_SERVICE_PORT: int

    @property
    def database_url(self) -> str:
        """URL подключения к базе данных"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def bot_token(self) -> str:
        """Токен Telegram бота"""
        return self.BOT_TOKEN

    @property
    def web_config(self) -> dict:
        """Конфигурация веб-сервера"""
        return {
            'host': self.WEB_HOST,
            'port': self.WEB_PORT,
            'timeout': self.WEB_TIMEOUT,
            'max_connections': self.WEB_MAX_CONNECTIONS,
        }

    @property
    def googel_drive_api_connector(self) -> str:
        """URL для подключения к Google Drive API"""
        return f"http://{self.WEB_SERVICE_HOST}:{self.WEB_SERVICE_PORT}"

settings = Settings(_env_file='.env')