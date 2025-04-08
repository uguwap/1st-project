from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    WHATSAPP_API_URL: str
    WHATSAPP_API_TOKEN: str

    @computed_field
    @property
    def db_url(self) -> str:
        return self.DATABASE_URL

    class Config:
        env_file = ".env"

settings = Settings()

