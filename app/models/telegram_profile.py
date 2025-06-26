from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict

class TelegramProfile(SQLModel, table=True):
    __tablename__ = "telegram_profile"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    chat_id: int
    username: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)

