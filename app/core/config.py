import os

from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    WHATSAPP_API_URL: str
    WHATSAPP_API_TOKEN: str

    @computed_field
    @property
    def db_url(self) -> str:
        return self.DATABASE_URL

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        env_file_encoding = "utf-8"

settings = Settings()

