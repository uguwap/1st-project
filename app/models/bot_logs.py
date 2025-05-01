from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, SQLModel


class BotLog(SQLModel, table=True):
    __tablename__ = "bot_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    event_type: str
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id")
    chat_id: Optional[int] = None
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

