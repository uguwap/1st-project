from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class ReminderBase(SQLModel):
    request_id: UUID                # Привязка к заявке
    remind_at: datetime             # Дата и время, когда напомнить
    is_sent: bool = False           # Напоминание уже отправлено или нет


class Reminder(ReminderBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ReminderCreate(ReminderBase):
    pass


class ReminderRead(ReminderBase):
    id: UUID
    created_at: datetime



